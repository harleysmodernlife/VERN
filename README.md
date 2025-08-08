# VERN Project

**Note:** Voice features (ASR/TTS) require optional packages like `whisper`.
These are not installed by default. If you want voice support, run:
```
pip install git+https://github.com/openai/whisper.git
```
Otherwise, VERN will run without voice features.

## Core Architectural Patterns

To improve stability and maintainability, VERN has adopted several core architectural patterns:

*   **Standardized Error Envelope**: All API errors return a consistent JSON structure (`{ "ok": false, "error_code": "...", "message": "..." }`). This makes error handling on the frontend predictable and robust, as developers can rely on a single format for any failed request. See `vern_backend/app/errors.py` for implementation.

*   **Centralized Database Path Helper**: The database connection path is managed by a single utility function (`get_sqlite_path` in `vern_backend/app/db_path.py`). Configuration is handled via the `SQLITE_DB_PATH` environment variable. This centralization prevents configuration drift and makes it easy to locate and manage the database file.

*   **Unified Frontend API Base URL**: The frontend uses a single utility (`getApiBase` in `vern_frontend/lib/apiBase.js`) to determine the backend API's base URL. This utility checks for a global variable, then an environment variable, and finally falls back to a relative path. This ensures that the frontend can reliably connect to the backend across different deployment environments (local, staging, production) without code changes.

## Standardized Error Envelopes (Backend)

All non-2xx API errors return a uniform JSON envelope:
```json
{ "ok": false, "error_code": "STRING_CODE", "message": "Human-readable", "details": { }, "request_id": "optional" }
```
- Codes include COMMON (NOT_FOUND, VALIDATION_ERROR, UNAUTHORIZED, FORBIDDEN, CONFLICT, METHOD_NOT_ALLOWED, RATE_LIMITED, UNKNOWN_ERROR), DB (DB_UNAVAILABLE, DB_MIGRATION_REQUIRED, DB_CONSTRAINT_VIOLATION), REGISTRY (REGISTRY_NOT_FOUND, REGISTRY_CONFLICT, REGISTRY_UNAVAILABLE), PRIVACY (PRIVACY_DENIED, PRIVACY_CONSENT_REQUIRED), INTEGRATION (INTEGRATION_UNAVAILABLE, INTEGRATION_TIMEOUT, INTEGRATION_ERROR).
- request_id is added by middleware; x-error-code header mirrors error_code.
- See `vern_backend/app/errors.py` and `vern_backend/app/utils_logging.py`.

## DB Path Configuration

- Env: `SQLITE_DB_PATH` (recommended). Default in Docker: `/app/data/vern.sqlite`.
- Resolver `vern_backend/app/db_path.py:get_sqlite_path()` ensures parent dir.
- Admin DB verify: `GET /admin/db/verify` -> `{ ok: true, path, migrated, version }` or standardized envelope.

## Frontend API Base

Precedence for resolving API base:
1) `window.__VERN_API_BASE__`
2) `NEXT_PUBLIC_API_BASE`
3) Same-origin (relative)
- Utility: `vern_frontend/lib/apiBase.js:getApiBase()`
- Panels using it: `vern_frontend/components/Dashboard.js`, `vern_frontend/components/AgentClusterViz.js`.

## Smoke and Tests

- Smoke: `scripts/smoke.sh`, `scripts/full_smoke.sh` print/assert envelopes (integration NOT_FOUND, registry delete missing, privacy decision validation, admin DB verify).
- Backend tests: `vern_backend/tests/test_errors_envelopes.py`, `vern_backend/tests/test_backend_envelopes_additional.py`, `vern_backend/tests/test_admin_db_verify.py`.
- Run: `pytest -q`

## CI/CD & Health Checks

- Automated tests and health checks run on every push and PR via GitHub Actions.
- Health checks verify memory backend, LLM, and plugin availability.

## Backend Selection & Resource Awareness

- Optional ASR, TTS, vision, memory backends with sane defaults. Neo4j supported via `VERN_MEMORY_BACKEND=neo4j`.

## Import Hygiene

- Use absolute imports from project root (`src.`). Avoid relative imports.

## Quick Start

- Docker Compose:
  ```bash
  docker-compose up --build
  ```
  - Frontend: http://localhost:3000
  - Backend: http://localhost:8000
  - Neo4j: http://localhost:7474 (neo4j/password)

- Manual:
  - Backend deps: `pip install -r requirements.txt`
  - Frontend deps: `cd vern_frontend && npm install`
  - Import self-test: `PYTHONPATH=. python scripts/check_imports.py`
  - Run backend: `PYTHONPATH=. uvicorn vern_backend.app.main:app --host 0.0.0.0 --port 8000`
  - Run frontend: `cd vern_frontend && npm run dev`

## Environment Variables

- Configure via `.env` (see example values in this file).

## Troubleshooting

- Check `.env` and absolute imports if errors occur. Ensure Docker images build match codebase.

## Contributing

- Branch-based workflow; no secrets committed.

## Dashboard Features

- Panels for Config Editor, Workflow Editor, Plugin Marketplace, Onboarding, Help.

## Test Coverage & Docs

- Frontend integration tests for dashboard and onboarding; docs updated each sprint.

## Dockerfiles

- Backend and Frontend Dockerfiles under `vern_backend/` and `vern_frontend/`; Neo4j uses official image.
