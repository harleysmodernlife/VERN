# VERN Known Issues & Gotchas

---

## Beast Mode Protocol Update (2025-07-30)

- **LLM-Driven Archetype Analysis:**  
  - For single user entries, one agent and a single LLM call output all 13 archetype resonance scores (base 14 vector) at once.
  - Full archetype cluster workflows are reserved for deep context or multi-turn analysis.
  - All context, vectors, and decisions are logged for auditability.
  - Archetype resonance can be mapped to standard indexes (Big Five, MBTI) for explainability and benchmarking.
  - HuggingFace emotion/trait models are deprecated for everyday use; retained only for strict benchmarking.

- **Recursive Implementation:**  
  - All code, docs, and context are kept in sync.
  - Work is recursive, deep, and autonomous—no shortcuts, no unnecessary dependencies.
  - Always read and preserve doc files before editing; never overwrite blindly.
  - Always call tools and test work; debug, patch, and refactor until all goals are met.
  - Update TASKS_AND_TODO.md and CHANGELOG.md after each confirmed change.

- **Auditability:**  
  - Every agent decision, context, and vector is logged and reconstructable.
  - System is explainable and can benchmark against standard psychological models.

---

## Multi-Agent Orchestration (2025-07)

- **LLM-only knowledge:**  
  - Agents cannot fetch real-time data or use external tools yet. All answers are based on the LLM’s internal knowledge and context.
  - Example: Weather, news, or live data queries will return general info, not current facts.

- **Agent confusion/overlap:**  
  - Orchestrator may delegate to clusters that aren’t relevant, or multiple agents may answer the same question.
  - Example: Finance agent may try to answer a weather question.
  - This is a known limitation of LLM-based planning and prompt engineering.

- **Ollama/model troubleshooting:**  
  - If you see “500 Server Error” or “address already in use,” Ollama may be stuck or out of resources.
  - Use `ps aux | grep ollama` and `sudo kill <PID>` to stop stuck processes.
  - Restart Ollama with `ollama serve`.
  - Try a smaller model if you run out of RAM.

- **Module import errors:**  
  - If you see `ModuleNotFoundError: No module named 'src'`, run the CLI as a module:  
    ```
    python3 -m src.mvp.cli
    ```

- **MCP proxy/server limitations:**  
  - Tool invocation from Python/browser clients is not supported by MCP proxy/server as of July 2025.
  - For MVP, tools are called directly in Python.

- **Performance:**  
  - LLM backend (Ollama/Qwen3) may be slow or error-prone on low-resource hardware.
  - Close other heavy programs and monitor RAM/CPU usage.

---

## Future Plans

- Add tool-calling (APIs, plugins, Python functions) for real-time data and actions.
- Add RAG (retrieval-augmented generation) so agents can pull from project docs, user data, or external knowledge bases.
- Improve agent specialization and orchestration logic.
- Add web/voice UI and plugin API for extensibility.

---

## Troubleshooting

- If you encounter LLM errors (timeouts, backend errors, slow responses):
  - Restart Ollama and ensure the model is loaded.
  - Try a smaller model (see [QUICKSTART.md](QUICKSTART.md)).
  - Increase the timeout in `src/mvp/qwen3_llm.py`.
  - Check system resources (RAM/CPU).
  - See [README.md](README.md) and [TASKS_AND_TODO.md](TASKS_AND_TODO.md) for more info.

---

## General Gotchas

- Always update TASKS_AND_TODO.md and README.md after confirmed changes.
- Never assume project state—read docs and context before acting.
- If stuck, checkpoint context and ask for review or clarification.

---

**If you encounter new issues, add them here and update the context in TASKS_AND_TODO.md.**
