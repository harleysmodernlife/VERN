# Agent Development Guides

Welcome to the VERN Agent Guides! This directory contains documentation, principles, and reference materials for building, testing, and integrating agents within the VERN ecosystem.

---

## Core Principles

All agents and plugins must adhere to the following principles to ensure a robust, secure, and maintainable system.

### 1. Modularity and Independence
- Each agent or cluster should be self-contained and independently deployable.
- Use absolute imports (e.g., `from src.mvp.some_module import ...`) to avoid path ambiguity. Run `python scripts/check_imports.py` to validate.

### 2. Configuration-Driven Backends
- All heavy backends (ASR, TTS, Vision, LLM) are optional and configured in `config/agent_backends.yaml`.
- Agents must check for available resources and fall back to lightweight stubs if a configured backend is unavailable. This ensures VERN can run in resource-constrained environments.

### 3. Standardized Logging
- Use the central logger for all actions, messages, and errors.
- Import loggers from `src/db/logger.py` (`log_action`, `log_message`, `log_gotcha`).

### 4. Security and Sandboxing
- All file operations must be sandboxed to the project root. Use the `fileops` plugin, which prevents directory traversal.
- Never commit secrets. Use `.env.example` as a template and reference `SECURITY_AND_GIT_GUIDELINES.md`.

---

## Agent Error Handling

Agents **must** use the standardized error handling system to ensure consistent API responses. When an error occurs, an agent should either raise a `BaseAppError` subclass or use the `error_response` helper to return a structured JSON error envelope.

This approach provides clients with predictable error formats, including a unique `error_code`, a human-readable `message`, and optional `details`.

### Raising `BaseAppError` Subclasses

The preferred method is to raise an appropriate exception from `vern_backend.app.errors`. This automatically generates the correct HTTP response and logs the error.

**Example:**
```python
from vern_backend.app.errors import NotFoundError, DependencyFailureError

def get_user_profile(user_id: str):
    user = db.get_user(user_id)
    if not user:
        # This will produce a 404 Not Found response
        raise NotFoundError("User profile not found.", details={"user_id": user_id})

    try:
        external_data = external_api.fetch_data(user.api_key)
    except Exception as e:
        # This will produce a 502 Bad Gateway response
        raise DependencyFailureError("Failed to fetch data from external API.", details={"reason": str(e)})

    return user.profile
```

### Using the `error_response` Helper

For cases where raising an exception is not suitable (e.g., in certain middleware or custom handlers), you can directly return a `JSONResponse` created by the `error_response` helper.

**Example:**
```python
from fastapi import Request
from vern_backend.app.errors import error_response

async def some_custom_handler(request: Request):
    if not request.headers.get("X-Custom-Auth"):
        return error_response(
            error_code="UNAUTHORIZED",
            http_status=401,
            message="Missing X-Custom-Auth header.",
            request=request
        )
    # ... proceed with logic
```

---

## API Interaction & Protocols

VERN provides several APIs and protocols for agent-to-agent communication, data storage, and interaction with external systems.

### Memory API (Knowledge Graph)
- **Endpoint:** `/memory/*`
- **Backend:** In-memory, file-based, or Neo4j (configurable via `VERN_MEMORY_BACKEND`).
- **Usage:** Store and retrieve entities and relationships in the knowledge graph. Agents should interact with the unified API, not the backend directly.
- **Reference:** `vern_backend/app/memory.py`

### Vector Memory API (Semantic Search)
- **Endpoint:** `/vector_memory/*`
- **Usage:** Add documents and perform semantic queries.
- **Reference:** `vern_backend/app/vector_memory.py`

### RAG API (Document Retrieval)
- **Endpoint:** `/rag/*`
- **Usage:** Add documents and query for retrieval-augmented generation.
- **Reference:** `vern_backend/app/rag.py`

### Privacy Agent API
- **Endpoint:** `/privacy/*`
- **Usage:** Check permissions, sanitize data, and audit actions.
- **Reference:** `vern_backend/app/privacy_api.py`

### Multi-Agent Orchestration API
- **Endpoint:** `/agents/orchestrate`
- **Usage:** Trigger complex workflows using a planner/executor/critic model.
- **Reference:** `src/mvp/agent_registry.py`

---

## Plugin System (MCP Tools)

VERN's plugin system is built on the **Multi-Agent Communication Protocol (MCP)**. All external actions (e.g., file operations, API calls) are exposed as "tools" that agents can call.

- **Registration:** Tools are registered using the `@mcp.tool()` decorator in `src/mvp/mcp_server.py`.
- **Discovery:** The plugin registry (`src/mvp/plugin_registry.py`) dynamically discovers all registered tools, making them available to agents and the GUI.
- **Legacy Plugins:** The old plugin system in `src/plugins/` is deprecated. All new functionality should be implemented as MCP tools.

### Available Toolsets
- **`fileops`**: Secure file listing and reading.
- **`chromadb_query`**: Document and knowledge retrieval.
- **`get_weather`**: Real-time weather data via OpenWeatherMap.
- **`calendar`**: Google Calendar integration.

---

## Onboarding and Best Practices

- **New Agents:** If you are creating a new agent, start by reviewing `PROJECT_OVERVIEW.md` and `CONTRIBUTING.md`.
- **Documentation:** Keep your agent's guide in this directory updated. Document its purpose, prompts, context handling, and any specific behaviors.
- **Diagrams:** Use ASCII art in Markdown code blocks for diagrams, and add a descriptive caption. This ensures they are accessible and easily updated.

## See Also

- [README.md](../README.md)
- [PROJECT_OVERVIEW.md](../PROJECT_OVERVIEW.md)
- [QUICKSTART.md](../QUICKSTART.md)
- [SECURITY_AND_GIT_GUIDELINES.md](../SECURITY_AND_GIT_GUIDELINES.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
