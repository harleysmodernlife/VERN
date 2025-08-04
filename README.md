# VERN Project

**Note:** Voice features (ASR/TTS) require optional packages like `whisper`.  
These are not installed by default. If you want voice support, run:
```
pip install git+https://github.com/openai/whisper.git
```
Otherwise, VERN will run without voice features.

## CI/CD & Health Checks

- Automated tests and health checks run on every push and pull request via GitHub Actions.
- Tests cover agent orchestration, LLM routing, prompt utilities, and more.
- Health checks verify memory backend, LLM, and plugin availability.
- See `.github/workflows/ci.yml` for pipeline details.

## Backend Selection & Resource Awareness

- All ASR, TTS, vision, and memory backends are optional and configurable.
- Memory subsystem defaults to in-memory or file-based graph storage for resource-constrained setups.
- To use Neo4j, set `VERN_MEMORY_BACKEND=neo4j` in your `.env` and ensure Neo4j is running/configured.
- If Neo4j is not available, agents/plugins will fall back automatically and log a warning.
- Example config for low-resource setup:
  ```yaml
  default_asr: espeak-asr
  default_tts: espeak-tts
  default_vision: tesseract
  ```
- No forced installs. Use only the models/APIs/backends you already have.
- See docs for details on backend options, memory fallback, and resource requirements.

## Import Hygiene

All Python imports in VERN use absolute paths from the project root (e.g., `from src.db.logger import ...`, `from src.mvp.llm_router import ...`).  
Relative imports (e.g., `from db.logger import ...` or `from mvp.llm_router import ...`) are not supported and will cause import errors.  
**Always use absolute imports** to ensure compatibility with FastAPI, uvicorn, and CLI tools.

If you see "ModuleNotFoundError" or "ImportError", check that your imports use the `src.` prefix and match the project structure.

## Dashboard Integration: Web Search Panel

To wire the `/web_search` backend endpoint to a dashboard panel, use a React/Next.js component like this:

```javascript
// components/WebSearchPanel.js
import { useState } from "react";
export default function WebSearchPanel() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const search = async () => {
    const res = await fetch("/api/web_search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, num_results: 3 }),
    });
    const data = await res.json();
    setResults(data.results || []);
  };
  return (
    <div>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <button onClick={search}>Search</button>
      <ul>
        {results.map((r, i) => <li key={i}>{r}</li>)}
      </ul>
    </div>
  );
}
```

## Minimal Working Example: /web_search Endpoint

After starting the backend, you can test the `/web_search` endpoint:

**With curl:**
```bash
curl -X POST http://localhost:8000/web_search \
  -H "Content-Type: application/json" \
  -d '{"query": "VERN project", "num_results": 3}'
```

**With httpie:**
```bash
http POST http://localhost:8000/web_search query="VERN project" num_results:=3
```

## Quick Start

### 🚀 One-Click Full Suite: Docker Compose

You can launch the entire VERN stack (backend, frontend, Neo4j) with a single command using Docker Compose:

```bash
docker-compose up --build
```

- This will build and start:
  - Neo4j database (for graph memory, official image, no Dockerfile needed)
  - Backend API (FastAPI, built from vern_backend/Dockerfile)
  - Frontend dashboard (Next.js, built from vern_frontend/Dockerfile)
- Access:
  - Frontend: [http://localhost:3000](http://localhost:3000)
  - Backend API: [http://localhost:8000](http://localhost:8000)
  - Neo4j browser: [http://localhost:7474](http://localhost:7474) (username: neo4j, password: password)

To stop everything:
```bash
docker-compose down
```

---

## Manual Setup (if you prefer)

1. **Install dependencies**
   - Python 3.10+ required.
   - Create a virtual environment:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Install backend dependencies:
     ```
     pip install -r requirements.txt
     ```
   - Install frontend dependencies:
     ```
     cd vern_frontend
     npm install
     ```

2. **Environment Setup**
   - Edit `.env` in the project root. Fill in all required values (see comments in the file).
   - Do NOT use `.env.example`—it has been removed.

3. **Database Initialization**
   - For SQLite, run:
     ```
     python src/db/init_db.py
     ```
   - For other DBs, check `src/db/schema.sql` and update connection settings.

4. **Import Self-Test (Recommended)**
   - Before starting the backend, run the import self-test script to check for broken imports:
     ```
     PYTHONPATH=. python scripts/check_imports.py
     ```
   - If you see any `[ERROR]` lines, fix the import paths before proceeding.

5. **Launch Backend**
   - Start backend API:
     ```
     PYTHONPATH=. uvicorn vern_backend.app.main:app --host 0.0.0.0 --port 8000
     ```
   - Or use CLI:
     ```
     python src/mvp/cli.py
     ```

5. **Launch Frontend**
   - In `vern_frontend`:
     ```
     npm run dev
     ```
   - Open browser at `http://localhost:3000`.

6. **Testing**
   - Backend:
     ```
     PYTHONPATH=src pytest tests/
     ```
     - Only core agent orchestration and LLM routing are tested by default.
     - Legacy, Whisper, MCP, and plugin registry tests have been removed.
     - Add new tests in `tests/` as you add features.
   - Frontend:
     ```
     cd vern_frontend
     npm test
     ```
   - Integration tests now cover dashboard, onboarding, help panels, and onboarding checklist logic.
   - All tests passing as of August 2025.

---

## Environment Variables

All configuration is now in `.env`. Example variables:
```
OPENAI_API_KEY=your-openai-key-here
GEMINI_API_KEY=your-gemini-key-here
OPENWEATHERMAP_API_KEY=your-openweathermap-key-here
GOOGLE_CALENDAR_CLIENT_ID=your-google-client-id-here
GOOGLE_CALENDAR_CLIENT_SECRET=your-google-client-secret-here
GOOGLE_CALENDAR_ID=your-calendar-id-here
GOOGLE_CALENDAR_CREDENTIALS_JSON=google_calendar_service_account.json
SQLITE_DB_PATH=./db/vern.sqlite
CHROMA_DB_PATH=./chroma_data/
DEBUG=false
VERN_ENV=development
DEBUG_OLLAMA=0
LANGUAGE=en
ENABLE_SCREEN_READER=false
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

---

## Troubleshooting

- If you see missing config errors, check `.env` for required variables.
- If you see `[ERROR]` lines when running `python scripts/check_imports.py`, fix the import paths to use absolute imports (e.g., `from src.db.logger import ...`).
- If you see `ModuleNotFoundError` or `ImportError`, ensure you have installed all dependencies:
  ```
  pip install -r requirements.txt
  ```
- All code now loads `.env` directly using `dotenv`.
- For weather and calendar plugins, ensure API keys and credentials are set in `.env`.
- If you see "Connection refused" errors for Neo4j, make sure you started the Docker Compose stack above.
- If you see build errors, ensure `vern_backend/Dockerfile` and `vern_frontend/Dockerfile` exist and match your codebase.

---

## Contributing

- Follow git hygiene: always work on a feature branch, commit with clear messages, and open pull requests for review.
- Never commit `.env` or secrets.

---

## Dashboard Features

### Config Editor Panel
- Edit `.env` and YAML config files directly from the dashboard.
- Validation and error feedback included.
- See onboarding checklist for required config.

### Workflow Editor Panel
- Build, visualize, and run multi-agent workflows.
- Drag-and-drop canvas for reordering workflow steps.
- Visual linking (arrows) between steps.
- Live previews for agent/plugin outputs.
- Chain agent outputs and automate tasks.

### Plugin Marketplace Panel
- Visual cards for each plugin: name, description, status, and icon.
- Enable, disable, update, and remove plugins.
- Edit plugin configuration (API keys, options) via config modal.
- Submit new plugins for review.

### Onboarding Panel
- Step-by-step checklist for new users.
- Persona/profile setup and feedback submission.
- Tooltips and direct links to docs/help for each onboarding step.
- **New:** Automatic detection and notification if Neo4j or other dependencies are missing.

### Help & Troubleshooting
- Each dashboard panel includes links to relevant documentation.
- For common issues, see the onboarding checklist and troubleshooting section.

---

## Test Coverage & Documentation

- Frontend integration tests cover dashboard, onboarding, help, and feedback panels.
- Onboarding checklist logic is robust and tested.
- Documentation (README, QUICKSTART, AGENT_GUIDES) is up to date after each sprint.
- See `QUICKSTART.md` and `TASKS_AND_TODO.md` for more details.
- For agent/plugin development, see `AGENT_GUIDES/`.

---

## Dockerfiles

- **vern_backend/Dockerfile:** Builds FastAPI backend with uvicorn.
- **vern_frontend/Dockerfile:** Builds Next.js frontend.
- **Neo4j:** Uses official image, no Dockerfile needed.
