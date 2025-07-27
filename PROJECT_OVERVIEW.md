# VERN Project Overview

## Architecture

VERN is a modular, agent-based system designed for adaptability, transparency, and teamwork. The architecture is organized into clusters, monitors, and shared services:

### Core Components

- **Agent Clusters:**  
  - *Archetype/Phoenix Cluster*: Human reasoning, values, synthesis  
  - *Dev Team Cluster*: Coding, debugging, automation  
  - *Admin Cluster*: Scheduling, file management, logistics  
  - *Research Cluster*: Information retrieval, summarization  
  - *Finance/Resource Cluster*: Budgeting, resource allocation  
  - *Health/Wellness Cluster*: Habit tracking, health data  
  - *Learning/Education Cluster*: Personalized learning, skill mapping  
  - *Social/Relationship Cluster*: Communication, event planning  
  - *Security/Privacy Cluster*: Threat monitoring, audits  
  - *Environment/Systems Cluster*: Device/system health, automation  
  - *Legal/Compliance Cluster*: Policy tracking, compliance  
  - *Creativity/Media Cluster*: Content creation, media management  
  - *Career/Work Cluster*: Job search, networking, performance  
  - *Travel/Logistics Cluster*: Trip planning, navigation  
  - *(Add more as needed)*

- **Orchestrator:** Integrates outputs, resolves conflicts, manages priorities.
- **Emergent Agent:** Scans for cross-cluster optimizations, creative solutions.
- **Knowledge Broker:** Checks memory/logs for existing answers before user queries.
- **id10t Monitor:** Sanity-checks actions for policy, stack, and convention adherence.

### Shared Services

- **Cluster & Agent Logs:**  
  - Each cluster maintains its own log (actions, errors, feedback) for transparency and local learning.
  - Sensitive data is compartmentalized; clusters only access what they need.
- **Unified Memory:**  
  - *SQLite*: Structured data, logs, user profiles  
  - *ChromaDB*: Semantic search, RAG, embeddings  
- **Configurable AI Providers:**  
  - API/local model selection, usage limits, and fallback options

### Communication

- **Message Bus:**  
  - Agents communicate via a unified bus (e.g., Python events, ZeroMQ, or similar)
- **Extensible Plugin System:**  
  Agents, clusters, and tools can be added or swapped modularly

- **MCP Tool API:**  
  VERN exposes a modular [MCP server](src/mvp/mcp_server.py) for tool discovery and invocation via the MCP CLI and Inspector.  
  See the "MCP Server Integration" section in README.md for usage and extension.

## System Flow

1. User input is routed to relevant cluster(s)
2. Cluster(s) process and output results
3. Orchestrator integrates and manages outputs
4. Emergent agent reviews for system-wide insights
5. Knowledge broker checks for existing info
6. id10t monitor sanity-checks actions
7. Final output/decision or user question is returned

## Stack Choices

- **Language:** Python (core, agents, plugins)
- **Databases:** SQLite, ChromaDB
- **Frontend/UI:** PySide6, Flask/FastAPI + HTMX, or minimal web UI
- **Containerization:** Docker (optional)
- **Testing:** Pytest, sample data, reproducible bug reports

## Principles

- Modular, open, and accessible by design
- Documentation and code must be kept up to date
- All contributors (human or AI) must follow project guidelines and critical reminders

## Context, Logging, and Learning

- **Cluster/Agent Context:**  
  Agents have access to their own logs and relevant cluster data, but not the full system state.
- **Escalation Protocols:**  
  When more context is needed, agents escalate to the Knowledge Broker or Orchestrator.
- **Learning:**  
  - Local: Each agent/cluster learns from its own logs and feedback.
  - System-wide: Orchestrator, Emergent Agent, and Knowledge Broker aggregate insights and update global strategies.
  - User Profile: Preferences, history, and feedback are stored in a profile DB, accessible as needed with privacy controls.
- **Transparency:**  
  All learning and adaptation steps are logged for debugging and improvement.

## Design Pillars & Roadmap

- **Interoperability:** Agents and clusters connect with diverse devices, platforms, and AIs.
- **Continuous Adaptation:** Agents red-team, self-improve, and stay up to date with new threats and discoveries.
- **Intentionality:** All actions align with user goals, values, and ethical principles.
- See [FUTURE_VISION_AND_ROADMAP.md](FUTURE_VISION_AND_ROADMAP.md) for long-term direction and open questions.

---

**Read first, then amend docs—never assume state. Never truncate with “remains unchanged”—always show full, updated context. Keep project/task/todo lists up to date after each confirmed change. Work as a team. Watch for gotchas and snags. Your work will be tested—be mindful of each task. Evaluate your work with a critical eye for errors.**
