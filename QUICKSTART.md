# VERN Quickstart (2025 Edition)

This guide is for **non-coders and new users**.
Follow these steps to get VERN running and usable for real-world tasks.

---

## 1. **Install Prerequisites**

- **Python 3.10+** (recommended: 3.12)
- **Node.js** (for the dashboard/frontend)
- **Docker** (optional, for easiest setup)

---

## 2. **Clone the VERN Repository**

```bash
git clone https://github.com/harleysmodernlife/VERN.git
cd VERN
```

---

## 3. **Set Up Python Environment**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 4. **Configure VERN**

- Create a `.env` file in the project root (you can copy `.env.example` to start).
- **Database Path**: The location of the SQLite database is controlled by the `SQLITE_DB_PATH` environment variable. If this is not set, it will default to `/app/data/vern.sqlite` inside the Docker container or a local path if run manually. For local development, it's recommended to set it explicitly:
  ```
  SQLITE_DB_PATH=./data/vern.sqlite
  ```
- Fill in other required values as needed.

---

## 5. **Initialize the Database**

This step is only necessary if you are *not* using the pre-built Docker image.

```bash
python src/db/init_db.py
```

---

## 6. **Start the Backend API**

```bash
uvicorn vern_backend.app.main:app --host 0.0.0.0 --port 8000
```
- The backend should now be running at [http://localhost:8000](http://localhost:8000)

---

## 7. **Start the Frontend Dashboard**

```bash
cd vern_frontend
npm install
npm run dev
```
- Open your browser to [http://localhost:3000](http://localhost:3000)

---

## 8. **Run Tests (Recommended)**

To ensure everything is working correctly, run the smoke tests. These scripts verify core functionality, including API health, agent communication, and error handling.

- **Focused Backend Tests**:
  ```bash
  ./scripts/smoke.sh
  ```
- **Frontend Tests**:
  ```bash
  cd vern_frontend && npm test
  ```
- **Full End-to-End Smoke Tests**:
  ```bash
  ./scripts/full_smoke.sh
  ```

---

## 9. **Troubleshooting**

VERN uses a standardized error envelope for all API responses that are not successful (i.e., not a 2xx status code). This helps in quickly identifying the nature of a problem. The JSON response will look like this:

```json
{
  "ok": false,
  "error_code": "SOME_CODE",
  "message": "A human-readable explanation.",
  "details": { ... },
  "request_id": "unique-id-for-this-request"
}
```

Here are a few key `error_code` examples to look out for:

- `PLUGIN_INVALID`: An agent tried to use a plugin that doesn't exist or is configured incorrectly.
- `DB_UNAVAILABLE`: The backend API cannot connect to the database. Check that the database is running and that the `SQLITE_DB_PATH` is correct.
- `VALIDATION_ERROR`: The request was malformed. The `details` field will contain more information on what was wrong.
- `PRIVACY_DENIED`: A privacy-sensitive action was blocked by the policy engine.

---

## 10. **Getting Help**

- Use the Help panel in the dashboard.
- Read the `README.md` and `AGENT_GUIDES` for more info.
- Ask questions in the VERN community.
