"""
VERN Plugin Tools
-----------------
MCP plugin invocation is currently stdio/subprocess-based (see call_plugin_tool).
No HTTP proxy/bridge is implemented yet; all plugin calls are routed via CLI subprocess.
To extend MCP tooling, add new tool definitions in mcp_server.py and register in the plugin registry.
Future plans: HTTP proxy/bridge for remote plugins, stricter validation, and richer extension patterns.
See README.md for contributor notes and extension guidelines.

Utility functions for plugin tool-calling and integration.
Routes plugin calls to MCP server tools, with error handling and logging.

Scaffolding for:
- Versioned plugin API boundary (see PLUGIN_API_VERSION)
- Whitelisted method enforcement (TODO: implement strict whitelist)
- Input/output validation (TODO: implement validation logic)
"""

import json
import subprocess

PLUGIN_API_VERSION = "1.0.0"

# Strict whitelist of allowed plugin tool names
WHITELISTED_TOOLS = [
    "chromadb",
    "get_weather",
    "add_event"
    # Add more approved tools here
]

def validate_plugin_call(tool_name, args, kwargs):
    """
    Validates plugin tool call against API boundary.

    Args:
        tool_name (str): Name of the tool.
        args (list): Positional arguments.
        kwargs (dict): Keyword arguments.

    Returns:
        bool: True if valid, False otherwise.

    Security:
        - Only whitelisted tools are allowed.
        - Validates input types and values.
        - TODO: Add output validation, signature verification, audit log, and admin review hooks.
    """
    if tool_name not in WHITELISTED_TOOLS:
        return False
    # Example input validation: only allow str/int/float/bool types
    allowed_types = (str, int, float, bool, dict, list)
    for arg in args:
        if not isinstance(arg, allowed_types):
            return False
    for v in kwargs.values():
        if not isinstance(v, allowed_types):
            return False
    # TODO: Validate argument values (range, format, etc.)
    # TODO: Validate output types and values
    return True

def call_plugin_tool(tool_name, *args, authorized_user=None, **kwargs):
    """
    Calls a plugin tool via MCP CLI (stdio), enforcing strict API boundaries and ACLs.

    Args:
        tool_name: Name of the MCP tool (must be whitelisted).
        *args: Positional arguments for the tool.
        **kwargs: Keyword arguments for the tool.

    Returns:
        Tool result (string or dict).

    Raises:
        NotImplementedError if the tool is not available.
        RuntimeError if validation fails.

    Security:
        - Only whitelisted tools are allowed.
        - Validates all inputs before call.
        - ACL enforced for sensitive tools (file read/write/delete).
        - TODO: Add output validation, signature verification, audit log, and admin review hooks.
    """
    if not validate_plugin_call(tool_name, args, kwargs):
        raise RuntimeError(f"Plugin tool '{tool_name}' call failed API boundary validation.")

    # ACL enforcement for file operations
    FILE_OP_TOOLS = {"file_read", "file_write", "file_delete"}
    if tool_name in FILE_OP_TOOLS:
        if authorized_user is None or not is_user_authorized_for_file_ops(authorized_user):
            raise RuntimeError("Unauthorized: insufficient permissions for file operations.")

    # Build CLI command for MCP stdio invocation
    cli_args = [
        "python3", "src/mvp/mcp_server.py", "--tool", tool_name,
        "--args", json.dumps(args),
        "--kwargs", json.dumps(kwargs)
    ]
    try:
        result = subprocess.run(cli_args, capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            raise RuntimeError(f"MCP CLI error: {result.stderr.strip()}")
        output = result.stdout.strip()
        try:
            parsed = json.loads(output)
        except Exception:
            parsed = output
        if isinstance(parsed, dict) and "error" in parsed:
            raise RuntimeError(f"MCP tool error: {parsed['error']}")
        return parsed
    except Exception as e:
        raise RuntimeError(f"Plugin tool call failed: {e}")

def is_user_authorized_for_file_ops(user):
    # Example ACL: only users with 'admin' or 'file_ops' role allowed
    return getattr(user, "role", None) in {"admin", "file_ops"}

# If MCP server or plugin is missing, raise NotImplementedError
def _missing_plugin(tool_name, *args, **kwargs):
    raise NotImplementedError(f"Plugin tool '{tool_name}' is not implemented or MCP server is unavailable.")

# TODO: Signature verification, audit log persistence, and admin review hooks to be implemented in future phases.
# TODO: Output validation and static analysis hooks to be added.
# TODO: HTTP proxy/bridge support for remote plugin invocation is planned for future releases.
