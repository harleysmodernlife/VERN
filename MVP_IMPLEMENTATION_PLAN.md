# VERN MVP Implementation Plan

---

## LLM Backend Modularity & Extensibility

- All agent LLM calls are routed through `src/mvp/llm_router.py`.
- Each backend (Ollama, Hugging Face Transformers, llama.cpp, etc.) has its own wrapper module (e.g., `ollama_llm.py`, `qwen3_llm.py`).
- Backend/model selection is controlled via `config/agent_backends.yaml` (no hardcoding).
- Adding a new backend:
  1. Write a wrapper module in `src/mvp/`.
  2. Add an entry to `agent_backends.yaml`.
  3. Update `llm_router.py` to route calls.
- All wrappers follow a common interface: `generate(prompt, context, **kwargs)`.

---

## Current Supported Backends

- `ollama-<model>` (e.g., `ollama-qwen3:0.6b`, `ollama-phi`)
- `fake_llm` (for testing)
- `qwen3-0.6b` (direct transformers integration)
- More can be added as needed.

---

## Testing & Documentation

- Each backend has its own test (e.g., `test_ollama_llm.py`).
- End-to-end agent tests confirm that swapping backends works.
- Documentation in `QUICKSTART.md`, `AGENT_GUIDES/README.md`, and here is kept up-to-date and crosslinked.

---

## Future-Proofing

- Keep all model-specific logic out of agent code.
- Use config-driven design for everything LLM-related.
- Regularly review and update docs as new models/providers become available.

---

## MCP Server & Tool API

- VERN includes a modular MCP server for tool discovery and invocation via the MCP CLI and Inspector.
- See `src/mvp/mcp_server.py` and the "MCP Server Integration" section in README.md for usage and extension instructions.

## See Also

- [QUICKSTART.md](QUICKSTART.md)
- [AGENT_GUIDES/README.md](AGENT_GUIDES/README.md)
- [KNOWN_ISSUES_AND_GOTCHAS.md](KNOWN_ISSUES_AND_GOTCHAS.md)
