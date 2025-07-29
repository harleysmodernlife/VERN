# VERN Quickstart Guide

**Read first, then amend docs—never assume state. Never truncate with “remains unchanged”—always show full, updated context.**

---

## 1. Prerequisites

- Python 3.9+ installed
- Git installed
- Basic terminal/command line familiarity
- **Hardware:** At least 4GB RAM (8GB+ recommended for Qwen3-0.6B); for slower hardware, use a smaller model (see below).

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

- **RAM Requirements:** Qwen3-0.6B requires at least 4GB RAM (more recommended). If you run out of RAM, try a smaller model (e.g., `phi`, `tinyllama`).
- If Ollama is not found, ensure it’s in your PATH and the service is running.
- For more models, see [Ollama Library](https://ollama.com/library).
- For best performance on low-resource hardware, use quantized GGUF models or run Ollama in CPU mode (expect slower inference).
- **If you see timeouts or backend errors in the CLI, try restarting Ollama, switching to a smaller model, or increasing the timeout in `src/mvp/qwen3_llm.py`.**
- If you get a "ModuleNotFoundError: No module named 'src'" error, run the CLI as a module:  
  ```
  python3 -m src.mvp.cli
  ```
- See [KNOWN_ISSUES_AND_GOTCHAS.md](KNOWN_ISSUES_AND_GOTCHAS.md) for more troubleshooting tips.

---

## 4. Running the MVP

### Manual Testing

1. **Run the CLI from the project root:**
   ```
   python3 -m src.mvp.cli
   ```
   - The CLI is now LLM-powered by default (Qwen3 via Ollama). Type natural language or explicit tool commands.
   - Try all options and see agent responses.

2. **What to Expect:**
   - Multi-agent orchestration: Orchestrator delegates to clusters and aggregates their responses.
   - Sample output:
     ```
     You: what's the weather like in tokyo?
     (orchestrator) (plan: Involve research and finance clusters to answer the question.)
     [Research]: The weather in Tokyo varies depending on time of year. In spring, it's often sunny, while in autumn, it can be cloudy. Humidity is high in Tokyo, so you might expect a warm and humid climate.
     [Finance]: I'm unable to provide specific weather information as the context doesn't include any weather-related details. If you have questions about budgeting, resource allocation, or other finance-related topics, feel free to ask!
     ```

### Automated Testing

1. From the project root, run:
   ```
   python3 tests/test_mvp.py
   python3 tests/test_db_logging.py
   python3 tests/test_agents_extended.py
   python3 tests/test_agents_horizontal.py
   python3 tests/test_cross_cluster_handoff.py
   python3 tests/test_llm_integration.py
   python3 tests/test_agent_context_workflow.py
   python3 tests/test_llm_backend_swap.py
   ```
   - Confirms all agent, LLM, and workflow logic.

---

## 5. Modular LLM Provider/Model Selection

- **Config-driven:**  
  - LLM provider/model selection is now driven by `config/agent_backends.yaml`.
  - The LLM router (`src/mvp/llm_router.py`) reads the config and routes agent calls to the selected backend/model.
  - To change models/providers, edit `config/agent_backends.yaml` and set the default backend/model.
  - Supported: Ollama (local), OpenAI (cloud, planned), fake_llm (testing), and more.

---

## MCP Server Integration (Tool API)

VERN includes a modular MCP server for tool discovery and invocation via the MCP CLI and Inspector.

- **Location:** `src/mvp/mcp_server.py`
- **How to run:**  
  1. Create and activate a venv:  
     `python3 -m venv .venv && source .venv/bin/activate`
  2. Install MCP CLI:  
     `pip install "mcp[cli]"`
  3. Start the server:  
     `mcp dev src/mvp/mcp_server.py`
- **How to extend:**  
  Add a new `@mcp.tool()` function in `src/mvp/mcp_server.py`.  
  See the README "MCP Server Integration" section for details.

---

## Cockpit/Dashboard UI (Prototype)

- See `vern_dashboard.html` in the project root for a minimal web UI prototype.
- This dashboard lets you invoke MCP tools, enter parameters, and view results visually.
- (Future: Live connection to MCP server for real-time workflows.)

---

## 6. LLM Backend Modularity

- LLM backend/model selection is controlled via `config/agent_backends.yaml`.
- Supported backends: `ollama-<model>`, `fake_llm`, `qwen3-0.6b` (transformers), and more.
- Add new backends by writing a wrapper and updating `llm_router.py`.
- See [AGENT_GUIDES/README.md](AGENT_GUIDES/README.md) for details.

---

## 7. Accessibility & Internationalization

- VERN aims to support keyboard navigation, screen readers, and multiple languages.
- See [GOALS_AND_MILESTONES.md](GOALS_AND_MILESTONES.md) for progress and plans.

---

## 8. Getting Help

- See [COMMUNITY.md](COMMUNITY.md) for support channels.
- Read [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY_AND_GIT_GUIDELINES.md](SECURITY_AND_GIT_GUIDELINES.md) before making changes.

---

**Welcome to VERN! Your feedback and contributions are valued.**

---

## Learn More

- See [FUTURE_VISION_AND_ROADMAP.md](FUTURE_VISION_AND_ROADMAP.md) for VERN’s long-term goals, modular design, and future direction.
