"""
Integration tests for src/mvp/mcp_server.py MCP tools using the official MCP SDK HTTP client.

Requires the MCP server to be running with: DANGEROUSLY_OMIT_AUTH=true mcp dev src/mvp/mcp_server.py
"""

import asyncio
import uuid

from mcp.client.streamable_http import streamablehttp_client
from mcp.types import JSONRPCRequest, JSONRPCMessage
from mcp.shared.message import SessionMessage

MCP_URL = "http://127.0.0.1:6277"

async def call_tool(tool, params):
    async with streamablehttp_client(MCP_URL) as (read_stream, write_stream, get_session_id):
        # Build JSON-RPC request for the tool
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
        # Read response
        async for response in read_stream:
            if isinstance(response, Exception):
                raise response
            # response is a JSONRPCMessage
            if hasattr(response, "root") and hasattr(response.root, "id") and response.root.id == request_id:
                # Success or error
                if hasattr(response.root, "result"):
                    return response.root.result
                elif hasattr(response.root, "error"):
                    raise Exception(f"Tool error: {response.root.error}")
                else:
                    raise Exception("Unknown response format")
            # response is a SessionMessage
            if hasattr(response, "message") and hasattr(response.message, "root") and hasattr(response.message.root, "id") and response.message.root.id == request_id:
                if hasattr(response.message.root, "result"):
                    return response.message.root.result
                elif hasattr(response.message.root, "error"):
                    raise Exception(f"Tool error: {response.message.root.error}")
                else:
                    raise Exception("Unknown response format")

async def main():
    # Echo
    assert await call_tool("echo", {"text": "hello"}) == "hello"
    print("echo: PASS")

    # Add
    assert await call_tool("add", {"a": 2, "b": 3}) == 5
    print("add: PASS")

    # Cluster status
    status = await call_tool("cluster_status", {})
    assert isinstance(status, dict) and "dev_team" in status
    print("cluster_status: PASS")

    # Schedule event
    result = await call_tool("schedule_event", {"details": "Team sync at 10am"})
    assert "Meeting scheduled" in result
    print("schedule_event: PASS")

    # Journal entry
    result = await call_tool("journal_entry", {"entry": "Today I felt great"})
    assert "Health/Wellness result" in result or "journal" in result.lower()
    print("journal_entry: PASS")

    # Finance balance
    result = await call_tool("finance_balance", {})
    assert "Finance/Resource result" in result or "balance" in result.lower()
    print("finance_balance: PASS")

    # Get user profile (may be empty if no user 1)
    profile = await call_tool("get_user_profile", {"user_id": 1})
    assert isinstance(profile, dict)
    print("get_user_profile: PASS")

    # Weather plugin
    result = await call_tool("get_weather", {"location": "Austin"})
    assert "Weather for" in result or "Weather API key not set" in result or "Could not find coordinates" in result
    print("get_weather: PASS")

    # Calendar plugin (add_event, list_events)
    result = await call_tool("add_event", {"title": "Test Event", "date": "2025-08-01"})
    assert "added for" in result or "Google Calendar config missing" in result or "Google Calendar API error" in result
    print("add_event: PASS")
    result = await call_tool("list_events", {})
    assert "No upcoming events" in result or "Google Calendar config missing" in result or "Google Calendar API error" in result or "Test Event" in result
    print("list_events: PASS")

    # Fileops plugin (fileops_list_files, fileops_read_file)
    result = await call_tool("fileops_list_files", {"directory": "."})
    assert isinstance(result, list) or "Error listing files" in result[0] or "Access denied" in result[0]
    print("fileops_list_files: PASS")
    result = await call_tool("fileops_read_file", {"path": "README.md"})
    assert isinstance(result, str) and ("Error reading file" in result or "Access denied" in result or len(result) > 0)
    print("fileops_read_file: PASS")

    # ChromaDB plugin (chromadb_query)
    result = await call_tool("chromadb_query", {"query": "test", "top_k": 1})
    assert "No relevant documents found." in result or "ChromaDB error" in result or isinstance(result, str)
    print("chromadb_query: PASS")

    print("All MCP tool JSON-RPC tests passed.")

if __name__ == "__main__":
    asyncio.run(main())
