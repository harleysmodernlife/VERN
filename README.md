# VERN

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

---

## Architecture Overview

> **VERN is a modular, agent-based system with a clear backend/frontend split.**

**Backend:**  
- Built with Python (FastAPI), managing all agent logic, plugin registry, orchestration, advanced dynamic feedback processing, and REST/WebSocket APIs.  
- Directory: `vern_backend/`  
- See [vern_backend/README.md](vern_backend/README.md)

**Frontend:**  
- Constructed with Next.js (React), featuring a modular dashboard for plugin management, interactive onboarding, workflow visualization with per-step context support, real-time notifications, and integrated feedback.  
- Directory: `vern_frontend/`  
- See [vern_frontend/README.md](vern_frontend/README.md)

**Key Components:**  
- **Modular Agent Clusters:**  
  Agents (DevTeam, KnowledgeBroker, Research, Health, Finance, Admin, Creativity, Career, Social, Environment, Legal, Travel, Security, Archetype, Emergent, ID10T Monitor) support persona tuning through both UI and API.
  
- **Orchestrator:**  
  Coordinates multi-agent communication while refining per-step context using advanced processing (trimming, capitalization, and other tailored adjustments). It also integrates a dynamic feedback loop: aggregated user feedback triggers automatic recommendations for adjusting agent parameters.
  
- **Workflow Editor:**  
  A visual tool that now supports per-step context input. The context for each step is refined in the backend for improved agent performance. Further sophisticated processing is planned for future sprints.
  
- **Feedback System:**  
  Users can submit feedback directly through the dashboard. Feedback is aggregated and used by the orchestrator to tune agent parameters dynamically.
  
- **Real-Time Notifications:**  
  A dedicated NotificationPanel displays live alerts regarding system errors and significant events.
  
- **User Onboarding and Guided Tours:**  
  Interactive panels guide new users through dashboard features, ensuring a smooth introduction.
  
- **Security & Extensibility:**  
  Incorporates robust logging, secure JWT/OAuth2 authentication, and a modular design for seamless feature expansion.

---

## API Reference

- **Backend API docs:** [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger/OpenAPI)

### Example Endpoints

#### List All Agent Clusters
```bash
curl -X GET http://localhost:8000/agents
```

#### Send a Message to an Agent (with Persona, Context, and Memory)
```bash
curl -X POST http://localhost:8000/agents/devteam/respond \
  -H "Content-Type: application/json" \
  -d '{"message": "What is our current project status?", "persona": "architect", "context": {"project": "VERN"}, "memory": "previous interactions"}'
```

#### List All Available Plugins/Tools
```bash
curl -X GET http://localhost:8000/plugins
```

#### Call a Plugin/Tool
```bash
curl -X POST http://localhost:8000/plugins/weather_plugin/call \
  -H "Content-Type: application/json" \
  -d '{"params": {"location": "Chicago"}}'
```

#### Submit a Plugin to the Marketplace
```bash
curl -X POST http://localhost:8000/plugins/submit \
  -H "Content-Type: application/json" \
  -d '{"name": "my_plugin", "description": "Does something cool", "code": "def run(): ...", "author": "yourname"}'
```

#### View Workflow Logs
```bash
curl -X GET http://localhost:8000/agents/workflows/logs
```

#### Authentication Example
```bash
curl -H "Authorization: Bearer <your_token>" http://localhost:8000/secure-status
```

---

## Sample Workflows

- **Chat with Agents:**  
  Submit messages via the dashboard or CLI. The orchestrator routes your input to the relevant agent(s) and aggregates responses.
  
- **Persona Tuning:**  
  Choose different personas (e.g., coach, architect, mentor) to shape agent responses via both the UI and API.
  
- **Agent Memory & Context:**  
  Agents use previous interactions and refined per-step context data (processed in the orchestrator) to generate informed responses.
  
- **Advanced Multi-Agent Workflows:**  
  Chain agents and plugins visually or via API to execute complex tasks. Each workflow step can include customized and refined context.
  
- **Feedback-Driven Parameter Adjustment:**  
  Submit feedback through the dashboard. The orchestrator uses aggregated feedback to recommend parameter adjustments, enhancing overall system performance.
  
- **Real-Time Notifications:**  
  Stay informed about system errors and events with live alerts from the NotificationPanel.
  
- **User Onboarding:**  
  Interactive guides assist you with dashboard navigation and feature utilization.

---

## Troubleshooting & FAQ

**Common Issues:**  
- **Startup Problems:**  
  Ensure Python (3.9+), Node.js (18+), and virtual environments are correctly set up.  
- **API Errors:**  
  Check backend logs; confirm uvicorn is running and endpoints are correctly addressed.  
- **LLM Response Issues:**  
  Verify Ollama is running and models are properly configured.  
- **Plugin Visibility:**  
  Refresh the Plugin Registry panel if a plugin is missing.  
- **Database Access:**  
  Confirm that SQLite/ChromaDB files are accessible and not locked.

**Debugging Tips:**  
- Use `pytest` for backend issues and `npm test` for frontend testing.  
- Leverage browser developer tools to inspect UI issues.  
- Review API logs and utilize endpoints like `/logs` or `/status`.

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
