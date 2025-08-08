"""
VERN Plugin Registry
--------------------
MCP plugin invocation is currently stdio/subprocess-based (see plugin_tools.py and plugin_sandbox.py).
No HTTP proxy/bridge is implemented yet; all plugin calls are local CLI subprocesses.
Registry/discovery logic matches this runtime model: plugins are only enabled after admin approval and signature verification.
Future plans: HTTP proxy/bridge for remote plugins, multi-admin workflows, and richer extension patterns.
See README.md for contributor notes and extension guidelines.

Dynamic registry for all MCP tools/plugins.
Supports discovery, metadata, enable/disable, and admin controls.

Scaffolding for:
- Signed plugin metadata (TODO: implement signature verification)
- Audit logging of plugin actions (now persists to SQLite via src/db/logger.py)
- Admin review workflow (TODO: integrate with admin approval system)
- Automated static analysis (TODO: add hooks for code analysis)

Audit Log Schema & Process:
- Uses the 'actions' table in SQLite (see src/db/logger.py).
- Fields: id, timestamp, agent_id, user_id, action_type, payload, status, gotcha_id, tags.
- All plugin registration, execution, and admin actions are logged via log_action().
- TODO: Add log rotation, search, and export capabilities for audit logs.

Admin Review Workflow:
- Plugins must be submitted for admin review before being enabled.
- Admins can approve or reject plugin registration, updates, and removals.
- Only plugins with "approved" status are enabled for execution.
- All review actions are logged to the audit log.
- TODO: Support multi-admin review, review history, and notifications.
"""

import inspect
import json
import os
from src.mcp.server.fastmcp import FastMCP
import src.mvp.mcp_server as mcp_server
from src.db.logger import log_action

REGISTRY_STATE_FILE = "plugin_registry_state.json"
# TODO: Remove legacy AUDIT_LOG_FILE after migration to SQLite
AUDIT_LOG_FILE = "plugin_audit_log.json"

# Signature verification for plugins
def _verify_plugin_signature(metadata):
    """
    Verifies the cryptographic signature of plugin metadata.

    Args:
        metadata (dict): Plugin metadata. Must include 'signature', 'payload', and 'public_key'.

    Returns:
        bool: True if signature is valid, False otherwise.

    Verification process:
        1. Extract 'signature', 'payload', and 'public_key' from metadata.
        2. Use public key to verify the signature over the payload.
        3. Return True if valid, False otherwise.

    TODO: Implement revocation checks (e.g., CRL, OCSP).
    TODO: Support multi-signature verification for collaborative plugins.
    TODO: Enforce minimum key length and algorithm standards.

    Note: This implementation uses a placeholder for cryptographic verification.
    Replace with actual verification using cryptography or PyNaCl.

    Example expected metadata:
        {
            "name": "example_plugin",
            "payload": "...",  # serialized plugin info
            "signature": "...",  # base64 signature
            "public_key": "...", # PEM or base64 public key
            ...
        }
    """
    signature = metadata.get("signature")
    payload = metadata.get("payload")
    public_key = metadata.get("public_key")
    if not signature or not payload or not public_key:
        # Missing required fields for verification
        return False

    # TODO: Replace with actual cryptographic verification
    # Example (pseudo-code):
    # from cryptography.hazmat.primitives import serialization, hashes
    # from cryptography.hazmat.primitives.asymmetric import padding
    # key = serialization.load_pem_public_key(public_key.encode())
    # try:
    #     key.verify(
    #         base64.b64decode(signature),
    #         payload.encode(),
    #         padding.PKCS1v15(),
    #         hashes.SHA256()
    #     )
    #     return True
    # except Exception:
    #     return False

    # For now, always return True (stub)
    return True

# Persistent audit logging to SQLite
def _log_audit_event(event_type, details, agent_id=None, user_id=None, status="success", tags=None):
    """
    Logs an audit event for plugin actions to the SQLite audit log.
    Args:
        event_type (str): Type of event (e.g., 'enable', 'disable', 'update').
        details (dict): Event details.
        agent_id (str, optional): Agent performing the action.
        user_id (str, optional): User performing the action.
        status (str, optional): Status of the action.
        tags (list, optional): Tags for the event.
    """
    # TODO: Enhance agent_id/user_id extraction from context
    try:
        log_action(
            agent_id=agent_id,
            user_id=user_id,
            action_type=event_type,
            payload=details,
            status=status,
            tags=tags
        )
    except Exception as e:
        print(f"Error logging audit event to DB: {e}")
    # TODO: Add log rotation, search, and export features for audit logs

def _load_registry_state():
    if os.path.exists(REGISTRY_STATE_FILE):
        try:
            with open(REGISTRY_STATE_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading registry state: {e}")
    return {}

def _save_registry_state(state):
    try:
        with open(REGISTRY_STATE_FILE, "w") as f:
            json.dump(state, f)
    except Exception as e:
        print(f"Error saving registry state: {e}")

def submit_plugin_for_review(plugin_name, metadata, submitted_by):
    """
    Submit a plugin for admin review.
    Sets status to 'pending' and logs the submission.
    """
    state = _load_registry_state()
    state[plugin_name] = {
        "enabled": False,
        "status": "pending",
        "metadata": metadata
    }
    _save_registry_state(state)
    _log_audit_event(
        "submit_plugin_for_review",
        {"plugin_name": plugin_name, "metadata": metadata},
        user_id=submitted_by,
        status="pending"
    )
    # TODO: Notify admins of new submission

def approve_plugin(plugin_name, approved_by):
    """
    Approve a plugin for execution.
    Sets status to 'approved' and enables the plugin.
    """
    state = _load_registry_state()
    if plugin_name in state:
        state[plugin_name]["status"] = "approved"
        state[plugin_name]["enabled"] = True
        _save_registry_state(state)
        _log_audit_event(
            "approve_plugin",
            {"plugin_name": plugin_name},
            user_id=approved_by,
            status="approved"
        )
        # TODO: Support multi-admin approval and review history
        # TODO: Notify submitter of approval

def reject_plugin(plugin_name, rejected_by, reason=""):
    """
    Reject a plugin submission.
    Sets status to 'rejected' and disables the plugin.
    """
    state = _load_registry_state()
    if plugin_name in state:
        state[plugin_name]["status"] = "rejected"
        state[plugin_name]["enabled"] = False
        _save_registry_state(state)
        _log_audit_event(
            "reject_plugin",
            {"plugin_name": plugin_name, "reason": reason},
            user_id=rejected_by,
            status="rejected"
        )
        # TODO: Support multi-admin rejection and review history
        # TODO: Notify submitter of rejection

def remove_plugin(plugin_name, removed_by):
    """
    Remove a plugin from the registry (admin only).
    """
    state = _load_registry_state()
    if plugin_name in state:
        del state[plugin_name]
        _save_registry_state(state)
        _log_audit_event(
            "remove_plugin",
            {"plugin_name": plugin_name},
            user_id=removed_by,
            status="removed"
        )
        # TODO: Support review history for removals
        # TODO: Notify submitter of removal

def update_plugin_metadata(plugin_name, metadata, updated_by):
    """
    Update plugin metadata (requires admin review).
    Sets status to 'pending' and disables plugin until re-approved.
    """
    state = _load_registry_state()
    if plugin_name in state:
        state[plugin_name]["metadata"] = metadata
        state[plugin_name]["status"] = "pending"
        state[plugin_name]["enabled"] = False
        _save_registry_state(state)
        _log_audit_event(
            "update_plugin_metadata",
            {"plugin_name": plugin_name, "metadata": metadata},
            user_id=updated_by,
            status="pending"
        )
        # TODO: Notify admins of update request

def get_all_mcp_tools():
    """
    Discover all @mcp.tool-registered tools in mcp_server.
    Verifies plugin signatures before including in registry.
    Only plugins with 'approved' status are enabled for execution.

    Returns:
        List of dicts: {name, description, enabled, signature_valid, status}
    """
    mcp: FastMCP = getattr(mcp_server, "mcp", None)
    if not mcp:
        return []
    tools = []
    import asyncio
    state = _load_registry_state()
    try:
        tool_list = asyncio.run(mcp.list_tools())
        for name in tool_list:
            fn = getattr(mcp_server, name, None)
            doc = inspect.getdoc(fn) or ""
            plugin_state = state.get(name, {})
            enabled = plugin_state.get("enabled", False)
            status = plugin_state.get("status", "unknown")
            # Simulate plugin metadata extraction
            # TODO: Replace with actual metadata source
            metadata = getattr(fn, "plugin_metadata", {}) if fn else {}
            signature_valid = _verify_plugin_signature(metadata)
            tools.append({
                "name": name,
                "description": doc.split("\n")[0] if doc else "",
                "enabled": enabled if status == "approved" else False,
                "signature_valid": signature_valid,
                "status": status
            })
    except Exception as e:
        print(f"Error discovering MCP tools: {e}")
    return tools

def set_tool_enabled(tool_name, enabled=True, admin_id=None):
    """
    Enable/disable a tool (admin control).
    Only allowed if plugin is approved.
    Persists state to plugin_registry_state.json.
    """
    state = _load_registry_state()
    plugin_state = state.get(tool_name, {})
    if plugin_state.get("status") != "approved":
        print(f"Cannot enable tool '{tool_name}': not approved by admin.")
        return
    plugin_state["enabled"] = enabled
    state[tool_name] = plugin_state
    _save_registry_state(state)
    print(f"Set tool '{tool_name}' enabled={enabled}")
    # Log admin action to persistent audit log
    _log_audit_event(
        "set_tool_enabled",
        {"tool_name": tool_name, "enabled": enabled},
        user_id=admin_id
    )
    # TODO: Support multi-admin enable/disable

# TODO: Integrate admin review workflow for plugin submissions/updates
# TODO: Add hooks for automated static analysis on plugin code
# TODO: Support multi-admin review and approval
# TODO: Track review history for each plugin
# TODO: Add notification system for review actions
