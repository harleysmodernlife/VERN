# VERN Task & TODO List (2025+)

---

## 🛠️ Sprint 1: Foundational Refactors & Modularization

- [x] **Prompt Utilities:** Build `src/mvp/prompt_utils.py` for all prompt construction. Refactor all agents to use it. Add unit tests.
- [x] **Error Handling/Escalation:** Centralize error escalation logic. Refactor LLM routing (`route_llm_call`) to return structured JSON errors. Standardize/rename logging functions (e.g., `log_gotcha` → `log_exception`).
- [x] **Context Processing:** Refactor context processor for robust nested data, add config flags for fine-tuning. Remove ad-hoc context handling.
- [x] **Modularization:** Extract redundant logic (logging, prompt assembly, escalation) into shared utilities. Update docs to reflect new structure.

---

## 🧠 Sprint 2: Memory System Integration

- [x] Memory subsystem scaffolded (FastAPI endpoints, in-memory graph, documented API). Agent clusters now integrated for persistent context/history.
- [x] Memory backend is now backend-agnostic (in-memory by default, Neo4j optional). Fallback logic and documentation in place for agents/plugins.
- [x] Update onboarding docs and usage examples for memory features.

---

## ⚡ Sprint 3: Asynchronous Support

- [x] Prototype async agent operations and LLM calls (using `asyncio`).
- [x] Implement sync wrappers for backward compatibility.
- [x] Refactor MCP client/server and agent orchestration for end-to-end async.
- [x] Document async patterns and migration steps.

---

## ✅ Sprint 4: Testing & CI/CD

- [x] Remove all legacy, Whisper, MCP, and plugin registry tests.
- [x] Scaffold new minimal test suite for core agent orchestration and LLM routing.
- [x] Ensure CI/CD pipeline runs only relevant tests for current codebase.
- [x] Update docs to reflect new test coverage and CI/CD setup.

---

## 🖥️ Sprint 5: Dashboard & Help Panel Improvements

- [x] Polish UI/UX and accessibility across all panels (Config Editor, Workflow Editor, Plugin Marketplace, Onboarding, Help).
- [x] Add demo mode instructions and troubleshooting tips for common issues (Docker, Neo4j, API keys).
- [x] Add more sample workflows and agent/plugin use cases to docs.
- [x] Update onboarding and help docs for new features.

---

## 🚀 Sprint 6: Advanced Features Prototyping

- [x] Visual workflow editor for drag-and-drop multi-agent scripting.
- [x] Real-time resource monitoring and auto-adaptation.
- [x] Advanced persona/context tuning for agents.
- [x] Document prototypes and integration patterns.

---

## 📚 Continuous Review & Documentation

- [x] After each sprint/refactor, update all relevant docs (README, TASKS_AND_TODO, AGENT_GUIDES, QUICKSTART, CHANGELOG).
- [x] Crosslink updates and checkpoint context.
- [x] Remove or mark legacy/deprecated patterns (Docker/Neo4j legacy code, old plugin registry).
- [x] Maintain onboarding-first, transparent, and accessible docs.

---

## 🏁 Sprint Checkpoint (August 2025)

- All roadmap steps complete: async, testing, health checks, CI/CD, dashboard polish, advanced features.
- Legacy patterns marked for removal (old Docker/Neo4j code, deprecated plugin registry).
- Docs, onboarding, and changelogs updated.
- Ready for next sprint: continuous review, extension, and onboarding-first improvements.


---

## 🗺️ Sprint Order & Dependencies

1. **Foundational Refactors & Modularization** (unblocks everything else)
2. **Memory System Integration** (enables persistent context/history)
3. **Async Support** (scales agent orchestration)
4. **Testing & CI/CD** (ensures reliability)
5. **Dashboard/Help Panel Improvements** (polish and accessibility)
6. **Advanced Features Prototyping** (future-proofing)

---

## 🧩 Mechanic/Plumber/Junkyard Builder Analogy

- **Refactor = Rewiring the electrical system:** Remove spaghetti wiring, install fuse box (shared utilities).
- **Memory Integration = Adding a logbook and sensors:** Track every job, wire up sensors for real-time feedback.
- **Async = Upgrading to smart relays:** Make the system responsive, no more waiting for one job to finish before starting the next.
- **Testing/CI = Pressure testing pipes:** Run water through every line, check for leaks, patch before the next job.
- **Dashboard = Upgrading the instrument panel:** Add gauges, warning lights, and clear instructions for every tool.
- **Advanced Features = Building a modular robot arm:** Prototype new attachments, test in the field, document for future mechanics.

---

## 📋 Full Todo List (Sprint Breakdown)

```
- [ ] Sprint 1: Refactor prompt utilities, error handling, context processing, and modularize shared logic.
- [ ] Sprint 2: Integrate memory subsystem with agent clusters, prototype graph backend, document patterns.
- [ ] Sprint 3: Implement async agent ops, LLM calls, MCP orchestration; add sync wrappers; document migration.
- [ ] Sprint 4: Expand unit/integration tests, CI/CD pipeline, health checks, error messages; update docs.
- [ ] Sprint 5: Polish dashboard panels, accessibility, demo mode, troubleshooting, sample workflows; update docs.
- [ ] Sprint 6: Prototype visual workflow editor, resource monitoring, persona/context tuning; document integration.
- [ ] Continuous: After each sprint, update all docs, crosslink changes, checkpoint context, remove legacy patterns.
```

---

## 🏁 Next Steps

- Begin with Sprint 1: Foundational Refactors & Modularization.
- After each sprint, checkpoint context and update all docs/task lists.
- Never assume state—always show full, updated context in docs and code.
