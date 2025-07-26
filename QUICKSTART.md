# VERN Quickstart Guide

**Read first, then amend docs—never assume state. Never truncate with “remains unchanged”—always show full, updated context.**

---

## 1. Prerequisites

- Python 3.9+ installed
- Git installed
- Basic terminal/command line familiarity

---

## 2. Setup

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/vern.git
   cd vern
   ```

2. **Create and activate a virtual environment:**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   ```
   python3 src/db/init_db.py
   ```
   - This will create `db/vern.db` using the schema in `src/db/schema.sql`.
   - Inspect or manage the DB with the `sqlite3` CLI or a GUI tool.

---

## 3. Local LLM Setup (Ollama)

### A. Install Ollama

1. **Install Ollama (Linux/macOS):**
   ```
   curl -fsSL https://ollama.com/install.sh | sh
   ```
   - See [Ollama docs](https://ollama.com/) for Windows or advanced options.

2. **Start the Ollama service (if not already running):**
   ```
   ollama serve
   ```

### B. Download and Run a Model

1. **Pull the Qwen3-0.6B model:**
   ```
   ollama pull qwen3:0.6b
   ```
2. **Test the model:**
   ```
   ollama run qwen3:0.6b
   ```

### C. Troubleshooting

- If you run out of RAM, try a smaller model (e.g., `phi`, `tinyllama`).
- If Ollama is not found, ensure it’s in your PATH and the service is running.
- For more models, see [Ollama Library](https://ollama.com/library).

---

## 4. Running the MVP

### Manual Testing

1. Navigate to the MVP directory:
   ```
   cd src/mvp/
   ```
2. Run the CLI:
   ```
   python3 cli.py
   ```
   - Try all options and see agent responses.

### Automated Testing

1. From the project root, run:
   ```
   python3 tests/test_mvp.py
   python3 tests/test_db_logging.py
   python3 tests/test_agents_extended.py
   python3 tests/test_cross_cluster_handoff.py
   python3 tests/test_agents_horizontal.py
   python3 tests/test_llm_integration.py
   python3 tests/test_agent_context_workflow.py
   python3 tests/test_llm_backend_swap.py
   ```
   - Confirms all agent, LLM, and workflow logic.

---

## 5. LLM Backend Modularity

- LLM backend/model selection is controlled via `config/agent_backends.yaml`.
- Supported backends: `ollama-<model>`, `fake_llm`, `qwen3-0.6b` (transformers), and more.
- Add new backends by writing a wrapper and updating `llm_router.py`.
- See AGENT_GUIDES/README.md for details.

---

## 6. Accessibility & Internationalization

- VERN aims to support keyboard navigation, screen readers, and multiple languages.
- See GOALS_AND_MILESTONES.md for progress and plans.

---

## 7. Getting Help

- See COMMUNITY.md for support channels.
- Read CONTRIBUTING.md and SECURITY_AND_GIT_GUIDELINES.md before making changes.

---

**Welcome to VERN! Your feedback and contributions are valued.**

---

## Learn More

- See [FUTURE_VISION_AND_ROADMAP.md](FUTURE_VISION_AND_ROADMAP.md) for VERN’s long-term goals, modular design, and future direction.
