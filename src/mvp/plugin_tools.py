"""
VERN Plugin Tools
-----------------
Utility functions for plugin tool-calling and integration.
Routes plugin calls to MCP server tools, with error handling and logging.
"""

import requests
import json

def call_plugin_tool(tool_name, *args, **kwargs):
    """
    Calls a plugin tool via MCP server.
    Args:
        tool_name: Name of the MCP tool (e.g., 'chromadb', 'get_weather', 'add_event').
        *args: Positional arguments for the tool.
        **kwargs: Keyword arguments for the tool.
    Returns:
        Tool result (string or dict).
    Raises:
        NotImplementedError if the tool is not available.
    """
    # MCP server endpoint (adjust as needed)
    MCP_SERVER_URL = "http://localhost:8502/mcp"
    payload = {
        "tool": tool_name,
        "args": args,
        "kwargs": kwargs
    }
    try:
        response = requests.post(MCP_SERVER_URL, json=payload, timeout=5)
        response.raise_for_status()
        result = response.json()
        if "error" in result:
            raise RuntimeError(f"MCP tool error: {result['error']}")
        return result.get("result", result)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("MCP server is not running or unreachable.")
    except Exception as e:
        raise RuntimeError(f"Plugin tool call failed: {e}")

# If MCP server or plugin is missing, raise NotImplementedError
def _missing_plugin(tool_name, *args, **kwargs):
    raise NotImplementedError(f"Plugin tool '{tool_name}' is not implemented or MCP server is unavailable.")
