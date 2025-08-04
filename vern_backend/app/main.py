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

@app.get("/")
def read_root():
    return {"message": "VERN Backend API is running."}

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
    metadata: list = None

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
    meta: list = None

@app.post("/rag/add")
def add_rag_documents(req: RAGAddRequest):
    rag_memory.add_documents(req.docs, req.meta)
    return {"status": "ok"}

@app.get("/rag/query")
def query_rag_memory(query: str, top_k: int = 5):
    results = rag_memory.query(query, top_k)
    return {"results": results}

@app.get("/secure-status")
def secure_status(user=Depends(get_current_user)):
    return {"status": "secure", "user": user}

# --- Multi-Agent Orchestration API ---

class OrchestrateRequest(BaseModel):
    task: str
    context: dict = {}

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

@app.post("/web_search")
def web_search_api(req: WebSearchRequest):
    # Import MCP tool dynamically
    from src.mvp.mcp_server import web_search
    result = web_search(req.query, req.num_results)
    return {"results": result}
