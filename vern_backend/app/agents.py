from fastapi import APIRouter, Body
from pydantic import BaseModel
from vern_backend.app.memory import MemoryGraph

memory = MemoryGraph()

def get_recent_events(user_id: str, limit: int = 10):
    events = memory.get_events(user_id)
    # Sort by timestamp descending, get latest 'limit' events
    events_sorted = sorted(events, key=lambda e: e["timestamp"], reverse=True)
    return events_sorted[:limit]

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
        # Fetch recent memory events for user and inject into context
        recent_events = get_recent_events(req.user_id)
        context_with_history = dict(req.context)
        context_with_history["recent_events"] = recent_events

        response_stream = orchestrator_respond(
            user_input,
            context_with_history,
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
        # Persist user input and response as events in memory graph
        memory.add_event(req.user_id, "user_input", properties={"input": user_input})
        memory.add_event(req.user_id, "agent_response", properties={"response": response})
        return OrchestratorResponse(response=response)
    except Exception as e:
        print(f"[ERROR] Orchestrator API error: {str(e)}")
        return OrchestratorResponse(response=f"Error: {str(e)}")

from src.db.logger import log_action
from fastapi.responses import JSONResponse

from src.mvp.orchestrator import create_workflow, list_workflows, run_workflow
from fastapi import Request

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

@router.post("/workflows/run")
async def api_run_workflow(request: Request):
    data = await request.json()
    name = data.get("name")
    initial_input = data.get("initial_input")
    user_id = data.get("user_id", "default_user")
    workflows = list_workflows()
    if name not in workflows:
        return JSONResponse(content={"error": f"Workflow '{name}' not found."}, status_code=404)
    result = run_workflow(name, initial_input, user_id)
    return {"result": result}

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
