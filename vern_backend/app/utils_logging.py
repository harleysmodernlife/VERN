import json
import logging
import os
import time
import uuid
from typing import Any, Dict, Optional

# JSON logger with minimal deps. Default JSON unless LOG_FORMAT=plain.
LOG_FORMAT = os.getenv("LOG_FORMAT", "json").lower()


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base: Dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "time": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
        }
        # Pull structured fields from record.__dict__ where logging passes extras
        extras = getattr(record, "__dict__", {})
        extra_payload = extras.get("extra")
        if isinstance(extra_payload, dict):
            base.update(extra_payload)
        return json.dumps(base, ensure_ascii=False)


def get_logger(name: str = "vern") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    if LOG_FORMAT == "json":
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def request_id() -> str:
    return uuid.uuid4().hex

def get_privacy_logger(name: str = "vern.privacy") -> logging.Logger:
    """
    Returns a compartmentalized logger for privacy-relevant events.
    TODO: Add file handler or external export for privacy logs.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    if LOG_FORMAT == "json":
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger

def log_privacy_event(event: str, payload: dict):
    """
    Log a privacy-relevant event using the privacy logger.
    TODO: Integrate with consent management and privacy audit export.
    """
    logger = get_privacy_logger()
    logger.info(event, extra={"extra": payload})


def timing_middleware(app):
    """
    FastAPI/Starlette middleware factory to log structured request/response events.
    Adds: request_id propagation, error_code if present, optional user_id, duration_ms.
    """
    logger = get_logger("vern.api")

    @app.middleware("http")
    async def _middleware(request, call_next):
        rid = request.headers.get("x-request-id") or request_id()
        # propagate request_id to request.state for handlers
        try:
            setattr(request.state, "request_id", rid)
        except Exception:
            pass

        start = time.perf_counter()
        status = 500
        error: Optional[str] = None
        error_code: Optional[str] = None
        user_id: Optional[str] = None
        response = None

        try:
            response = await call_next(request)
            status = getattr(response, "status_code", 200)
            # allow handlers to set error codes on headers/state
            try:
                # priority: request.state.error_code (set by our exception handlers) then x-error-code header
                error_code = getattr(request.state, "error_code", None) or (response.headers.get("x-error-code") if hasattr(response, "headers") else None)
            except Exception:
                pass
            return response
        except Exception as e:
            error = str(e)
            # capture error code from request.state if set by handler/exception handlers
            try:
                ec = getattr(request.state, "error_code", None)
                if ec:
                    error_code = ec
            except Exception:
                pass
            raise
        finally:
            duration_ms = int((time.perf_counter() - start) * 1000)
            # pull optional user_id from request.state if set by upstream
            try:
                user_id = getattr(request.state, "user_id", None)
            except Exception:
                user_id = None

            payload = {
                "event": "http_request",
                "request_id": rid,
                "method": request.method,
                "path": request.url.path,
                "status": status,
                "duration_ms": duration_ms,
                "client": request.client.host if request.client else None,
            }
            if user_id:
                payload["user_id"] = user_id
            if error:
                payload["error"] = error
            if error_code:
                payload["error_code"] = error_code

            logger.info("request", extra={"extra": payload})

    return app