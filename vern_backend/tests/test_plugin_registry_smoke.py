import pytest
from src.mvp.plugin_registry import PluginRegistry

def test_plugin_registry_smoke():
    registry = PluginRegistry()
    plugins = registry.list_plugins()
    assert isinstance(plugins, list)
    assert all("name" in plugin for plugin in plugins)