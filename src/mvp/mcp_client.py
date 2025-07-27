"""
VERN MCP Client

Connects to MCP servers and lists available tools/resources.
"""

import asyncio
from mcp.client.session import ClientSession

class VernMCPClient:
    def __init__(self, *args, **kwargs):
        # ClientSession is async and requires streams; we'll use the stdio transport for now
        pass

    async def list_tools(self, server_url="http://localhost:8080"):
        """
        List available tools from the MCP server using HTTP transport.
        """
        import httpx
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{server_url}/v1/tools/list",
                    json={"method": "tools/list", "params": {}},
                    timeout=10,
                )
                resp.raise_for_status()
                data = resp.json()
                return data
        except Exception as e:
            return f"HTTP error: {e}"

    async def call_tool(self, tool_name, params, server_url="http://localhost:8080"):
        """
        Call a tool by name with parameters.
        """
        return "MCP tool call not yet implemented (requires async transport setup)."
