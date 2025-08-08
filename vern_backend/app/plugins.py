from fastapi import APIRouter, Body, status, Request
from pydantic import BaseModel

"""
VERN Backend Plugin API
----------------------
API endpoints for plugin management, invocation, and registry.

Scaffolding for:
- Admin review workflow (TODO: implement approval and review system)
- Automated static analysis (TODO: add code analysis hooks)
"""

router = APIRouter(prefix="/plugins", tags=["plugins"])

class PluginInfo(BaseModel):
    name: str
    description: str
    enabled: bool = True

from src.mvp.plugin_registry import get_all_mcp_tools, set_tool_enabled
from vern_backend.app.errors import PluginInvalidError, error_response

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
def call_plugin(plugin_name: str, req: PluginInvokeRequest = Body(...), request: Request = None):
    all_tools = [tool["name"] for tool in get_all_mcp_tools()]
    if plugin_name not in all_tools:
        raise PluginInvalidError(f"Plugin '{plugin_name}' not found.")

    try:
        from src.mvp.plugin_tools import call_plugin_tool
        # Extract user from request.state (assumes authentication middleware sets request.state.user)
        authorized_user = getattr(request.state, "user", None)
        result = call_plugin_tool(plugin_name, *req.args, authorized_user=authorized_user, **req.kwargs)
        return {"result": result}
    except ConnectionError:
        return error_response("INTEGRATION_UNAVAILABLE", status.HTTP_503_SERVICE_UNAVAILABLE, "MCP server is not running or unreachable.", request)
    except Exception as e:
        return error_response("INTEGRATION_ERROR", status.HTTP_502_BAD_GATEWAY, str(e), request)

class PluginSubmission(BaseModel):
    name: str
    description: str
    code: str
    author: str

@router.post("/{plugin_name}/update")
def update_plugin(plugin_name: str, submission: PluginSubmission = Body(...)):
    # TODO: Implement update logic (e.g., replace code, validate, reload)
    # TODO: Integrate with admin review workflow (approval required)
    # TODO: Add static analysis for submitted code
    print(f"[PLUGIN UPDATE] {plugin_name} by {submission.author}")
    # For now, just acknowledge
    return {"status": "received", "message": f"Plugin '{plugin_name}' update received for review."}

@router.post("/{plugin_name}/remove")
def remove_plugin(plugin_name: str):
    # TODO: Implement removal logic (e.g., delete from registry, unload)
    # TODO: Integrate with admin review workflow (approval required)
    print(f"[PLUGIN REMOVE] {plugin_name}")
    # For now, just acknowledge
    return {"status": "received", "message": f"Plugin '{plugin_name}' removal received for review."}

@router.post("/submit")
def submit_plugin(submission: PluginSubmission):
    # For now, just log and acknowledge; in production, review and add to registry
    print(f"[PLUGIN SUBMISSION] {submission.name} by {submission.author}")
    # TODO: Add review, sandboxing, and registry integration
    # TODO: Integrate with admin review workflow (approval required)
    # TODO: Add static analysis for submitted code
    return {"status": "received", "message": "Plugin submission received for review."}
