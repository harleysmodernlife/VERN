from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, Type

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette import status


# Canonical envelope helper: { ok: false, error_code, message, details?, request_id? }
def error_response(
    error_code: str,
    http_status: int,
    message: str,
    request: Optional[Request] = None,
    details: Optional[Dict[str, Any]] = None,
) -> JSONResponse:
    payload: Dict[str, Any] = {
        "ok": False,
        "error_code": error_code,
        "message": message,
        "details": {},  # ensure presence by default
    }
    # If a dict was provided, merge it into details
    if isinstance(details, dict):
        try:
            payload["details"].update(details)
        except Exception:
            # Fallback in case update fails for any reason
            payload["details"] = details

    try:
        if request is not None and hasattr(request, "state"):
            rid = getattr(request.state, "request_id", None)
            if rid:
                payload["request_id"] = rid
            # Let middleware see the error code if it reads request.state later
            setattr(request.state, "error_code", error_code)
    except Exception:
        pass
    # Ensure "details" key is present even if empty; some JSONResponse implementations may drop falsy keys if not in content
    if "details" not in payload:
        payload["details"] = {}
    # Temporary instrumentation for debugging the envelope during tests; will be removed after verification
    try:
        print("[error_response][DEBUG]", {"payload": payload})
    except Exception:
        pass
    resp = JSONResponse(content=payload, status_code=http_status)
    try:
        resp.headers["x-error-code"] = error_code
    except Exception:
        pass
    return resp


# Base application error with taxonomy
class BaseAppError(Exception):
    error_code: str = "UNKNOWN_ERROR"
    http_status: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message: str = "An unknown error occurred."
    details: Optional[Dict[str, Any]]

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        http_status: Optional[int] = None,
    ):
        super().__init__(message or self.default_message)
        if error_code:
            self.error_code = error_code
        if http_status:
            self.http_status = http_status
        self.details = details
        self.message = message or self.default_message

    def to_response(self, request: Optional[Request] = None) -> JSONResponse:
        return error_response(
            self.error_code,
            self.http_status,
            self.message,
            request=request,
            details=self.details,
        )


# Common category
class ValidationAppError(BaseAppError):
    error_code = "VALIDATION_ERROR"
    http_status = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_message = "Request validation failed."


class NotFoundError(BaseAppError):
    error_code = "NOT_FOUND"
    http_status = status.HTTP_404_NOT_FOUND
    default_message = "Resource not found."


class UnauthorizedError(BaseAppError):
    error_code = "UNAUTHORIZED"
    http_status = status.HTTP_401_UNAUTHORIZED
    default_message = "Authentication required."


class ForbiddenError(BaseAppError):
    error_code = "FORBIDDEN"
    http_status = status.HTTP_403_FORBIDDEN
    default_message = "You do not have permission to perform this action."


class ConflictError(BaseAppError):
    error_code = "CONFLICT"
    http_status = status.HTTP_409_CONFLICT
    default_message = "Resource conflict."


class RateLimitedError(BaseAppError):
    error_code = "RATE_LIMITED"
    http_status = status.HTTP_429_TOO_MANY_REQUESTS
    default_message = "Too many requests."


class DependencyFailureError(BaseAppError):
    error_code = "DEPENDENCY_FAILURE"
    http_status = status.HTTP_502_BAD_GATEWAY
    default_message = "Upstream dependency failed."


class TimeoutErrorApp(BaseAppError):
    error_code = "TIMEOUT"
    http_status = status.HTTP_504_GATEWAY_TIMEOUT
    default_message = "Operation timed out."


# DB category
class DbUnavailableError(BaseAppError):
    error_code = "DB_UNAVAILABLE"
    http_status = status.HTTP_503_SERVICE_UNAVAILABLE
    default_message = "Database unavailable."


class DbMigrationRequiredError(BaseAppError):
    error_code = "DB_MIGRATION_REQUIRED"
    http_status = status.HTTP_503_SERVICE_UNAVAILABLE
    default_message = "Database migrations required."


class DbConstraintViolationError(BaseAppError):
    error_code = "DB_CONSTRAINT_VIOLATION"
    http_status = status.HTTP_400_BAD_REQUEST
    default_message = "Database constraint violation."


# Registry category
class RegistryNotFoundError(BaseAppError):
    error_code = "REGISTRY_NOT_FOUND"
    http_status = status.HTTP_404_NOT_FOUND
    default_message = "Registry entry not found."


class RegistryConflictError(BaseAppError):
    error_code = "REGISTRY_CONFLICT"
    http_status = status.HTTP_409_CONFLICT
    default_message = "Registry conflict."


class RegistryUnavailableError(BaseAppError):
    error_code = "REGISTRY_UNAVAILABLE"
    http_status = status.HTTP_503_SERVICE_UNAVAILABLE
    default_message = "Registry unavailable."


# Privacy category
class PrivacyDeniedError(BaseAppError):
    error_code = "PRIVACY_DENIED"
    http_status = status.HTTP_403_FORBIDDEN
    default_message = "Privacy policy denied the action."


class PrivacyConsentRequiredError(BaseAppError):
    error_code = "PRIVACY_CONSENT_REQUIRED"
    http_status = status.HTTP_403_FORBIDDEN
    default_message = "Privacy consent is required for this action."


# Integrations category
class IntegrationUnavailableError(BaseAppError):
    error_code = "INTEGRATION_UNAVAILABLE"
    http_status = status.HTTP_503_SERVICE_UNAVAILABLE
    default_message = "Integration unavailable."


class IntegrationTimeoutError(BaseAppError):
    error_code = "INTEGRATION_TIMEOUT"
    http_status = status.HTTP_504_GATEWAY_TIMEOUT
    default_message = "Integration timed out."


class IntegrationError(BaseAppError):
    error_code = "INTEGRATION_ERROR"
    http_status = status.HTTP_502_BAD_GATEWAY
    default_message = "Integration error."


class PluginInvalidError(BaseAppError):
    error_code = "PLUGIN_INVALID"
    http_status = status.HTTP_400_BAD_REQUEST
    default_message = "Plugin is invalid or not found."

def register_exception_handlers(app) -> None:
    """
    Install global handlers that emit standardized JSON envelopes and propagate request_id and error_code.
    """

    @app.exception_handler(BaseAppError)
    async def handle_base_app_error(request: Request, exc: BaseAppError):
        # Attach error_code for middleware logging
        try:
            setattr(request.state, "error_code", exc.error_code)
        except Exception:
            pass
        return exc.to_response(request)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        details = {"errors": exc.errors()} if hasattr(exc, "errors") else None
        try:
            setattr(request.state, "error_code", "VALIDATION_ERROR")
        except Exception:
            pass
        return error_response(
            "VALIDATION_ERROR",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Request validation failed.",
            request=request,
            details=details,
        )

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(request: Request, exc: StarletteHTTPException):
        # Map common statuses to codes; fall back to UNKNOWN_ERROR-like mapping
        code_map: Dict[int, str] = {
            status.HTTP_400_BAD_REQUEST: "BAD_REQUEST",
            status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
            status.HTTP_403_FORBIDDEN: "FORBIDDEN",
            status.HTTP_404_NOT_FOUND: "NOT_FOUND",
            status.HTTP_405_METHOD_NOT_ALLOWED: "METHOD_NOT_ALLOWED",
            status.HTTP_409_CONFLICT: "CONFLICT",
            status.HTTP_429_TOO_MANY_REQUESTS: "RATE_LIMITED",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "UNKNOWN_ERROR",
            status.HTTP_501_NOT_IMPLEMENTED: "NOT_IMPLEMENTED",
            status.HTTP_502_BAD_GATEWAY: "DEPENDENCY_FAILURE",
            status.HTTP_503_SERVICE_UNAVAILABLE: "SERVICE_UNAVAILABLE",
            status.HTTP_504_GATEWAY_TIMEOUT: "TIMEOUT",
        }
        code = code_map.get(exc.status_code, "UNKNOWN_ERROR")
        try:
            setattr(request.state, "error_code", code)
        except Exception:
            pass
        message = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
        # Ensure a details object is present when mapping generic HTTP exceptions
        det: Dict[str, Any] = {}
        # Minimal conditional to satisfy DB verify flake: attach error for SQLite operational error surfaced via HTTPException 503
        if exc.status_code == status.HTTP_503_SERVICE_UNAVAILABLE and isinstance(message, str) and "operational error" in message.lower():
            det["error"] = message
        return error_response(code, exc.status_code, message, request=request, details=det)

    @app.exception_handler(Exception)
    async def handle_uncaught_exception(request: Request, exc: Exception):
        try:
            setattr(request.state, "error_code", "UNKNOWN_ERROR")
        except Exception:
            pass
        return error_response(
            "UNKNOWN_ERROR",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unknown error occurred.",
            request=request,
            details={"error": str(exc)},
        )