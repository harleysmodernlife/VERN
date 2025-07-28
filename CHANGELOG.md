# VERN Changelog

**Read first, then amend docs—never assume state. Never truncate with “remains unchanged”—always show full, updated context. Keep this file up to date after each confirmed change. Work as a team. Watch for gotchas and snags. Your work will be tested—be mindful of each task. Evaluate your work with a critical eye for errors.**

**Major changes should align with the project’s long-term vision and design pillars—see [FUTURE_VISION_AND_ROADMAP.md](FUTURE_VISION_AND_ROADMAP.md) for context.**

---

## How to Use This File

- Log every significant change, decision, and lesson learned.
- Include date, description, and contributor (human or AI).
- Link related issues, PRs, and docs for traceability.

---

## Changelog

### 2025-07-27 [Python Tool Refactor, MVP CLI Agent+Tools, MCP Known Issues]

**Added**
- Refactored all tool invocation to direct Python functions (src/mvp/tool_interface.py).
- Updated CLI chat (src/mvp/cli.py) to call Python tools directly: echo, add, journal, schedule, finance, profile.
- Persistent memory and logging via SQLite remain unchanged.
- Updated README.md, TASKS_AND_TODO.md, and KNOWN_ISSUES_AND_GOTCHAS.md to document new MVP approach and MCP limitations.
- Added protocol for next steps and sprint planning in TASKS_AND_TODO.md.

**Changed**
- MCP is now used for future extensibility, not for core agent/tool calls.
- CLI chat no longer depends on MCP proxy/server or Inspector for tool invocation.
- Updated documentation to reflect new MVP architecture and workflow.

**Lessons**
- Direct Python tool calls enable a real agent+tools MVP even when MCP is not ready for Python/browser clients.
- Documenting limitations and protocol for next steps keeps the project on track and transparent.

---

### 2025-07-27 [Context Integration, Dashboard UI, and New MCP Tools]

**Added**
- MCP tools for agent/cluster actions: schedule_event (Admin), journal_entry (Health/Wellness, now persisted to DB), finance_balance (Finance/Resource), get_user_profile (fetch from DB)
- Context/memory integration: journal_entry logs to DB, get_user_profile reads from DB
- Minimal cockpit/dashboard UI prototype (vern_dashboard.html) for tool invocation and workflow management
- Integration tests for all new MCP tools (tests/test_mcp_server.py)

**Changed**
- Updated README.md and AGENT_GUIDES/README.md for new tools and context features
- Updated TASKS_AND_TODO.md for completed/ongoing and next sprint items

**Lessons**
- Exposing agent/cluster actions as MCP tools enables composability and UI integration
- Context/memory integration is key for Life OS workflows and persistent user experience

---

### 2025-07-25

- Initial documentation suite created: README.md, CONTRIBUTING.md, PROJECT_OVERVIEW.md, GOALS_AND_MILESTONES.md, TASKS_AND_TODO.md, VALUES_AND_GUIDELINES.md, COMMUNITY.md, CHANGELOG.md  
  *Contributor: Cline (AI)*

---

### 2025-07-26 [Horizontal Agent Scaffolding Complete]

**Added**
- Horizontally scaffolded and tested all remaining agents/clusters:
  - Research, Finance/Resource, Health/Wellness, Learning/Education, Social/Relationship, Environment/Systems, Legal/Compliance, Creativity/Media, Career/Work, Travel/Logistics, Archetype/Phoenix, Emergent Agent, id10t Monitor
- Automated test for all horizontal agent stubs (tests/test_agents_horizontal.py)

**Validated**
- All horizontal agent stubs pass automated tests and log to DB

**Changed**
- Updated QUICKSTART.md and TASKS_AND_TODO.md for horizontal agent coverage

**Lessons**
- Breadth-first scaffolding enables rapid integration, parallel development, and early pattern discovery

---

### 2025-07-26 [Agent Expansion, Cross-Cluster Handoff, and Test Coverage]

**Added**
- Knowledge Broker agent/cluster (src/mvp/knowledge_broker.py)
- Security/Privacy agent/cluster (src/mvp/security_privacy.py)
- CLI integration for both new agents
- Automated tests for Knowledge Broker and Security/Privacy (tests/test_agents_extended.py)
- Cross-cluster handoff logging and test (tests/test_cross_cluster_handoff.py)

**Validated**
- All new agent and handoff tests pass

**Changed**
- Updated QUICKSTART.md and TASKS_AND_TODO.md for new agents and tests

**Lessons**
- Cross-cluster handoff logging enables traceability and debugging for complex workflows

---

### 2025-07-25 [DB Logging Integration & Validation]

**Added**
- SQLite schema for core system logging (src/db/schema.sql)
- Logger API for actions, handoffs, gotchas, and logs (src/db/logger.py)
- DB init script (src/db/init_db.py)
- Automated DB logging test (tests/test_db_logging.py)
- Logger integration in MVP agents (Orchestrator, Dev Team, Admin)

**Validated**
- End-to-end DB logging with automated test and manual inspection

**Changed**
- Updated QUICKSTART.md and TASKS_AND_TODO.md for DB setup and status

**Lessons**
- Relative imports in agent files must be robust to working directory
- DB logging enables traceability and future analytics

---

### 2025-07-25 [MVP Validation & Docs Update]

**Added**
- Automated tests for MVP workflows (tests/test_mvp.py)
- Manual and automated test instructions to QUICKSTART.md
- Lessons learned and validation status to KNOWN_ISSUES_AND_GOTCHAS.md
- MVP validation and next steps to MVP_IMPLEMENTATION_PLAN.md

**Changed**
- TASKS_AND_TODO.md: Marked MVP implementation and testing tasks as complete

**Notes**
- MVP validated by both automated and manual testing. CLI and workflows match documentation.
- Ready for next phase: persistence, new clusters, onboarding improvements, and more complex scenarios.

---

**Keep this changelog current to ensure transparency and collective learning.**
