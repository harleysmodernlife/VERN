"""
VERN MCP Client

Connects to MCP servers and lists/calls available tools/resources.
"""

import asyncio
import uuid
import anyio

from mcp.client.streamable_http import streamablehttp_client
from mcp.types import JSONRPCRequest, JSONRPCMessage
from mcp.shared.message import SessionMessage

# Update MCP_URL to match your Streamable HTTP endpoint
MCP_URL = "http://localhost:3001/sse"

class VernMCPClient:
    """
    VERN MCP Client for connecting to MCP servers and listing/calling tools.
    """

    async def list_tools(self, server_url=None):
        """
        List available tools from the MCP server.
        """
        url = server_url or MCP_URL
        async with streamablehttp_client(url) as (read_stream, write_stream, get_session_id):
            request_id = str(uuid.uuid4())
            request = JSONRPCRequest(
                jsonrpc="2.0",
                id=request_id,
                method="list_tools",
                params={},
            )
            message = JSONRPCMessage(request)
            session_message = SessionMessage(message)
            await write_stream.send(session_message)
            async for response in read_stream:
                if hasattr(response, "root") and hasattr(response.root, "id") and response.root.id == request_id:
                    if hasattr(response.root, "result"):
                        return response.root.result
                    elif hasattr(response.root, "error"):
                        raise Exception(f"Tool error: {response.root.error}")
                if hasattr(response, "message") and hasattr(response.message, "root") and hasattr(response.message.root, "id") and response.message.root.id == request_id:
                    if hasattr(response.message.root, "result"):
                        return response.message.root.result
                    elif hasattr(response.message.root, "error"):
                        raise Exception(f"Tool error: {response.message.root.error}")
        raise Exception("No response from MCP server.")

    async def call_tool_async(self, tool, params):
        async with streamablehttp_client(MCP_URL) as (read_stream, write_stream, get_session_id):
            request_id = str(uuid.uuid4())
            request = JSONRPCRequest(
                jsonrpc="2.0",
                id=request_id,
                method=tool,
                params=params,
            )
            message = JSONRPCMessage(request)
            session_message = SessionMessage(message)
            await write_stream.send(session_message)
            async for response in read_stream:
                if hasattr(response, "root") and hasattr(response.root, "id") and response.root.id == request_id:
                    if hasattr(response.root, "result"):
                        return response.root.result
                    elif hasattr(response.root, "error"):
                        raise Exception(f"Tool error: {response.root.error}")
                if hasattr(response, "message") and hasattr(response.message, "root") and hasattr(response.message.root, "id") and response.message.root.id == request_id:
                    if hasattr(response.message.root, "result"):
                        return response.message.root.result
                    elif hasattr(response.message.root, "error"):
                        raise Exception(f"Tool error: {response.message.root.error}")
        raise Exception("No response from MCP server.")

    def call_tool(self, tool, params):
        return asyncio.run(self.call_tool_async(tool, params))
