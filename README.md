# VERN Integration: User Profile, Feedback, and Adaptation Logic

## Summary of Changes

- **Database Schema:** Added `user_profiles`, `feedback`, and `adaptation_events` tables via migration.
- **Backend APIs:** Refactored endpoints for persistent user profiles, feedback, and adaptation event logging.
- **Agent Workflows:** Orchestrator now logs adaptation events and uses user profile/feedback data for personalization.
- **Frontend Panels:** UserProfilePanel and FeedbackPanel enhanced for editing preferences, submitting feedback, and displaying adaptation events.
- **Inline TODOs:** Added in backend and frontend files for future improvements (validation, richer UI, live updates).

## Onboarding, Setup, and Workflow Editing Enhancements (2025-08-08)

- **Onboarding Wizard:** Step-by-step onboarding guides users through environment setup, DB initialization, agent registration, plugin enable, and profile setup. See [`vern_frontend/components/OnboardingPanel.js`](vern_frontend/components/OnboardingPanel.js:1).
- **Backend Automation:** DB migrations run at startup. Agent registration and plugin enable endpoints are documented for automation. See inline TODOs in [`vern_backend/app/main.py`](vern_backend/app/main.py:54).
- **Workflow Editor:** Visual editor supports drag-and-drop, CRUD, and live preview. Inline TODOs for import/export, validation, and analytics. See [`vern_frontend/components/WorkflowEditorPanel.js`](vern_frontend/components/WorkflowEditorPanel.js:1).
- **Inline TODOs:** Major files updated with inline TODOs for future enhancements and automation.
## Memory & RAG Upgrade (2025-08-08)

- Extended [`vern_backend/app/memory.py`](vern_backend/app/memory.py:1) and [`vern_backend/app/vector_memory.py`](vern_backend/app/vector_memory.py:1) for RAG, semantic search, and long-term logs.
- Integrated RAG and semantic retrieval into agent workflows ([`vern_backend/app/agents.py`](vern_backend/app/agents.py:1)).
- Added unit tests for memory and agent integration ([`vern_backend/tests/test_memory_rag.py`](vern_backend/tests/test_memory_rag.py:1)).
- Inline TODOs added for future enhancements (hybrid retrieval, advanced filtering, external DB persistence).

## Next Steps

- Add richer validation and error handling for user profile and feedback forms.
- Implement live updates for adaptation events (websockets or polling).
- Expand agent workflow logic to leverage user preferences and feedback for deeper personalization.
- Write tests for new endpoints and UI components.
- Optimize database queries and add indices for performance.

See inline TODOs in code for specific enhancement ideas.

## Privacy Controls & Transparent Logging (2025-08-08)

- Privacy policy enforcement and compartmentalized audit logging added in [`vern_backend/app/privacy_policy.py`](vern_backend/app/privacy_policy.py:1) and [`vern_backend/app/utils_logging.py`](vern_backend/app/utils_logging.py:1).
- Frontend panels now display privacy status and allow users to view privacy audit trails ([`vern_frontend/components/OrchestratorPanel.js`](vern_frontend/components/OrchestratorPanel.js:1), [`vern_frontend/components/WorkflowLogsPanel.js`](vern_frontend/components/WorkflowLogsPanel.js:1)).
- Inline TODOs added for future privacy audits, consent management, and data export features.

**Next steps:**  
- Implement persistent audit log storage and filtering.  
- Add user consent management and data export endpoints.  
- Expand frontend privacy controls and audit filtering.

---

## MCP Plugin Runtime Model & Registry (2025-08-08)

### Current Runtime Model

- **Invocation:** MCP plugins are executed via stdio-based subprocess calls (Python CLI), not via HTTP or network bridge. Each plugin/tool call is routed through the MCP server using CLI arguments and subprocess isolation.
- **Security:** Plugins run in a sandboxed subprocess with resource limits and import whitelisting. No containerization or network isolation yet.
- **Registry/Discovery:** Plugins/tools are registered in the MCP registry, requiring admin review and approval before activation. Only approved plugins are enabled for execution.
- **Audit Logging:** All plugin registration, approval, and execution actions are logged to persistent audit logs (SQLite).
- **No HTTP Bridge:** There is currently no HTTP proxy/bridge for plugin invocation. All communication is local (stdio/subprocess).

### Contributor Notes & Future Plans

- **HTTP Proxy/Bridge:** Future phases will add an HTTP bridge for plugin invocation, enabling remote plugins and richer integration patterns.
- **Extending MCP Tooling:** To extend MCP tooling, add new tool definitions in [`src/mvp/mcp_server.py`](src/mvp/mcp_server.py:1) and register them in the plugin registry. All new plugins must pass admin review and signature verification.
- **Planned Enhancements:** Signature verification, static analysis, containerization, resource limits, and multi-admin workflows are planned. See inline TODOs in [`src/mvp/plugin_registry.py`](src/mvp/plugin_registry.py:1), [`src/mvp/plugin_tools.py`](src/mvp/plugin_tools.py:1), and [`src/mvp/plugin_sandbox.py`](src/mvp/plugin_sandbox.py:1).

See code comments in the above files for technical details and extension guidelines.
