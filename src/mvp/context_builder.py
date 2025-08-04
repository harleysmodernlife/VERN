"""
VERN Context Builder
-------------------
Assembles context for agent orchestration:
- User request
- Available MCP tools
- History/logs
- Permissions
- System state
"""

import os
import json

class ContextBuilder:
    def __init__(self, user_request: str, user_id: int = None, config: dict = None):
        """
        ContextBuilder now supports config flags for fine-tuning context assembly.
        config: {
            "include_tools": bool,
            "include_history": bool,
            "include_permissions": bool,
            "include_system_state": bool,
            "custom_processors": dict (optional, for advanced overrides)
        }
        """
        self.user_request = user_request
        self.user_id = user_id
        self.config = config or {
            "include_tools": True,
            "include_history": True,
            "include_permissions": True,
            "include_system_state": True,
            "custom_processors": {}
        }
        self.context = {
            "user_request": user_request,
            "user_id": user_id
        }
        if self.config.get("include_tools", True):
            self.context["tools"] = self._process("tools", self.get_available_tools())
        if self.config.get("include_history", True):
            self.context["history"] = self._process("history", self.get_history())
        if self.config.get("include_permissions", True):
            self.context["permissions"] = self._process("permissions", self.get_permissions())
        if self.config.get("include_system_state", True):
            self.context["system_state"] = self._process("system_state", self.get_system_state())

    def _process(self, key, value):
        # Use custom processor if provided, else return value as-is
        processor = self.config.get("custom_processors", {}).get(key)
        if processor:
            return processor(value)
        return value

    def get_available_tools(self):
        # Stub: Replace with MCP server tool registry query
        # Example: Query MCP server for registered tools
        return ["echo", "add", "file_read", "file_write", "file_list", "file_delete",
                "get_weather", "add_event", "list_events", "fileops_list_files", "fileops_read_file"]

    def get_history(self):
        # Stub: Replace with DB/log query
        # Example: Load recent actions from log file
        history_path = "db/user_history.json"
        if os.path.exists(history_path):
            try:
                with open(history_path, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def get_permissions(self):
        # Stub: Replace with real permissions logic
        # Example: Load user permissions from DB/config
        return {"can_read": True, "can_write": True, "can_schedule": True}

    def get_system_state(self):
        # Stub: Replace with real system state logic
        # Example: Load system status, resource usage, etc.
        return {"status": "online", "resources": {"cpu": "normal", "ram": "normal"}}

    def build(self):
        return self.context
