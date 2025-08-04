# Agent Guides

## Backend Selection & Resource Awareness

- All agent backends (ASR, TTS, vision, LLM) are optional and configurable in `config/agent_backends.yaml`.
- Heavy libraries (Whisper, Coqui, etc.) are NOT required. You can select lightweight or stub backends.
- Agents check available resources before loading any backend, and fall back to stubs or lightweight alternatives if needed.
- Example config for low-resource setup:
  ```yaml
  default_asr: espeak-asr
  default_tts: espeak-tts
  default_vision: tesseract
  ```
- No forced installs. Use only the models/APIs you already have.
- See README.md for more details on backend options and resource requirements.


This directory contains guides and reference docs for building, testing, and integrating agents and plugins in VERN.

---

## 🧠 Memory API (Knowledge Graph & Semantic Search)

VERN exposes a memory subsystem for agents/plugins via FastAPI endpoints.  
**Default is in-memory or file-based graph storage for resource-constrained setups.**  
If Neo4j is available and configured, it will be used; otherwise, agents/plugins will fall back automatically.

- Backend selection is controlled by the `VERN_MEMORY_BACKEND` environment variable (`memory` or `neo4j`).
- Health checks and warnings are logged if Neo4j is referenced but not available.
- Agents/plugins should always interact with the unified memory API, not directly with any backend.

Endpoints:

- `POST /memory/entity` — Add entity (`entity_id`, `properties`)
- `GET /memory/entity/{entity_id}` — Get entity
- `PUT /memory/entity/{entity_id}` — Update entity (`properties`)
- `DELETE /memory/entity/{entity_id}` — Delete entity

- `POST /memory/relationship` — Add relationship (`source_id`, `target_id`, `rel_type`, `properties`)
- `GET /memory/relationship/{entity_id}` — Get relationships for entity

- `POST /memory/event` — Add event (`entity_id`, `event_type`, `properties`)
- `GET /memory/event/{entity_id}` — Get events for entity

### Example: Add an entity

```bash
curl -X POST http://localhost:8000/memory/entity \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "user_1", "properties": {"name": "Alice", "role": "admin"}}'
```

### Example: Add a relationship

```bash
curl -X POST http://localhost:8000/memory/relationship \
  -H "Content-Type: application/json" \
  -d '{"source_id": "user_1", "target_id": "project_42", "rel_type": "works_on"}'
```

### Example: Add an event

```bash
curl -X POST http://localhost:8000/memory/event \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "user_1", "event_type": "login"}'
```

See `vern_backend/app/memory.py` for API details and usage patterns.

---

### 🧠 Vector Memory API (Semantic Search)

---

### 🧠 RAG API (Document Retrieval, Haystack)

---

### 🤖 Multi-Agent Orchestration API (Planner/Executor/Critic)

---

### 🔒 Privacy Agent API

---

### 🔗 Protocols: MCP/A2A, REST, gRPC

---

### 🖥️ Multimodal Agents: Voice & Vision

- Voice Agent: ASR (speech-to-text) via `transcribe_audio`, TTS (text-to-speech) via `synthesize_speech`
- Vision Agent: Image analysis via `analyze_image`, document OCR via `extract_text_from_document`

#### Example: Voice agent

```python
from src/mvp.voice_agent import transcribe_audio, synthesize_speech
text = transcribe_audio(b"...")  # returns "Transcribed text (stub)"
audio = synthesize_speech("Hello world")  # returns b"audio-bytes-stub"
```

#### Example: Vision agent

```python
from src/mvp.vision_agent import analyze_image, extract_text_from_document
result = analyze_image(b"...")  # returns {"caption": "...", "labels": [...]}
text = extract_text_from_document(b"...")  # returns "Extracted text (stub)"
```

#### Visual Workflow Scripting

- Visual workflow editor (Node-RED/n8n style) planned for future release.
- Agents, plugins, and multimodal steps will be scriptable via drag-and-drop UI.

See `src/mvp/voice_agent.py` and `src/mvp/vision_agent.py` for agent API details and extension patterns.

---

- MCP/A2A: Inter-agent and plugin messaging protocol (`handle_mcp_message`)
- REST: All FastAPI endpoints are RESTful and documented above
- gRPC: Agent/plugin interoperability via `handle_grpc_request` (stub)

#### Example: MCP message

```python
from src.mvp.protocols import handle_mcp_message
resp = handle_mcp_message({"type": "call_tool", "tool": "weather", "params": {"location": "Austin"}})
print(resp)
```

#### Example: gRPC request

```python
from src.mvp.protocols import handle_grpc_request
resp = handle_grpc_request({"method": "AgentService/Call", "payload": {"agent": "planner"}})
print(resp)
```

See `src/mvp/protocols.py` for protocol handler details and extension patterns.

---

- `POST /privacy/check_permission` — Check permission for sensitive actions (`action`, `user_id`, `data`)
- `POST /privacy/sanitize` — Sanitize sensitive data (`data`)
- `GET /privacy/audit_log` — Retrieve audit log of agent actions

#### Example: Check permission

```bash
curl -X POST http://localhost:8000/privacy/check_permission \
  -H "Content-Type: application/json" \
  -d '{"action": "send_email", "user_id": "user_1", "data": {"email": "alice@example.com", "ssn": "123-45-6789"}}'
```

#### Example: Sanitize data

```bash
curl -X POST http://localhost:8000/privacy/sanitize \
  -H "Content-Type: application/json" \
  -d '{"data": {"email": "alice@example.com", "ssn": "123-45-6789", "credit_card": "4111111111111111"}}'
```

#### Example: Get audit log

```bash
curl http://localhost:8000/privacy/audit_log
```

See `src/mvp/privacy_agent.py` for privacy agent details and extension patterns.

---

- `POST /agents/orchestrate` — Orchestrate a task using planner/executor/critic agents (`task`, optional `context`)

#### Example: Orchestrate a workflow

```bash
curl -X POST http://localhost:8000/agents/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"task": "Plan a trip", "context": {}}'
```

Returns:
```json
{
  "steps": ["Step for: Plan a trip"],
  "results": ["Executed: Step for: Plan a trip"],
  "critiques": ["Critique: Executed: Step for: Plan a trip"]
}
```

See `src/mvp/agent_registry.py` for orchestration details and agent role templates.

---

- `POST /rag/add` — Add documents to RAG memory (`docs`, optional `meta`)
- `GET /rag/query` — Query RAG memory (`query`, optional `top_k`)

#### Example: Add documents

```bash
curl -X POST http://localhost:8000/rag/add \
  -H "Content-Type: application/json" \
  -d '{"docs": ["VERN supports RAG", "Agents use Haystack"], "meta": [{"type": "info"}, {"type": "tech"}]}'
```

#### Example: Query RAG memory

```bash
curl "http://localhost:8000/rag/query?query=RAG%20support&top_k=2"
```

See `vern_backend/app/rag.py` for API details and usage patterns.

---

- `POST /vector_memory/add` — Add documents to semantic memory (`docs`, optional `metadata`)
- `GET /vector_memory/query` — Query semantic memory (`text`, optional `top_k`)

#### Example: Add documents

```bash
curl -X POST http://localhost:8000/vector_memory/add \
  -H "Content-Type: application/json" \
  -d '{"docs": ["VERN is modular", "Agents collaborate"], "metadata": [{"type": "info"}, {"type": "team"}]}'
```

#### Example: Query semantic memory

```bash
curl "http://localhost:8000/vector_memory/query?text=collaborate&top_k=3"
```

See `vern_backend/app/vector_memory.py` for API details and usage patterns.

---
All agents must escalate errors to the orchestrator for robust fallback. See src/mvp/health_wellness.py and src/mvp/knowledge_broker.py for templates. Document escalation logic in your agent guide.

## Diagram/Image Workflow for Docs

To add diagrams or visuals in VERN documentation (for non-image editors):

```text
+-------------------+      +-------------------+
|   Frontend (GUI)  |<---->|   Backend (API)   |
+-------------------+      +-------------------+
         |                        |
         v                        v
   [User Actions]           [Agent Logic]
```

*Diagram: High-level VERN architecture showing the frontend and backend interaction, with user actions routed to agent logic.*

- Write diagrams in Markdown code blocks using ASCII/text.
- Add a clear, concise text description below each diagram.
- Optionally add `<!-- TODO: Convert to SVG/PNG for docs -->` for future contributors.
- When ready, convert ASCII diagrams to SVG/PNG using tools like Excalidraw, Mermaid, draw.io, or AI image generators.
- Replace or supplement the code block with the image, keeping the text description for accessibility.

This workflow ensures visuals are accessible, editable, and convertible for production docs.

Welcome to the VERN Agent Guides!  
This directory contains documentation and prompts for each agent cluster, as well as general onboarding and extension instructions.

---

## Import Hygiene & Troubleshooting

- All Python imports in VERN use absolute paths from the project root (e.g., `from src.db.logger import ...`, `from src.mvp.llm_router import ...`).
- Relative imports (e.g., `from db.logger import ...` or `from mvp.llm_router import ...`) are not supported and will cause import errors.
- Before starting the backend, run the import self-test script to check for broken imports:
  ```
  python scripts/check_imports.py
  ```
- If you see `[ERROR]` lines, fix the import paths to use the `src.` prefix and match the project structure.
- If you see `ModuleNotFoundError` or `ImportError`, ensure you have installed all dependencies:
  ```
  pip install -r requirements.txt
  ```
- For more troubleshooting, see the README.md and QUICKSTART.md.

---

## Dashboard & Onboarding Test Coverage (2025)

- Frontend integration tests now cover dashboard, onboarding, help, feedback, and notification panels.
- Onboarding checklist logic is robust and tested.
- All documentation (README, QUICKSTART, TASKS_AND_TODO) is synced after each sprint.
- See those docs for details on UI/UX, onboarding, and test coverage.

---

## Beast Mode Doc Protocol

> **VERN Beast Mode Doc Protocol**
>
> 1. **Recursive, Context-Driven:** Always read and preserve all relevant docs before editing. Never overwrite blindly. Never truncate with “remains unchanged”—always show full, updated context.
> 2. **Sync Code, Docs, and Context:** After every confirmed change, update all relevant docs, task lists, and changelogs. Cross-link updates and checkpoint context.
> 3. **Onboarding First:** Assume the reader is new. Every doc must enable a new user (coder or not) to get started, understand the "why," and contribute safely.
> 4. **Transparency & Auditability:** Log every major change, decision, and lesson in CHANGELOG.md and TASKS_AND_TODO.md. Reference related issues, PRs, and docs for traceability.
> 5. **No Stale or Misleading Docs:** Remove or clearly mark legacy patterns. If a feature is deprecated or planned, say so explicitly.
> 6. **Architecture & Workflows:** Include diagrams, sample workflows, and real-world use cases. Show how agents, plugins, and tools interact.
> 7. **Testing & CI/CD:** Document all tests, coverage, and CI/CD setup. Every new feature or fix must include tests and doc updates.
> 8. **Security & Privacy:** Never commit secrets. Use `.env.example` and document all config. Reference SECURITY_AND_GIT_GUIDELINES.md in every onboarding doc.
> 9. **Accessibility & Internationalization:** Maintain a checklist and status for accessibility and language support.
> 10. **Extension & Marketplace:** Document how to add agents, plugins, and UI panels. Maintain a roadmap for the plugin marketplace and third-party contributions.
> 11. **Continuous Review:** After each sprint or major change, checkpoint context, review all docs, and update as needed. Never end a sprint with stale docs.
> 12. **Human-AI Partnership:** All docs should reinforce VERN’s mission: context-driven, ethical, accessible, and open to all.

---

## Cluster/Agent Onboarding & Self-Check

If you are a new agent (AI or human) or need to re-orient:

- **Read [PROJECT_OVERVIEW.md](../PROJECT_OVERVIEW.md)** for the big picture and cluster/team structure.
- **Review [TASKS_AND_TODO.md](../TASKS_AND_TODO.md)** for the current sprint, blockers, and context.
- **Summarize the current cluster goal** before acting or making changes.
- **Update TASKS_AND_TODO.md** after each confirmed change.
- **If unsure, ask for review or clarification before proceeding.**
- **Review [SECURITY_AND_GIT_GUIDELINES.md](../SECURITY_AND_GIT_GUIDELINES.md) before handling any code, config, or API keys.**
- **For contributing, see [CONTRIBUTING.md](../CONTRIBUTING.md).**

---

## Agent Cluster Structure

- Each cluster (Dev, Admin, Research, etc.) has its own guide and prompt file.
- Clusters are modular and can be extended or swapped as needed.
- See each `AGENT_GUIDES/<CLUSTER>.md` for role-specific info and prompts.

---

## Adding or Updating Agents/Clusters

1. Add a new Python module in `src/mvp/` for your agent/cluster.
2. Create or update the corresponding guide in `AGENT_GUIDES/`.
3. Register new tools in `src/mvp/mcp_server.py` using `@mcp.tool()`.
4. Update documentation and tests as needed.
5. **To add LLM-powered reasoning to an agent:**
   - Add a response function that calls the LLM (see `src/mvp/orchestrator.py` for an example).
   - Pass recent chat history, agent status, and relevant context to the LLM.
   - Document the agent’s prompt, context, and tool-calling logic in the cluster guide.

---

## Multi-Agent Orchestration & Delegation

- The Orchestrator agent uses the LLM to decide which clusters and plugins to involve for any user input.
- Sub-tasks are delegated to relevant clusters and plugins, which each use their own LLM-powered logic and tools.
- Results are aggregated and summarized for the user.
- All agent modules are modular and extensible for future plugins and new clusters.

---

## Modular LLM Provider/Model Selection

- **Config-driven:**  
  - LLM provider/model selection is now driven by `config/agent_backends.yaml`.
  - The LLM router (`src/mvp/llm_router.py`) reads the config and routes agent calls to the selected backend/model.
  - GUI shows current model/provider and instructs how to change.
- **How to change models/providers:**  
  - Edit `config/agent_backends.yaml` to set the default backend/model.
  - Supported: Ollama (local), OpenAI (cloud, planned), fake_llm (testing), and more.
  - See QUICKSTART.md for details.

---

## Plugin API & Tool-Calling

- **MCP Tools:**  
  - All tools are now registered via MCP-compatible `@mcp.tool()` decorators in `src/mvp/mcp_server.py`.
  - Legacy plugins in `src/plugins/` are deprecated and should not be modified.
  - Agents and orchestrator call tools via MCP protocol for real-world actions.
- **Sample MCP tools:**  
  - Weather (`get_weather`), calendar (`add_event`, `list_events`), fileops (`fileops_list_files`, `fileops_read_file`), chromadb (`chromadb_query`: document/knowledge retrieval).

---

### Plugin Registry & Marketplace (Dynamic Discovery)

- **Dynamic Discovery:**  
  - All MCP tools are now dynamically discovered via the plugin registry (`src/mvp/plugin_registry.py`).
  - The GUI "Tools/Plugins" page lists all available tools with descriptions, using the registry.
  - No more hardcoded tool lists—new tools appear automatically after registration.
- **Metadata:**  
  - Each tool includes name, description (from docstring), and enabled/disabled state.
  - Future: add author, version, tags, and admin controls.
- **Admin Controls:**  
  - Enable/disable tools per session in the GUI.
  - Future: persist enable/disable state, allow admin-only registration/removal.
- **Marketplace Roadmap:**  
  - Foundation is laid for a future plugin marketplace with third-party contributions, approval, and install.
  - Contributors will be able to submit plugins/tools for review and inclusion.
- **See also:** `src/mvp/plugin_registry.py`, `src/mvp/gui.py`

---

### ChromaDB Plugin (`chromadb_query`)

- **Integration:** Uses ChromaDB Python client for document/knowledge retrieval.
- **Config:** Requires `CHROMA_DB_PATH` in your `.env` file (default: `./chroma_data/`).
- **Usage:** 
  - `chromadb_query(query: str, top_k: int = 3)` returns top matching documents for a query string.
- **Pipeline:** Loads ChromaDB client, queries the "vern_docs" collection, returns top results.
- **Error Handling:** Robust error messages for missing config, DB errors, or no results.
- **Example .env:**
  ```
  CHROMA_DB_PATH=./chroma_data/
  ```
- **Example Output:**
  ```
  Document 1 text...

  Document 2 text...

  Document 3 text...
  ```
- **See also:** `src/mvp/mcp_server.py`, `.env.example`, `requirements.txt`

---

### Fileops Plugin (`fileops_list_files`, `fileops_read_file`)

- **Integration:** Secure, sandboxed file operations under the project root.
- **Usage:** 
  - `fileops_list_files(directory: str)` lists files in a directory (relative to project root).
  - `fileops_read_file(path: str)` reads a file (relative to project root).
- **Security:** 
  - All paths are resolved and validated to prevent directory traversal.
  - Access outside the project root is denied.
  - Only files and directories under the project root are accessible.
- **Error Handling:** Robust error messages for invalid paths, access violations, or file errors.
- **Example Output:**
  ```
  ['README.md', 'requirements.txt', 'src', ...]
  Error reading file: [Errno 2] No such file or directory: 'notfound.txt'
  Access denied: file traversal outside project root.
  ```
- **See also:** `src/mvp/mcp_server.py`

---

### Calendar Plugin (`add_event`, `list_events`)

- **Integration:** Uses Google Calendar API for real event creation and listing.
- **Config:** Requires `GOOGLE_CALENDAR_ID` and a service account JSON file (path set in `GOOGLE_CALENDAR_CREDENTIALS_JSON`) in your `.env` file.
- **Usage:** 
  - `add_event(title: str, date: str)` creates an event on the configured calendar.
  - `list_events()` lists upcoming events.
- **Pipeline:** Loads credentials, calls Google Calendar API, formats output.
- **Error Handling:** Robust error messages for missing config, invalid credentials, or API/network errors.
- **Example .env:**
  ```
  GOOGLE_CALENDAR_ID=your-calendar-id-here
  GOOGLE_CALENDAR_CREDENTIALS_JSON=google_calendar_service_account.json
  ```
- **Example Output:**
  ```
  Event 'Team Sync' added for 2025-08-01. Google Event ID: abc123xyz
  2025-08-01: Team Sync
  ```
- **See also:** `src/mvp/mcp_server.py`, `.env.example`, `requirements.txt`

---

### Weather Plugin (`get_weather`)

- **Integration:** Uses OpenWeatherMap API for real-time weather data.
- **Config:** Requires `OPENWEATHERMAP_API_KEY` in your `.env` file.
- **Usage:** Call `get_weather(location: str)` with a city or region name.
- **Pipeline:** Geocodes city name to lat/lon, fetches weather, formats output.
- **Error Handling:** Robust error messages for missing API key, invalid location, or network/API errors.
- **Example .env:**
  ```
  OPENWEATHERMAP_API_KEY=your-openweathermap-key-here
  ```
- **Example Output:**
  ```
  Weather for Austin, US:
  - Clear sky
  - Temperature: 32°C
  - Humidity: 40%
  - Wind speed: 2.5 m/s
  ```
- **See also:** `src/mvp/mcp_server.py`, `.env.example`, `requirements.txt`

- **How to add tools:**  
  - Add a Python function with an `@mcp.tool()` decorator to `src/mvp/mcp_server.py`.
  - See QUICKSTART.md for details.

---

## RAG/Document Retrieval

- **ChromaDB plugin:**  
  - Stores and searches documents/knowledge.
  - Research agent and orchestrator use it for doc/knowledge search.

---

## Persona Tuning

- **Health/Wellness agent:**  
  - Supports multiple personas (default, coach, medic, mindfulness).
  - Pattern can be extended to other agents.

---

## Agent Protocol: Logging, Persona/Context, Error Handling

- All agent clusters must:
  - Log every action and LLM/tool call using `log_action`, `log_message`, and `log_gotcha` (see `src/db/logger.py`).
  - Accept and use persona/context parameters for adaptive, user-specific responses.
  - Implement robust error handling and escalation stubs (escalate to orchestrator/emergent agent on failure).
  - Document persona/context handling and escalation logic in the cluster guide.
  - Keep code, docs, and context in sync after every change.

- See any refactored agent in `src/mvp/` for a template.

## Best Practices

- Keep guides and prompts up to date with code and workflow changes.
- Use clear, descriptive language—assume the reader is new to the project.
- Document any gotchas, caveats, or lessons learned in the relevant guide.
- Reference [KNOWN_ISSUES_AND_GOTCHAS.md](../KNOWN_ISSUES_AND_GOTCHAS.md) for system-wide caveats.
- **For LLM-powered agents:**  
  - Document how context is passed and managed.
  - Describe fallback/error handling for LLM failures.
  - Note how tool-calling is triggered from LLM plans (if implemented).

## Dashboard Panels & Onboarding

- **Config Editor Panel:** Edit `.env` and YAML config files, with validation and error feedback.
- **Workflow Editor Panel:** Build, visualize, and run multi-agent workflows.
- **Plugin Marketplace Panel:** Enable, disable, update, and remove plugins; submit new plugins for review.
- **Onboarding Panel:** Step-by-step checklist, persona/profile setup, tooltips, and direct links to docs/help.
- **Help Panel:** Troubleshooting steps, FAQ, and links to docs/videos for non-coders.
- **Feedback Panel:** Submit feedback and bug reports.
- **Notification Panel:** Real-time notifications and error alerts.

**Troubleshooting:**  
- Use the Help panel for common issues and FAQ.
- For onboarding, follow the checklist and use tooltips/links for guidance.
- If stuck, submit feedback or join the community for support.

## See Also

- [README.md](../README.md)
- [PROJECT_OVERVIEW.md](../PROJECT_OVERVIEW.md)
- [QUICKSTART.md](../QUICKSTART.md)
- [TASKS_AND_TODO.md](../TASKS_AND_TODO.md)
- [MVP_IMPLEMENTATION_PLAN.md](../MVP_IMPLEMENTATION_PLAN.md)
- [KNOWN_ISSUES_AND_GOTCHAS.md](../KNOWN_ISSUES_AND_GOTCHAS.md)
- [SECURITY_AND_GIT_GUIDELINES.md](../SECURITY_AND_GIT_GUIDELINES.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
