from fastapi import APIRouter, Body
from pydantic import BaseModel

router = APIRouter(prefix="/agents", tags=["agents"])

class OrchestratorRequest(BaseModel):
    user_input: str
    context: dict = {}
    agent_status: str = None
    user_id: str = "default_user"
    verbose: bool = False

class OrchestratorResponse(BaseModel):
    response: str

@router.post("/orchestrator/respond", response_model=OrchestratorResponse)
def orchestrator_respond_api(req: OrchestratorRequest = Body(...)):
    # Input validation: sanitize user_input
    user_input = req.user_input.strip()
    if not user_input:
        return OrchestratorResponse(response="Error: user_input cannot be empty.")
    # Wire to real orchestrator logic
    try:
        from src.mvp.orchestrator import orchestrator_respond
        response_stream = orchestrator_respond(
            user_input,
            req.context,
            req.agent_status,
            req.user_id,
            req.verbose
        )
        # Join streamed output into a string for API response
        if hasattr(response_stream, "__iter__") and not isinstance(response_stream, str):
            response = "".join(list(response_stream))
        else:
            response = str(response_stream)
        # Audit log (optional, can be expanded)
        print(f"[AUDIT] Orchestrator called by user_id={req.user_id} with input='{user_input}'")
        return OrchestratorResponse(response=response)
    except Exception as e:
        print(f"[ERROR] Orchestrator API error: {str(e)}")
        return OrchestratorResponse(response=f"Error: {str(e)}")

from db.logger import log_action
from fastapi.responses import JSONResponse

@router.get("/status")
def agent_cluster_status():
    # Example: fetch agent/cluster status from DB or in-memory registry
    # For now, return static demo data
    status = [
        {"name": "research", "cluster": "Research", "status": "online"},
        {"name": "finance", "cluster": "Finance", "status": "online"},
        {"name": "health", "cluster": "Health", "status": "online"},
        {"name": "admin", "cluster": "Admin", "status": "online"},
        {"name": "emergent", "cluster": "Emergent", "status": "online"},
        {"name": "orchestrator", "cluster": "Orchestrator", "status": "online"},
    ]
    return JSONResponse(content=status)

@router.get("/workflows/logs")
def workflow_logs():
    # Example: fetch workflow logs from DB
    # For now, return static demo data
    logs = [
        {"timestamp": "2025-08-01T19:00:00Z", "workflow": "trip_planning", "steps": ["research", "weather", "calendar"], "status": "success"},
        {"timestamp": "2025-08-01T19:05:00Z", "workflow": "health_check", "steps": ["health", "emergent"], "status": "success"},
    ]
    return JSONResponse(content=logs)
