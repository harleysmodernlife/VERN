# VERN Quickstart Guide

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

**Read first, then amend docs—never assume state. Never truncate with “remains unchanged”—always show full, updated context.**

---

## Beast Mode Doc Protocol

> **VERN Beast Mode Doc Protocol**
>
> 1. **Recursive, Context-Driven:** Always read and preserve all relevant docs before editing. Never overwrite blindly.
> 2. **Sync Code, Docs, and Context:** Update all docs, task lists, and changelogs after every confirmed change.
> 3. **Onboarding First:** Ensure docs enable new users, whether coders or not, to get started safely.
> 4. **Transparency & Auditability:** Log every change, decision, and lesson in CHANGELOG.md and TASKS_AND_TODO.md.
> 5. **No Stale or Misleading Docs:** Clearly mark deprecated features and planned updates.
> 6. **Architecture & Workflows:** Include diagrams, sample workflows, and real-world use cases.
> 7. **Testing & CI/CD:** Document all tests, coverage, and CI/CD setups; each change comes with tests and doc updates.
> 8. **Security & Privacy:** Never commit secrets; use `.env.example` and reference SECURITY_AND_GIT_GUIDELINES.md.
> 9. **Accessibility & Internationalization:** Maintain checklists for both.
> 10. **Extension & Marketplace:** Document how to add agents, plugins, and UI panels.
> 11. **Continuous Review:** Regularly update docs after each sprint.
> 12. **Human-AI Partnership:** Ensure all docs support ethical, transparent, and accessible human-AI collaboration.

---

## 1. Prerequisites

- Python 3.9+ installed
- Node.js 18+ and npm (for frontend)
- Git installed
- Basic terminal/command line skills
- **Hardware:** At least 4GB RAM (8GB+ recommended for larger models)

---

## 2. Setup (Backend & Frontend)

### A. Clone the repository

```bash
git clone https://github.com/harleysmodernlife/VERN.git
cd VERN
```

### B. Backend Setup (FastAPI)

```bash
cd vern_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### C. Frontend Setup (Next.js)

Open a new terminal:

```bash
cd vern_frontend
npm install
npm run dev
```
- App: [http://localhost:3000](http://localhost:3000)

---

## 3. Onboarding Checklist (Non-Coder Friendly)

- [ ] Clone the repository and install prerequisites.
- [ ] Start the backend (FastAPI) and frontend (Next.js).
- [ ] Open [http://localhost:3000](http://localhost:3000) in your browser.
- [ ] Explore dashboard panels including chat, plugin registry, user profile, onboarding, etc.
- [ ] Read [SECURITY_AND_GIT_GUIDELINES.md](SECURITY_AND_GIT_GUIDELINES.md) before handling any config or code.
- [ ] If contributing, review [CONTRIBUTING.md](CONTRIBUTING.md).
- [ ] If stuck, consult [COMMUNITY.md](COMMUNITY.md) or ask for help.

---

## 4. Local LLM Setup (Ollama)

### A. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```
- Check [Ollama docs](https://ollama.com/) for Windows or advanced options.

### B. Download and Run a Model

```bash
ollama pull qwen3:0.6b
ollama run qwen3:0.6b
```

### C. Troubleshooting

- Ensure Ollama is in your PATH.
- For alternative models, visit: [Ollama Library](https://ollama.com/library).
- For low-resource systems, use quantized models or CPU mode (expect slower inference).
- See [KNOWN_ISSUES_AND_GOTCHAS.md](KNOWN_ISSUES_AND_GOTCHAS.md) for more troubleshooting tips.

---

## 5. Running the MVP

- **CLI:** `python -m mvp.cli` (from project root)
- **GUI:** `streamlit run src/mvp/gui.py` (minimal prototype)
- **Frontend:** [http://localhost:3000](http://localhost:3000) (Next.js dashboard)
- **Backend:** [http://localhost:8000/docs](http://localhost:8000/docs) (FastAPI API docs)
- **Feedback:** Submit user feedback via the integrated Feedback Panel.

---

## 6. API Usage & Sample Workflows

- **Backend API docs:** [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger/OpenAPI)
- **Full API Reference:** See [README.md](README.md#api-reference) for OpenAPI YAML and examples.

### Quick API Examples

#### List all agent clusters

```bash
curl -X GET http://localhost:8000/agents
```

#### Send a message to an agent (with persona, context, and memory)

```bash
curl -X POST http://localhost:8000/agents/devteam/respond \
  -H "Content-Type: application/json" \
  -d '{"message": "What is our current project status?", "persona": "architect", "context": {"project": "VERN"}, "memory": "previous interactions"}'
```

#### List all available plugins/tools

```bash
curl -X GET http://localhost:8000/plugins
```

#### Call a plugin/tool

```bash
curl -X POST http://localhost:8000/plugins/weather_plugin/call \
  -H "Content-Type: application/json" \
  -d '{"params": {"location": "Chicago"}}'
```

#### Submit a plugin to the marketplace

```bash
curl -X POST http://localhost:8000/plugins/submit \
  -H "Content-Type: application/json" \
  -d '{"name": "my_plugin", "description": "Does something cool", "code": "def run(): ...", "author": "yourname"}'
```

#### View workflow logs

```bash
curl -X GET http://localhost:8000/agents/workflows/logs
```

#### Authentication Example

```bash
curl -H "Authorization: Bearer <your_token>" http://localhost:8000/secure-status
```

---

## 7. Testing

- **Backend:**  
  ```bash
  cd vern_backend
  pytest
  ```
- **Frontend:**  
  Run `npm test` in the vern_frontend directory.
- **API:**  
  Visit [http://localhost:8000/docs](http://localhost:8000/docs) to test endpoints.

---

## 8. Modular LLM Provider/Model Selection

- Configure the default model in `config/agent_backends.yaml`.
- Supported: Ollama (local), OpenAI (cloud, planned), fake_llm (testing), etc.

---

## 9. Plugin API & Tool-Calling

- Add Python functions with the `@mcp.tool()` decorator in `src/mvp/mcp_server.py`.
- Tools are auto-discovered in the GUI.
- See [AGENT_GUIDES/README.md](AGENT_GUIDES/README.md) for details.

---

## 10. Accessibility & Internationalization

- VERN supports keyboard navigation and screen readers.
- See [GOALS_AND_MILESTONES.md](GOALS_AND_MILESTONES.md) for current progress and plans.

---

## 11. Getting Help

- Refer to [COMMUNITY.md](COMMUNITY.md) for support details.
- For contributions, consult [CONTRIBUTING.md](CONTRIBUTING.md).
- Review [SECURITY_AND_GIT_GUIDELINES.md](SECURITY_AND_GIT_GUIDELINES.md) before modifying code or config.

---

## Additional Features & Current State

- **Turbocharged Agent Clusters:**  
  All agents support persona tuning via both UI and API. Agent memory and context are handled via the backend; our visual workflow editor now allows per-step context input (basic implementation, refined processing coming soon).

- **Workflow Editor Enhancements:**  
  Use the Workflow Editor to build multi-agent workflows. Each step now has fields for agent name, persona, and optional context.

- **Feedback System:**  
  Submit feedback directly through the dashboard using the integrated Feedback Panel. This helps improve the system over time.

- **User Onboarding & Guided Tours:**  
  Interactive panels guide you through the dashboard and its features, ensuring a smooth learning curve.

- **Robust Security & Logging:**  
  The system employs JWT/OAuth2 for secure API access and extensive logging for transparency.

---

## Troubleshooting & FAQ

- **Startup Issues:**  
  Ensure Python (3.9+), Node.js (18+), and virtualenv are set up correctly.
- **API Errors:**  
  Check the backend logs and confirm uvicorn is running.
- **LLM Response Issues:**  
  Make sure Ollama is running and models are properly configured.
- **Plugin Issues:**  
  Refresh the Plugin Registry panel if a plugin is not visible.
- **Database Access:**  
  Verify that SQLite/ChromaDB is not locked.

**Debugging Tips:**
- Use `pytest` for backend and `npm test` for frontend issues.
- Utilize browser developer tools for UI debugging.
- Review logs via endpoints such as `/logs` or `/status`.

---

## Additional Resources

- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
- [QUICKSTART.md](QUICKSTART.md)
- [AGENT_GUIDES/README.md](AGENT_GUIDES/README.md)
- [TASKS_AND_TODO.md](TASKS_AND_TODO.md)
- [CHANGELOG.md](CHANGELOG.md)
- [SECURITY_AND_GIT_GUIDELINES.md](SECURITY_AND_GIT_GUIDELINES.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [FUTURE_VISION_AND_ROADMAP.md](FUTURE_VISION_AND_ROADMAP.md)

---

**VERN is dedicated to fostering a collaborative, transparent, and intelligent human-AI partnership. Always review the documentation to ensure clarity and consistency.**
