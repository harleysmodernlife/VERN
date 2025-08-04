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
    from fastapi import HTTPException
    try:
        from src.mvp.plugin_tools import call_plugin_tool
        result = call_plugin_tool(plugin_name, *req.args, **req.kwargs)
        return {"result": result}
    except NotImplementedError:
        raise HTTPException(status_code=404, detail=f"Plugin tool '{plugin_name}' not implemented.")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="MCP server is not running or unreachable.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class PluginSubmission(BaseModel):
    name: str
    description: str
    code: str
    author: str

@router.post("/{plugin_name}/update")
def update_plugin(plugin_name: str, submission: PluginSubmission = Body(...)):
    # TODO: Implement update logic (e.g., replace code, validate, reload)
    print(f"[PLUGIN UPDATE] {plugin_name} by {submission.author}")
    # For now, just acknowledge
    return {"status": "received", "message": f"Plugin '{plugin_name}' update received for review."}

@router.post("/{plugin_name}/remove")
def remove_plugin(plugin_name: str):
    # TODO: Implement removal logic (e.g., delete from registry, unload)
    print(f"[PLUGIN REMOVE] {plugin_name}")
    # For now, just acknowledge
    return {"status": "received", "message": f"Plugin '{plugin_name}' removal received for review."}

@router.post("/submit")
def submit_plugin(submission: PluginSubmission):
    # For now, just log and acknowledge; in production, review and add to registry
    print(f"[PLUGIN SUBMISSION] {submission.name} by {submission.author}")
    # TODO: Add review, sandboxing, and registry integration
    return {"status": "received", "message": "Plugin submission received for review."}
