# VERN Known Issues & Gotchas

---

## LLM/Agent Limitations (2025-07)

- **LLM backend (Ollama/Qwen3) may be slow or error-prone on low-resource hardware.**
  - Timeouts, backend errors, or slow responses may occur.
  - If you see errors, try restarting Ollama, switching to a smaller model, or increasing the timeout in `src/mvp/qwen3_llm.py`.
  - See [QUICKSTART.md](QUICKSTART.md) for troubleshooting tips.

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

- **CLI chat is LLM-powered by default (Qwen3 via Ollama), with tool overrides for explicit commands.**
- **Agents and chat interface call Python functions for tools (echo, add, journal, etc.).**
- **Persistent memory and logging are handled via SQLite.**
- **MCP integration is planned for future releases when ecosystem matures.**

---

## Future Plans

- Monitor MCP SDK and CLI for updates enabling direct tool invocation from Python/browser clients.
- Refactor agent/tool code for MCP integration when supported.
- Add web/chat UI for user experience upgrade when CORS and API support are available.
- Extend LLM-powered agent logic to more clusters and workflows.
- Implement agent-to-agent delegation and tool invocation from LLM plans.

---

## Troubleshooting

- If you encounter LLM errors (timeouts, backend errors, slow responses):
  - Restart Ollama and ensure the model is loaded.
  - Try a smaller model (see [QUICKSTART.md](QUICKSTART.md)).
  - Increase the timeout in `src/mvp/qwen3_llm.py`.
  - Check system resources (RAM/CPU).
  - See [README.md](README.md) and [TASKS_AND_TODO.md](TASKS_AND_TODO.md) for more info.

---

## General Gotchas

- Always update TASKS_AND_TODO.md and README.md after confirmed changes.
- Never assume project state—read docs and context before acting.
- If stuck, checkpoint context and ask for review or clarification.

---

**If you encounter new issues, add them here and update the context in TASKS_AND_TODO.md.**
