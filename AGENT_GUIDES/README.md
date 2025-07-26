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
