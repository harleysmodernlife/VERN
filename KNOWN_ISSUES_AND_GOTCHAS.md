# VERN Known Issues & Gotchas

---

## MCP Limitations (2025-07)

- **MCP proxy/server does not support direct tool invocation from Python/browser clients.**
  - Tool calls from CLI chat, Python scripts, or browser-based UIs (dashboard, Inspector) are not supported.
  - For MVP, tools are called directly in Python.
  - MCP is used for future extensibility, tool discovery, and integration only.

- **Browser-based UIs (Inspector, dashboard) may fail to connect to MCP proxy due to missing CORS headers.**
  - Tool invocation and config fetches may not work until MCP proxy adds CORS support.

- **Inspector UI may show no tools or fail to connect if MCP server is not running in compatible mode.**
  - Always use `mcp dev src/mvp/mcp_server.py` for Inspector compatibility.

---

## Current MVP Approach

- **Agents and chat interface call Python functions for tools (echo, add, journal, etc.).**
- **Persistent memory and logging are handled via SQLite.**
- **MCP integration is planned for future releases when ecosystem matures.**

---

## Future Plans

- Monitor MCP SDK and CLI for updates enabling direct tool invocation from Python/browser clients.
- Refactor agent/tool code for MCP integration when supported.
- Add web/chat UI for user experience upgrade when CORS and API support are available.

---

## General Gotchas

- Always update TASKS_AND_TODO.md and README.md after confirmed changes.
- Never assume project state—read docs and context before acting.
- If stuck, checkpoint context and ask for review or clarification.

---

**If you encounter new issues, add them here and update the context in TASKS_AND_TODO.md.**
