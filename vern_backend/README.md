# VERN Backend (FastAPI)

This is the backend API server for the VERN platform.  
It exposes all agent, plugin, orchestration, and registry logic as REST and WebSocket APIs for the frontend and third-party extensions.

## Features

- Modular FastAPI app for agent orchestration, plugin registry, and user/session management
- REST and WebSocket APIs for all agent, plugin, and orchestration actions
- Real-time logs, diagnostics, and agent/cluster status
- Authentication (JWT/OAuth2) and multi-user support (planned)
- Plugin/extension API for third-party devs
- OpenAPI/Swagger docs for all endpoints
- Automated tests and CI/CD ready

## Directory Structure

- `app/` - FastAPI app modules (agents, plugins, registry, users, etc.)
- `tests/` - Automated tests for all endpoints and workflows
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Quickstart

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the server:
   ```
   uvicorn app.main:app --reload
   ```
3. Visit the docs:
   ```
   http://localhost:8000/docs
   ```

## API Reference

- **Interactive API docs:** [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger/OpenAPI)
- **Key Endpoints:**
  - `GET /agents` — List all agent clusters
  - `POST /agents/{agent_name}/respond` — Send a message to an agent and get a response
  - `GET /plugins` — List all available plugins/tools
  - `POST /plugins/{tool_name}/call` — Call a plugin/tool with parameters
  - `GET /users/{user_id}` — Get user profile
  - `POST /users/{user_id}/update` — Update user profile
  - `GET /logs` — Get recent logs and diagnostics
  - `GET /status` — Get system/cluster status
  - (See `/docs` for full list and schemas)

## Testing & CI

- Run all backend tests:
  ```
  pytest
  ```
- Tests cover agent logic, plugin/tool calls, orchestration, and API endpoints.
- CI/CD: Add your preferred workflow (GitHub Actions, etc.) to automate tests on push/PR.

## See Also

- [vern_frontend/README.md](../vern_frontend/README.md)
- [../README.md](../README.md)
