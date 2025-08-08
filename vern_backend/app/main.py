from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Body
from pydantic import BaseModel
from vern_backend.app.agents import router as agents_router
from vern_backend.app.plugins import router as plugins_router
from vern_backend.app.users import router as users_router
from vern_backend.app.config import router as config_router
from vern_backend.app.integrations import router as integrations_router
from vern_backend.app.memory import MemoryGraph
from vern_backend.app.vector_memory import VectorMemory
from vern_backend.app.rag import RAGMemory
# Added for deterministic admin_db_verify responses
from starlette.responses import Response
import json

from src.mvp.agent_registry import orchestrate
from src.mvp.privacy_agent import PrivacyAgent

memory = MemoryGraph()
vector_memory = VectorMemory()
rag_memory = RAGMemory()
privacy_agent = PrivacyAgent()

app = FastAPI(
    title="VERN Backend API",
    description="Modular FastAPI backend for agent orchestration, plugin registry, and user/session management.",
    version="0.1.0"
)

# Structured logging middleware (JSON by default)
from vern_backend.app.utils_logging import timing_middleware
timing_middleware(app)

# Global standardized error handling
from vern_backend.app.errors import register_exception_handlers
register_exception_handlers(app)

# CORS: allow frontend on localhost:3000 (and Docker hostnames) to call API from browser
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://vern-frontend:3000",
        "http://frontend:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run lightweight SQLite migrations at startup
try:
    from src.db.migrate import migrate as run_db_migrations
    run_db_migrations()
    print("[startup] Applied pending DB migrations")
    # DB startup verification: ensure agents table exists
    from vern_backend.app.db_path import get_sqlite_path
    import sqlite3
    db_path = get_sqlite_path()
    with sqlite3.connect(db_path) as _con:
        cur = _con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='agents'")
        row = cur.fetchone()
        if row and row[0] == "agents":
            print("[startup] DB check: agents table OK")
        else:
            print("[startup][WARN] DB check: agents table MISSING")
except Exception as _e:
    print(f"[startup][WARN] DB migrations failed or unavailable: {_e}")

# Simple health endpoint for connectivity checks
@app.get("/health")
def health():
    from datetime import datetime, timezone
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}

# --- Admin / DB verify (consolidated) ---
from fastapi import Request
from vern_backend.app.errors import error_response
from starlette import status as _status
import sqlite3 as _sqlite3

# Ensure 'sqlite3' name is used within handler body so patch("vern_backend.app.main.sqlite3.connect") intercepts

@app.get("/admin/db/verify")
def admin_db_verify(request: Request):
    """
    Returns:
      { ok: true, path, migrated: bool, version: int } on success,
      or standardized error envelope DB_UNAVAILABLE / UNKNOWN_ERROR.
    """
    from vern_backend.app.db_path import get_sqlite_path
    try:
        path = get_sqlite_path()
    except Exception as e:
        # Path resolution itself failed
        rid = getattr(request.state, "request_id", None)
        body = {
            "ok": False,
            "error_code": "UNKNOWN_ERROR",
            "message": "An unknown error occurred.",
            "details": {"error": str(e), "path": None},
        }
        if rid:
            body["request_id"] = rid
        # One-run debug to confirm payload
        try:
            print("[admin_db_verify][DEBUG][path_error]", body)
        except Exception:
            pass
        return Response(
            content=json.dumps(body, ensure_ascii=False),
            media_type="application/json",
            status_code=_status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers={"x-error-code": "UNKNOWN_ERROR"},
        )

    try:
        with sqlite3.connect(path) as con:
            # Prefer schema_migrations if present
            cur = con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_migrations'")
            has_sm = cur.fetchone() is not None
            version = 0
            migrated = False
            if has_sm:
                migrated = True
                try:
                    # Attempt to get max version, if column exists
                    cur = con.execute("SELECT MAX(version) FROM schema_migrations")
                    row = cur.fetchone()
                    if row and row[0] is not None:
                        version = int(row[0])
                except _sqlite3.OperationalError:
                    # Fallback for legacy schema_migrations without version column
                    cur = con.execute("SELECT COUNT(*) FROM schema_migrations")
                    row = cur.fetchone()
                    if row and row[0] is not None:
                        version = int(row[0])
            else:
                cur = con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='agents'")
                migrated = cur.fetchone() is not None
            return {"ok": True, "path": path, "migrated": bool(migrated), "version": int(version)}
    except sqlite3.OperationalError as e:
        rid = getattr(request.state, "request_id", None)
        body = {
            "ok": False,
            "error_code": "DB_UNAVAILABLE",
            "message": "Database unavailable.",
            "details": {"error": str(e), "path": path},
        }
        if rid:
            body["request_id"] = rid
        try:
            print("[admin_db_verify][DEBUG][db_unavailable]", body)
        except Exception:
            pass
        return Response(
            content=json.dumps(body, ensure_ascii=False),
            media_type="application/json",
            status_code=_status.HTTP_503_SERVICE_UNAVAILABLE,
            headers={"x-error-code": "DB_UNAVAILABLE"},
        )
    except Exception as e:
        rid = getattr(request.state, "request_id", None)
        body = {
            "ok": False,
            "error_code": "UNKNOWN_ERROR",
            "message": "An unknown error occurred.",
            "details": {"error": str(e), "path": path},
        }
        if rid:
            body["request_id"] = rid
        try:
            print("[admin_db_verify][DEBUG][unknown_error]", body)
        except Exception:
            pass
        return Response(
            content=json.dumps(body, ensure_ascii=False),
            media_type="application/json",
            status_code=_status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers={"x-error-code": "UNKNOWN_ERROR"},
        )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # TODO: Validate JWT token and return user info
    if not token or token == "fake":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")
    return {"user_id": "default_user"}

app.include_router(agents_router)
app.include_router(plugins_router)
app.include_router(users_router)
app.include_router(config_router)
app.include_router(integrations_router)

# Include privacy policy API
from vern_backend.app.privacy_api import router as privacy_policy_router
app.include_router(privacy_policy_router)

# Include feedback router
from vern_backend.app.feedback import router as feedback_router
app.include_router(feedback_router)

@app.get("/")
def read_root():
    return {"message": "VERN Backend API is running."}

# (Removed duplicate legacy /admin/db/verify definition to keep a single consolidated handler above)

# --- Memory API ---

@app.post("/memory/entity")
def add_entity(entity_id: str = Body(...), properties: dict = Body(...)):
    memory.add_entity(entity_id, properties)
    return {"status": "ok"}

@app.get("/memory/entity/{entity_id}")
def get_entity(entity_id: str):
    entity = memory.get_entity(entity_id)
    return {"entity": entity}

@app.put("/memory/entity/{entity_id}")
def update_entity(entity_id: str, properties: dict = Body(...)):
    memory.update_entity(entity_id, properties)
    return {"status": "ok"}

@app.delete("/memory/entity/{entity_id}")
def delete_entity(entity_id: str):
    memory.delete_entity(entity_id)
    return {"status": "ok"}

@app.post("/memory/relationship")
def add_relationship(source_id: str = Body(...), target_id: str = Body(...), rel_type: str = Body(...), properties: dict = Body({})):
    memory.add_relationship(source_id, target_id, rel_type, properties)
    return {"status": "ok"}

@app.get("/memory/relationship/{entity_id}")
def get_relationships(entity_id: str):
    rels = memory.get_relationships(entity_id)
    return {"relationships": rels}

@app.post("/memory/event")
def add_event(entity_id: str = Body(...), event_type: str = Body(...), properties: dict = Body({})):
    memory.add_event(entity_id, event_type, properties=properties)
    return {"status": "ok"}

@app.get("/memory/event/{entity_id}")
def get_events(entity_id: str):
    events = memory.get_events(entity_id)
    return {"events": events}

# --- Vector Memory API ---

class VectorMemoryAddRequest(BaseModel):
    docs: list
    metadata: list | None = None

@app.post("/vector_memory/add")
def add_vector_documents(req: VectorMemoryAddRequest):
    vector_memory.add_documents(req.docs, req.metadata)
    return {"status": "ok"}

@app.get("/vector_memory/query")
def query_vector_memory(text: str, top_k: int = 5):
    results = vector_memory.query(text, top_k)
    return {"results": results}

# --- RAG API ---

class RAGAddRequest(BaseModel):
    docs: list
    meta: list | None = None

@app.post("/rag/add")
def add_rag_documents(req: RAGAddRequest):
    # Ensure meta is a list of dicts, fallback to [{}] per doc when None
    meta = req.meta if isinstance(req.meta, list) else None
    if meta is None:
        meta = [{} for _ in req.docs]
    rag_memory.add_documents(req.docs, meta)
    return {"status": "ok"}

@app.get("/rag/query")
def query_rag_memory(query: str, top_k: int = 5):
    results = rag_memory.query(query, top_k)
    return {"results": results}

@app.get("/secure-status")
def secure_status(user=Depends(get_current_user)):
    return {"status": "secure", "user": user}

# --- Multi-Agent Orchestration API ---

from typing import Dict, Any

class OrchestrateRequest(BaseModel):
    task: str
    context: Dict[str, Any] = {}

    # Coerce None or non-dict into {}
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_context

    @classmethod
    def validate_context(cls, values):
        ctx = values.get("context", {})
        if ctx is None or not isinstance(ctx, dict):
            values["context"] = {}
        return values

@app.post("/agents/orchestrate")
def orchestrate_agents(req: OrchestrateRequest):
    result = orchestrate(req.task, req.context)
    return result

# --- Privacy Agent API ---

class PrivacyCheckRequest(BaseModel):
    action: str
    user_id: str
    data: dict

class PrivacySanitizeRequest(BaseModel):
    data: dict

@app.post("/privacy/check_permission")
def check_permission(req: PrivacyCheckRequest):
    allowed = privacy_agent.check_permission(req.action, req.user_id, req.data)
    return {"allowed": allowed}

@app.post("/privacy/sanitize")
def sanitize_data(req: PrivacySanitizeRequest):
    sanitized = privacy_agent.sanitize_data(req.data)
    return {"sanitized": sanitized}

@app.get("/privacy/audit_log")
def get_audit_log():
    return {"audit_log": privacy_agent.get_audit_log()}

# --- Web Search API ---

class WebSearchRequest(BaseModel):
    query: str
    num_results: int = 5

# Feature-flag or temporarily disable web_search in the vertical slice to reduce surface area
ENABLE_WEB_SEARCH = False

@app.post("/web_search")
def web_search_api(req: WebSearchRequest):
    if not ENABLE_WEB_SEARCH:
        raise HTTPException(status_code=501, detail="web_search is disabled in this build.")
    # Import MCP tool dynamically
    from src.mvp.mcp_server import web_search
    result = web_search(req.query, req.num_results)
    return {"results": result}
