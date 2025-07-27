"""
MCP CLI Utility for VERN

Test MCP server connectivity and list available tools.
"""

import asyncio
from mcp_client import VernMCPClient

async def main():
    print("=== VERN MCP CLI ===")
    server_url = input("Enter MCP server URL (default: http://localhost:8080): ").strip() or "http://localhost:8080"
    client = VernMCPClient()
    print(f"Connecting to MCP server at {server_url}...")
    try:
        tools = await client.list_tools(server_url)
        print("Available tools:")
        print(tools)
    except Exception as e:
        print(f"Failed to connect or list tools: {e}")

if __name__ == "__main__":
    asyncio.run(main())
