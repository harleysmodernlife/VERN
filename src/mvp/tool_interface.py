"""
Tool Interface and Registry for VERN Agents

Defines a base Tool class and a registry for agent tool-calling.
"""

from typing import Any, Dict, Callable

class Tool:
    def __init__(self, name: str, description: str, func: Callable[[Dict[str, Any]], Any]):
        self.name = name
        self.description = description
        self.func = func

    def call(self, params: Dict[str, Any]) -> Any:
        return self.func(params)

# Example tool implementations
def echo_tool(params):
    return params.get("message", "")

def add_tool(params):
    return params.get("a", 0) + params.get("b", 0)

# Tool registry
TOOL_REGISTRY = {
    "echo": Tool(
        name="echo",
        description="Echoes back the provided message.",
        func=echo_tool
    ),
    "add": Tool(
        name="add",
        description="Adds two numbers (a + b).",
        func=add_tool
    ),
}

def get_tool(name: str) -> Tool:
    return TOOL_REGISTRY.get(name)
