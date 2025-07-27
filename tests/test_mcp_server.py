"""
Integration tests for src/mvp/mcp_server.py MCP tools.
Requires the MCP server to be running with: mcp dev src/mvp/mcp_server.py
"""

import pytest
from mcp.client import MCPClient

@pytest.fixture(scope="module")
def mcp_client():
    # Connect to the running MCP server (default inspector proxy)
    return MCPClient("http://127.0.0.1:6277")

def test_echo(mcp_client):
    result = mcp_client.call_tool("echo", {"text": "hello"})
    assert result == "hello"

def test_add(mcp_client):
    result = mcp_client.call_tool("add", {"a": 2, "b": 3})
    assert result == 5

def test_file_write_and_read(mcp_client, tmp_path):
    test_file = tmp_path / "test.txt"
    mcp_client.call_tool("file_write", {"path": str(test_file), "content": "abc"})
    content = mcp_client.call_tool("file_read", {"path": str(test_file)})
    assert content == "abc"

def test_file_list(mcp_client, tmp_path):
    test_file = tmp_path / "foo.txt"
    test_file.write_text("bar")
    files = mcp_client.call_tool("file_list", {"directory": str(tmp_path), "glob_pattern": "*.txt"})
    assert any("foo.txt" in f for f in files)

def test_file_delete(mcp_client, tmp_path):
    test_file = tmp_path / "del.txt"
    test_file.write_text("gone")
    mcp_client.call_tool("file_delete", {"path": str(test_file)})
    assert not test_file.exists()

def test_cluster_status(mcp_client):
    status = mcp_client.call_tool("cluster_status", {})
    assert isinstance(status, dict)
    assert "dev_team" in status

def test_schedule_event(mcp_client):
    result = mcp_client.call_tool("schedule_event", {"details": "Team sync at 10am"})
    assert "Meeting scheduled" in result

def test_journal_entry(mcp_client):
    result = mcp_client.call_tool("journal_entry", {"entry": "Today I felt great"})
    assert "Health/Wellness result" in result or "journal" in result.lower()

def test_finance_balance(mcp_client):
    result = mcp_client.call_tool("finance_balance", {})
    assert "Finance/Resource result" in result or "balance" in result.lower()
