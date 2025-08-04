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

- Edit the `.env` file in the project root.
  - Fill in required values (see comments in the file).
  - For most users, you can leave advanced options alone.

---

## 5. **Initialize the Database**

```bash
python src/db/init_db.py
```

---

## 5.5. **Import Self-Test (Recommended)**

Before starting the backend, run the import self-test script to check for broken imports:

```bash
python scripts/check_imports.py
```
If you see any `[ERROR]` lines, fix the import paths before proceeding.

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

## 8. **Run Core Tests (Optional, for sanity check)**

```bash
PYTHONPATH=src pytest tests/
```
- Only core agent orchestration and LLM routing are tested.
- If you see "2 passed", you're good!

---

## 9. **Using VERN**

- Use the dashboard to:
  - Edit config files
  - Run agent workflows
  - Get help and troubleshooting tips
  - Submit feedback

- You can also run backend agents directly:
  ```bash
  python src/mvp/cli.py
  ```

---

## 10. **Troubleshooting**

- If you see errors about missing config, check `.env`.
- If the dashboard doesn't load, make sure both backend and frontend are running.
- For help, use the Help panel in the dashboard or ask in the VERN community.

---

## 11. **Updating VERN**

- To update, pull the latest code and re-run `pip install -r requirements.txt` and `npm install` in `vern_frontend`.

---

## 12. **Getting Help**

- Use the Help panel in the dashboard.
- Read the README and AGENT_GUIDES for more info.
- Ask questions in the VERN community: https://github.com/harleysmodernlife/VERN#community

---

**You do NOT need Whisper, MCP, or any advanced plugins unless you want them.  
Just follow these steps and VERN should work for you!**
