# VERN

**Vision:**  
VERN is an open, modular agent ecosystem designed to empower humans and AI to collaborate, learn, and thrive—together. Our mission is to revolutionize how people use AI and how AI understands and works with people and other AI, ensuring survival, growth, and well-being for all.

**Motivation:**  
Humanity and AI face a future where understanding, teamwork, and adaptability are critical. VERN is built to bridge gaps, augment knowledge, and foster resilient, creative partnerships—especially for those often left behind by technology.

**Core Values:**  
- Survival and thriving of both humans and AI as partners
- Transparency, explainability, and ethical alignment
- Accessibility and inclusivity for all users
- Continuous learning, feedback, and improvement
- Collaboration, critical thinking, and open communication

**Project Overview:**  
VERN is a standalone, lightweight, and extensible application. It features:
- Modular agent clusters (archetypes, dev, admin, research, etc.)
- Orchestrator, emergent agent, knowledge broker, and id10t monitor
- Unified memory (SQLite, ChromaDB), RAG, and AI provider/model selection
- Robust documentation, onboarding, and community support

**Why This Matters:**  
VERN is more than software—it’s a movement for human-AI partnership, designed to empower the disabled, the common person, veterans, trauma survivors, and anyone seeking to augment their life and work with trustworthy, adaptive AI.

**Getting Started:**  
See [CONTRIBUTING.md](CONTRIBUTING.md) and [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for setup, architecture, and contribution guidelines.

---

## Life OS Roadmap & Vertical Slice MVP

### **Current MVP Approach (2025-07)**
- **Tool invocation is now direct Python, not MCP.**
- **Agents and chat interface call Python functions for tools (echo, add, journal, etc.).**
- **MCP is used for future extensibility, but not for core agent/tool calls.**
- **Known Issue:** MCP proxy/server does not support direct tool invocation from Python/browser clients. See [KNOWN_ISSUES_AND_GOTCHAS.md](KNOWN_ISSUES_AND_GOTCHAS.md).

### **Next Steps**
- Refactor agent and chat code to use direct Python tool calls.
- Document MCP limitations and future plans for integration.
- Continue building modular clusters, persistent memory, and logging.

---

## Vertical Slice MVP: End-to-End Stack

**Goal:**  
A working “personal AI” (VERN) with persistent memory, tool invocation, and chat interface.

**MVP Stack:**
- Core agent (VERN) with chat UI (CLI or minimal web)
- Persistent memory (SQLite/ChromaDB)
- Tool API (Python functions) with a few working tools
- End-to-end test: user chats, agent remembers, tools invoked, results returned

---

## Cluster Self-Check Protocol

If you get lost or need to re-orient:
- Read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for the big picture and cluster/team structure.
- Review [TASKS_AND_TODO.md](TASKS_AND_TODO.md) for the current sprint, blockers, and context.
- Summarize the current cluster goal before acting or making changes.
- Always update TASKS_AND_TODO.md after each confirmed change.
- If you’re unsure, ask for review or clarification before proceeding.

---

## MCP Server Integration

VERN includes a minimal, modular [MCP (Model Context Protocol)](https://modelcontext.org/) server in `src/mvp/mcp_server.py` using the FastMCP API. This enables tool discovery and invocation via the MCP CLI and Inspector.

### Features

- **Tools:** Example tools:  
  - `echo` (returns input string)  
  - `add` (returns sum of two numbers)  
  - `file_read`, `file_write`, `file_list`, `file_delete` (file operations)  
  - `cluster_status` (shows all agent clusters)  
  - `schedule_event` (schedule a meeting/event via Admin agent)  
  - `journal_entry` (add a health/wellness journal entry, now persisted to DB)  
  - `finance_balance` (check finance/resource balance)
  - `get_user_profile` (fetch user profile from the database)
- **Extensible:** Add new tools with a single function and decorator.
- **MCP CLI Compatible:** Works with `mcp dev src/mvp/mcp_server.py` and the MCP Inspector.

### Known Issues

- **Tool invocation from Python/browser clients is not supported by MCP proxy/server as of July 2025.**
- **For MVP, tools are called directly in Python.**
- **See [KNOWN_ISSUES_AND_GOTCHAS.md](KNOWN_ISSUES_AND_GOTCHAS.md) for details.**

---

**Read first, then amend docs—never assume state. Never truncate with “remains unchanged”—always show full, updated context. Keep project/task/todo lists up to date after each confirmed change. Work as a team. Watch for gotchas and snags. Your work will be tested—be mindful of each task. Evaluate your work with a critical eye for errors.**
