# VERN Agent Guides

This directory contains guides, prompts, and configuration for all VERN agents.

---

## LLM Backend Modularity

- Each agent can use a different LLM backend/model, configured in `config/agent_backends.yaml`.
- Supported backends:
  - `ollama-<model>` (e.g., `ollama-qwen3:0.6b`, `ollama-phi`)
  - `fake_llm` (for testing)
  - `qwen3-0.6b` (direct transformers integration)
  - More can be added by writing a wrapper and updating `llm_router.py`.

### How to Add or Change an Agent's LLM Backend

1. Edit `config/agent_backends.yaml` and set the backend for your agent.
2. If using a new backend, add a wrapper in `src/mvp/` and update `llm_router.py`.
3. Test with the agent CLI or automated tests.

---

## Agent Tool-Calling (NEW)

- Agents and the orchestrator can call modular tools via a shared registry (`src/mvp/tool_interface.py`).
- Tools are Python classes with a name, description, and a `call(params)` method.
- Example tools: `echo`, `add` (see registry for details).
- To call a tool manually, use the CLI option "Call a tool (orchestrator)" and provide the tool name and parameters.
- To add a new tool: define a function, add it to the registry in `tool_interface.py`, and document its usage.

### MCP Tools for Clusters (via MCP Server)

- `schedule_event`: Schedule a meeting/event via the Admin agent.
- `journal_entry`: Add a health/wellness journal entry via the HealthWellness agent (now persisted to DB).
- `finance_balance`: Check finance/resource balance via the FinanceResource agent.
- `get_user_profile`: Fetch a user profile from the database for context-aware actions.
- See the main [README.md](../README.md) for full tool list and usage instructions.

---

## Agent Guide Index

- [ADMIN.md](ADMIN.md)
- [DEV_TEAM.md](DEV_TEAM.md)
- [RESEARCH.md](RESEARCH.md)
- [KNOWLEDGE_BROKER.md](KNOWLEDGE_BROKER.md)
- [HEALTH_WELLNESS.md](HEALTH_WELLNESS.md)
- [LEARNING_EDUCATION.md](LEARNING_EDUCATION.md)
- [SOCIAL_RELATIONSHIP.md](SOCIAL_RELATIONSHIP.md)
- [SECURITY_PRIVACY.md](SECURITY_PRIVACY.md)
- [ENVIRONMENT_SYSTEMS.md](ENVIRONMENT_SYSTEMS.md)
- [LEGAL_COMPLIANCE.md](LEGAL_COMPLIANCE.md)
- [CREATIVITY_MEDIA.md](CREATIVITY_MEDIA.md)
- [CAREER_WORK.md](CAREER_WORK.md)
- [TRAVEL_LOGISTICS.md](TRAVEL_LOGISTICS.md)
- [ORCHESTRATOR.md](ORCHESTRATOR.md)
- [EMERGENT_AGENT.md](EMERGENT_AGENT.md)
- [ID10T_MONITOR.md](ID10T_MONITOR.md)

---

## See Also

- [QUICKSTART.md](../QUICKSTART.md) for setup and backend installation.
- [MVP_IMPLEMENTATION_PLAN.md](../MVP_IMPLEMENTATION_PLAN.md) for architecture and extensibility.
- [KNOWN_ISSUES_AND_GOTCHAS.md](../KNOWN_ISSUES_AND_GOTCHAS.md) for backend/model caveats.
