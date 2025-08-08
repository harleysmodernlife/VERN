from fastapi import APIRouter, Body, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from vern_backend.app.memory import MemoryGraph
from vern_backend.app.vector_memory import VectorMemory
from vern_backend.app.registry_service import registry, AgentRecord

memory = MemoryGraph()
vector_memory = VectorMemory()

# Provide a safe shim for get_events to avoid AttributeError in minimal slice
if not hasattr(memory, "get_events"):
    # Maintain a simple in-memory log per user_id
    _EVENTS = {}

    def _add_event(user_id: str, event_type: str, properties=None):
        from datetime import datetime, timezone
        properties = properties or {}
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": event_type,
            "properties": properties,
        }
        _EVENTS.setdefault(user_id, []).append(entry)

    def _get_events(user_id: str):
        return _EVENTS.get(user_id, [])

    # Monkey-patch minimal methods used in this slice
    setattr(memory, "add_event", _add_event)
    setattr(memory, "get_events", _get_events)

def get_recent_events(user_id: str, limit: int = 10):
    events = memory.get_events(user_id)
    # Sort by timestamp descending, get latest 'limit' events
    events_sorted = sorted(events, key=lambda e: e.get("timestamp", ""), reverse=True)
    return events_sorted[:limit]

router = APIRouter(prefix="/agents", tags=["agents"])

class OrchestratorRequest(BaseModel):
    user_input: str
    context: dict = {}
    agent_status: str | None = None
    user_id: str = "default_user"
    verbose: bool = False

class OrchestratorResponse(BaseModel):
    response: str

def _extract_requested_action(ctx: dict) -> str:
    """
    Determine requested action using precedence:
    requested_action > action > tool.action > tool.name (mapped) > intent
    Returns '' if none found.
    """
    if not isinstance(ctx, dict):
        return ""
    # 1) requested_action
    ra = ctx.get("requested_action")
    if isinstance(ra, str) and ra:
        return ra
    # 2) action
    a = ctx.get("action")
    if isinstance(a, str) and a:
        return a
    # 3) tool.action
    tool = ctx.get("tool")
    if isinstance(tool, dict):
        ta = tool.get("action")
        if isinstance(ta, str) and ta:
            return ta
        # 4) tool.name mapped
        tn = tool.get("name")
        if isinstance(tn, str) and tn:
            mapping = {
                "fetch": "web.fetch",
                "web": "web.fetch",
                "email": "email.send",
                "reader": "file.read",
                "writer": "file.write",
            }
            if tn in mapping:
                return mapping[tn]
    # 5) intent
    intent = ctx.get("intent")
    if isinstance(intent, str) and intent:
        return intent
    return ""

@router.post("/orchestrator/respond")
def orchestrator_respond_api(req: OrchestratorRequest = Body(...)):
    """
    NOTE: When privacy consent is required, this endpoint SHORT-CIRCUITS and returns ONLY:
    {
      "policy_required": true,
      "action": "<file.read|file.write|web.fetch|email.send>",
      "reason": "string",
      "request_id": "uuid",
      "suggested_scope": { ... },
      "expires_at": <number|null>,
      "user_id": "<user>"
    }
    Otherwise, returns {"response": "..."}.
    """
    # Input validation: sanitize user_input
    user_input = (req.user_input or "").strip()
    if not user_input:
        return {"response": "Error: user_input cannot be empty."}

    # Build context with history
    recent_events = get_recent_events(req.user_id)
    context_with_history = dict(req.context or {})
    context_with_history["recent_events"] = recent_events

    # PRIVACY: evaluate sensitive action
    try:
        from vern_backend.app.privacy_policy import SENSITIVE_ACTIONS  # to check valid set
    except Exception:
        SENSITIVE_ACTIONS = {"file.read", "file.write", "web.fetch", "email.send"}

    action = _extract_requested_action(context_with_history)
    if isinstance(action, str) and action in SENSITIVE_ACTIONS:
        # call policy evaluate directly (same process)
        try:
            from vern_backend.app.privacy_policy import engine
            required, payload = engine.evaluate(action, req.user_id, context_with_history)
            if required and payload and payload.get("policy_required"):
                # Include user_id for UI convenience
                payload["user_id"] = req.user_id
                # audit: privacy_prompt
                try:
                    from src.db.logger import log_action
                    log_action(
                        "orchestrator",
                        req.user_id,
                        "privacy_prompt",
                        {"request_id": payload.get("request_id"), "action": action, "reason": payload.get("reason"), "scope": payload.get("suggested_scope")}
                    )
                except Exception:
                    pass
                return payload
        except Exception as _e:
            # if privacy check fails unexpectedly, proceed but annotate context
            context_with_history["privacy_check_failed"] = str(_e)

    # Wire to real orchestrator logic
    try:
        from src.mvp.orchestrator import orchestrator_respond
        # Some versions of orchestrator_respond accept fewer args; call defensively.
        try:
            response_stream = orchestrator_respond(
                user_input,
                context_with_history,
                req.agent_status,
                req.user_id,
                req.verbose
            )
        except TypeError:
            try:
                response_stream = orchestrator_respond(
                    user_input,
                    context_with_history,
                    req.agent_status,
                    req.user_id
                )
            except TypeError:
                try:
                    response_stream = orchestrator_respond(
                        user_input,
                        context_with_history,
                        req.agent_status
                    )
                except TypeError:
                    try:
                        response_stream = orchestrator_respond(
                            user_input,
                            context_with_history
                        )
                    except TypeError:
                        response_stream = orchestrator_respond(user_input)
        # Join streamed output into a string for API response
        if hasattr(response_stream, "__iter__") and not isinstance(response_stream, str):
            response = "".join(list(response_stream))
        else:
            response = str(response_stream)
        # Persist user input and response as events in memory graph (shim-safe)
        try:
            memory.add_event(req.user_id, "user_input", properties={"input": user_input})
            memory.add_event(req.user_id, "agent_response", properties={"response": response})
        except Exception as _e:
            print(f"[WARN] Failed to persist events: {_e}")
        return {"response": response}
    except Exception as e:
        print(f"[ERROR] Orchestrator API error: {str(e)}")
        return {"response": f"Error: {str(e)}"}

# --- Workflows (unchanged) ---
from src.mvp.orchestrator import create_workflow, list_workflows, run_workflow
from inspect import isasyncgen, isgenerator
from types import AsyncGeneratorType, GeneratorType

@router.post("/workflows/create")
async def api_create_workflow(request: Request):
    data = await request.json()
    name = data.get("name")
    steps = data.get("steps", [])
    if not name or not isinstance(steps, list) or not steps:
        return JSONResponse(content={"error": "Invalid workflow payload: 'name' and non-empty 'steps' required."}, status_code=400)
    result = create_workflow(name, steps)
    return {"result": result}

@router.get("/workflows/list")
def api_list_workflows():
    return list_workflows()

import inspect
from typing import Any

def _normalize_result_sync(value: Any) -> Any:
    # Sync helper to keep return JSON-safe
    try:
        if inspect.isgenerator(value):
            return "".join(str(x) for x in value)
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        if isinstance(value, (dict, list)):
            return value
        # Iterables (non-string) fallback
        if hasattr(value, "__iter__") and not isinstance(value, (str, bytes, dict, list)):
            try:
                return "".join(str(x) for x in value)  # type: ignore
            except Exception:
                return str(value)
        return str(value)
    except Exception:
        return str(value)

async def _normalize_result(value: Any) -> Any:
    # Await coroutines
    if inspect.isawaitable(value):
        try:
            value = await value  # type: ignore
        except Exception as _e:
            return str(_e)
    # Strict async generator first
    if inspect.isasyncgen(value):
        parts: list[str] = []
        try:
            async for chunk in value:  # type: ignore
                parts.append(str(chunk))
        except Exception:
            pass
        return "".join(parts)
    # Async-iterables implementing __aiter__
    if hasattr(value, "__aiter__") and not isinstance(value, (str, bytes, dict, list)):
        parts: list[str] = []
        try:
            async for chunk in value:  # type: ignore
                parts.append(str(chunk))
        except Exception:
            pass
        return "".join(parts)
    return _normalize_result_sync(value)

@router.post("/workflows/run")
async def api_run_workflow(request: Request):
    data = await request.json()
    name = data.get("name")
    initial_input = data.get("initial_input")
    user_id = data.get("user_id", "default_user")
    workflows = list_workflows()
    if name not in workflows:
        return JSONResponse(content={"error": f"Workflow '{name}' not found."}, status_code=404)

    # The run_workflow function is now async and returns a JSON-serializable list.
    result = await run_workflow(name, initial_input, user_id)
    return {"result": result}

# --- Agent Registry endpoints ---

import json
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from vern_backend.app.errors import error_response  # use project-wide standardized envelope

@router.post("/heartbeat")
async def agent_heartbeat(request: Request):
    """
    Accepts JSON: { name, cluster?, capabilities?, meta? }
    Returns: { ok: true, name, last_seen }
    """
    # Accept legacy form-encoded or json bodies: parse raw text, then json.
    raw = await request.body()
    if not raw:
        return error_response("REGISTRY_HEARTBEAT_INVALID", status.HTTP_400_BAD_REQUEST, "Empty body", request)
    text = raw.decode("utf-8", errors="ignore").strip()

    payload = None
    # Try JSON first
    try:
        payload = json.loads(text)
    except Exception:
        # Try to coerce "key=value&..." form into dict
        if "=" in text and "&" in text:
            parts = [p for p in text.split("&") if p]
            kv = {}
            for p in parts:
                if "=" in p:
                    k, v = p.split("=", 1)
                    kv[k] = v
            payload = kv
        else:
            return error_response("REGISTRY_HEARTBEAT_INVALID", status.HTTP_400_BAD_REQUEST, "Invalid JSON", request)

    if not isinstance(payload, dict):
        return error_response("REGISTRY_HEARTBEAT_INVALID", status.HTTP_400_BAD_REQUEST, "Body must be a JSON object", request)

    name = payload.get("name")
    if not isinstance(name, str) or not name.strip():
        return error_response("REGISTRY_HEARTBEAT_INVALID", status.HTTP_400_BAD_REQUEST, "name is required", request)

    cluster = payload.get("cluster") or "default"
    capabilities_obj = payload.get("capabilities", [])
    meta_obj = payload.get("meta", {})

    # Normalize capabilities:
    # - if string: try JSON parse else split by comma
    # - if not list/dict: wrap as list
    if capabilities_obj is None:
        capabilities_obj = []
    if isinstance(capabilities_obj, str):
        cap_str = capabilities_obj.strip()
        if cap_str.startswith("[") or cap_str.startswith("{"):
            try:
                capabilities_obj = json.loads(cap_str)
            except Exception:
                capabilities_obj = [s for s in cap_str.split(",") if s]
        else:
            capabilities_obj = [s for s in cap_str.split(",") if s]
    if not isinstance(capabilities_obj, (list, dict)):
        capabilities_obj = [str(capabilities_obj)]

    # Normalize meta:
    # - if string: try JSON parse else default {}
    if meta_obj is None:
        meta_obj = {}
    if isinstance(meta_obj, str):
        try:
            m = json.loads(meta_obj)
            meta_obj = m if isinstance(m, dict) else {}
        except Exception:
            meta_obj = {}
    if not isinstance(meta_obj, dict):
        meta_obj = {}

    capabilities_json = json.dumps(capabilities_obj)
    meta_json = json.dumps(meta_obj)

    rec = registry.heartbeat(name, cluster, capabilities_json, meta_json)
    return {"ok": True, "name": rec.name, "last_seen": float(rec.last_seen) if rec.last_seen is not None else None}

class AgentRegistryResponse(BaseModel):
    name: str
    cluster: str
    status: str
    # Expose JSON types at API boundary
    capabilities: dict | list | None = None
    last_seen: float | None = None
    meta: dict | None = None

    @staticmethod
    def from_record(rec: AgentRecord) -> dict:
        # Decode JSON fields if present
        caps = None
        meta = None
        try:
            if rec.capabilities is not None:
                caps = json.loads(rec.capabilities)
        except Exception:
            caps = rec.capabilities  # fall back to raw string
        try:
            if rec.meta is not None:
                meta = json.loads(rec.meta)
        except Exception:
            meta = rec.meta
        return {
            "name": rec.name,
            "cluster": rec.cluster,
            "status": rec.status,
            "capabilities": caps,
            "last_seen": float(rec.last_seen) if rec.last_seen is not None else None,
            "meta": meta,
        }

@router.get("/status")
def agent_cluster_status():
    recs = registry.list()
    # Fallback: if empty, provide the previous minimal defaults
    if not recs:
        status_list = [
            {"name": "admin", "cluster": "Admin", "status": "online"},
            {"name": "research", "cluster": "Research", "status": "online"},
            {"name": "dev_team", "cluster": "Dev Team", "status": "online"},
            {"name": "health", "cluster": "Health", "status": "online"},
        ]
        return JSONResponse(content=status_list)
    return JSONResponse(content=[AgentRegistryResponse.from_record(r) for r in recs])

@router.delete("/{name}")
def delete_agent(name: str, request: Request):
    # Check existence
    if not registry.get(name):
        return error_response("REGISTRY_NOT_FOUND", status.HTTP_404_NOT_FOUND, f"Agent '{name}' not found", request)
    registry.delete(name)
    return {"ok": True, "deleted": name}

@router.get("/workflows/logs")
def workflow_logs():
    # Example: fetch workflow logs from DB
    # For now, return static demo data
    logs = [
        {"timestamp": "2025-08-01T19:00:00Z", "workflow": "trip_planning", "steps": ["research", "weather", "calendar"], "status": "success"},
        {"timestamp": "2025-08-01T19:05:00Z", "workflow": "health_check", "steps": ["health", "emergent"], "status": "success"},
    ]
    return JSONResponse(content=logs)
