import os
import pytest
import mvp.plugin_registry as registry

def test_registry_enable_disable_persistence(tmp_path, monkeypatch):
    # Use a temp file for registry state
    test_file = tmp_path / "plugin_registry_state.json"
    monkeypatch.setattr(registry, "REGISTRY_STATE_FILE", str(test_file))

    # Simulate tool names
    tool_name = "test_tool"
    registry.set_tool_enabled(tool_name, True)
    state = registry._load_registry_state()
    assert state[tool_name] is True

    registry.set_tool_enabled(tool_name, False)
    state = registry._load_registry_state()
    assert state[tool_name] is False

def test_get_all_mcp_tools_handles_missing_mcp(monkeypatch):
    # Patch mcp_server to have no mcp instance
    monkeypatch.setattr(registry, "mcp_server", type("Dummy", (), {})())
    tools = registry.get_all_mcp_tools()
    assert tools == []

def test_get_all_mcp_tools_returns_tools(monkeypatch):
    # Patch mcp_server with dummy mcp and list_tools
    class DummyMCP:
        async def list_tools(self):
            return ["tool_a", "tool_b"]
    dummy_server = type("DummyServer", (), {"mcp": DummyMCP(), "tool_a": lambda: None, "tool_b": lambda: None})()
    monkeypatch.setattr(registry, "mcp_server", dummy_server)
    monkeypatch.setattr(registry, "_load_registry_state", lambda: {"tool_a": True, "tool_b": False})
    tools = registry.get_all_mcp_tools()
    names = [t["name"] for t in tools]
    assert "tool_a" in names and "tool_b" in names
    enabled = {t["name"]: t["enabled"] for t in tools}
    assert enabled["tool_a"] is True
    assert enabled["tool_b"] is False
