"""
VERN Plugin Registry
--------------------
Dynamic registry for all MCP tools/plugins.
Supports discovery, metadata, enable/disable, and admin controls.
"""

import inspect
import json
import os
from mcp.server.fastmcp import FastMCP
import mvp.mcp_server as mcp_server

REGISTRY_STATE_FILE = "plugin_registry_state.json"

def _load_registry_state():
    if os.path.exists(REGISTRY_STATE_FILE):
        try:
            with open(REGISTRY_STATE_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading registry state: {e}")
    return {}

def _save_registry_state(state):
    try:
        with open(REGISTRY_STATE_FILE, "w") as f:
            json.dump(state, f)
    except Exception as e:
        print(f"Error saving registry state: {e}")

def get_all_mcp_tools():
    """
    Discover all @mcp.tool-registered tools in mcp_server.
    Returns:
        List of dicts: {name, description, enabled}
    """
    mcp: FastMCP = getattr(mcp_server, "mcp", None)
    if not mcp:
        return []
    tools = []
    import asyncio
    state = _load_registry_state()
    try:
        tool_list = asyncio.run(mcp.list_tools())
        for name in tool_list:
            fn = getattr(mcp_server, name, None)
            doc = inspect.getdoc(fn) or ""
            enabled = state.get(name, True)
            tools.append({
                "name": name,
                "description": doc.split("\n")[0] if doc else "",
                "enabled": enabled
            })
    except Exception as e:
        print(f"Error discovering MCP tools: {e}")
    return tools

def set_tool_enabled(tool_name, enabled=True):
    """
    Enable/disable a tool (admin control).
    Persists state to plugin_registry_state.json.
    """
    state = _load_registry_state()
    state[tool_name] = enabled
    _save_registry_state(state)
    print(f"Set tool '{tool_name}' enabled={enabled}")
