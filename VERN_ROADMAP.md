# VERN Technical Roadmap (2025+)

This roadmap lays out the step-by-step technical plan for building VERN into a truly effective, extensible, user-empowering "life OS". It supersedes and clarifies previous plans where conflicts exist.

---

## Phase 1: Foundation

1. **Plugin System Hardening**
   - Refactor plugin execution to use sandboxing (subprocesses, containers, restricted interpreters)
   - Define and enforce secure, versioned plugin APIs
   - Implement plugin registry with signed metadata and audit logging
   - Build admin review and automated static analysis workflow
   - Update documentation for plugin development and security

2. **Agent Cluster Expansion**
   - Define specs and guides for new agent clusters: Writing, Research, Presentation, Insight
   - Implement agent classes and workflows for each domain
   - Integrate agents with orchestrator, memory, and plugin system
   - Register new plugins and write tests

3. **Unified UI**
   - Design dashboard with sidebar navigation (Agents, Workflows, Plugins, Integrations, Feedback, Help, Onboarding)
   - Refactor existing panels into dashboard modules
   - Build workflow builder (drag-and-drop) and onboarding wizard
   - Centralize notifications, feedback, and plugin management
   - Test with non-coders and iterate

4. **Cloud API Connectors**
   - Scaffold connector base class and protocol handlers (OAuth2, REST, etc.)
   - Build registry and configuration management
   - Implement sample connectors (Google, finance, health, device APIs)
   - Integrate with FastAPI endpoints and MCP Tool API
   - Add tests and documentation

5. **User Profile, Feedback, Adaptation**
   - Extend DB schema: user_profiles, feedback, adaptation_events
   - Refactor APIs to support feedback and adaptation signals
   - Log adaptation events and update agent workflows
   - Enhance frontend panels for personalization and feedback

---

## Phase 2: Memory & Learning

6. **Full RAG & Semantic Memory**
   - Upgrade memory system for retrieval-augmented generation (RAG)
   - Implement semantic search and long-term logs
   - Integrate agent/user learning via feedback loops and adaptation

7. **Privacy & Transparency**
   - Add transparent logging and privacy controls
   - Document all learning/adaptation steps for auditability

---

## Phase 3: Empowerment & Extensibility

8. **Self-Modification & Workflow Editing**
   - Automate onboarding, setup, and modification via VERN itself
   - Build self-modification and workflow editing tools
   - Prepare for community contributions and agent/plugin marketplace

---

## Phase 4: Testing & Documentation

9. **Testing & Guides**
   - Build automated and manual test suites for all core flows
   - Write clear user guides and onboarding wizards

---

## Phase 5: Release & Iteration

10. **Release MVP**
    - Release for real-world use
    - Gather feedback, iterate, and expand agent capabilities

---

## References

- See [`FUTURE_VISION_AND_ROADMAP.md`](FUTURE_VISION_AND_ROADMAP.md), [`GOALS_AND_MILESTONES.md`](GOALS_AND_MILESTONES.md), [`TASKS_AND_TODO.md`](TASKS_AND_TODO.md) for historical context.
- This file is the authoritative technical roadmap. Update after each major milestone.
