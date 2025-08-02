from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/plugins", tags=["plugins"])

class PluginInfo(BaseModel):
    name: str
    description: str
    enabled: bool = True

from src.mvp.plugin_registry import get_all_mcp_tools, set_tool_enabled
from fastapi import HTTPException, Body

@router.get("/", response_model=list[PluginInfo])
def list_plugins():
    tools = get_all_mcp_tools()
    return [PluginInfo(name=tool["name"], description=tool["description"], enabled=tool["enabled"]) for tool in tools]

@router.post("/{plugin_name}/enable")
def enable_plugin(plugin_name: str):
    set_tool_enabled(plugin_name, True)
    return {"status": "enabled"}

@router.post("/{plugin_name}/disable")
def disable_plugin(plugin_name: str):
    set_tool_enabled(plugin_name, False)
    return {"status": "disabled"}

class PluginInvokeRequest(BaseModel):
    args: list = []
    kwargs: dict = {}

@router.post("/{plugin_name}/call")
def call_plugin(plugin_name: str, req: PluginInvokeRequest = Body(...)):
    try:
        from src.mvp.plugin_tools import call_plugin_tool
        result = call_plugin_tool(plugin_name, *req.args, **req.kwargs)
        return {"result": result}
    except NotImplementedError:
        raise HTTPException(status_code=404, detail=f"Plugin tool '{plugin_name}' not implemented.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class PluginSubmission(BaseModel):
    name: str
    description: str
    code: str
    author: str

@router.post("/submit")
def submit_plugin(submission: PluginSubmission):
    # For now, just log and acknowledge; in production, review and add to registry
    print(f"[PLUGIN SUBMISSION] {submission.name} by {submission.author}")
    # TODO: Add review, sandboxing, and registry integration
    return {"status": "received", "message": "Plugin submission received for review."}
