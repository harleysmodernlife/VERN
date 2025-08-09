> **Note:** For document/image OCR, you must install Tesseract OCR on your system (not just the Python package).  
> Tesseract OCR must be installed on your operating system (not just in the project folder).  
> Other required system packages for VERN backend:
> - sqlite3 (database, usually pre-installed on Linux/Mac)
## Local Setup Guide

1. Install Python 3.10+ and Node.js 18+ on your system.
2. Clone the repo and run `python -m venv .venv && source .venv/bin/activate`.
3. Run `pip install -r vern_backend/requirements.txt`.
4. Install system packages:  
   - Ubuntu: `sudo apt-get install tesseract-ocr sqlite3`
   - Mac: `brew install tesseract sqlite3`
5. (Optional) Install Neo4j if you want graph features.
6. In `vern_frontend`, run `npm install` and `npm run build`.
7. Start backend: `uvicorn vern_backend.app.main:app --reload`
## Running with Docker Compose

1. Make sure Docker and Docker Compose are installed.
2. Run `docker compose up --build` from the project root.
3. This will build and start both backend and frontend containers.
4. All features (backend API, agents, config panel, workflows) will work the same as local setup.
5. To update config, use the frontend Config panel or edit files in the project and rebuild.
6. For Neo4j or other services, add them to `docker-compose.yml` as needed.
8. Start frontend: `npm start` in `vern_frontend`
9. Open the app in your browser and use the Config panel to set agent backends and options.
10. See QUICKSTART.md for troubleshooting tips.
> - tesseract-ocr (for OCR, already installed)
> - neo4j (if you use graph features, install Neo4j Community Edition)
> - Optional: ffmpeg (for audio/video processing in some agents)
> The Python code calls the system's `tesseract` executable, so it must be available in your PATH.  
> Example install commands:  
> - Ubuntu: `sudo apt-get install tesseract-ocr`  
> - Mac: `brew install tesseract`
> On Ubuntu: `sudo apt-get install tesseract-ocr`  
> On Mac: `brew install tesseract`
> **Note:** To avoid installing GPU/CUDA libraries, do not install torch or nvidia-* by default. For CPU-only PyTorch, use:
> `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu`
> See [`vern_backend/requirements.txt`](vern_backend/requirements.txt:1) and [`setup.py`](setup.py:1) for details.

---

## Troubleshooting: Accidental GPU/CUDA Package Installation

If you installed GPU/CUDA packages (e.g., torch with CUDA, nvidia-*), follow these steps to revert to CPU-only:

**1. Detect GPU/CUDA packages:**
- Run `pip list | grep -E 'torch|nvidia'` to check for GPU/CUDA packages.
- If `torch` shows a CUDA version (e.g., `torch 2.x.x+cu118`), or if you see `nvidia-*` packages, GPU/CUDA is installed.

**2. Uninstall GPU/CUDA packages:**
- Run:
  ```
  pip uninstall torch torchvision torchaudio nvidia-cublas-cu11 nvidia-cuda-runtime-cu11 nvidia-cudnn-cu11 nvidia-cufft-cu11 nvidia-curand-cu11 nvidia-cusolver-cu11 nvidia-cusparse-cu11 nvidia-nccl-cu11 nvidia-nvtx-cu11
  ```
  (You may not have all packages; uninstall any that appear.)

**3. Install CPU-only versions:**
- Run:
  ```
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
  ```

**4. Validate CPU-only environment:**
- Run:
  ```python
  import torch
  print(torch.cuda.is_available())  # Should print False
  ```
- Confirm no `nvidia-*` packages in `pip list`.

**5. Restart your backend and verify functionality.**

For more help, see the Help panel in the app or ask in the VERN Community.
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

## Advanced Features (2025-08-09)

- **Workflow Analytics:** Visualize workflow execution stats, bottlenecks, and success rates in the Workflow Editor.
- **Agent Health Monitoring:** View real-time agent status, error logs, and uptime metrics in the Agent Management Panel.
- **Plugin Sandboxing:** Plugins run in isolated environments with permission controls and resource limits. See Plugin Registry and Marketplace panels.
- **Notification Center:** Centralized alerts for workflow events, agent issues, and plugin updates.
- **User Activity Logs:** Track user actions for auditing and troubleshooting in the Workflow Logs Panel.
- **Accessibility Enhancements:** Keyboard navigation, ARIA labels, and high-contrast mode available across all panels.

### Usage Tips

- Access analytics and health metrics from the relevant panels.
- Configure plugin permissions and sandboxing in the Plugin Registry.
- Use the Notification Center for system-wide alerts.
- Enable high-contrast mode and keyboard shortcuts in user settings.
See code comments in the above files for technical details and extension guidelines.
