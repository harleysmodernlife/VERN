# Known Issues & Gotchas

---

## LLM Backend/Model Notes

- **Ollama Model Names:**  
  - Model names must match Ollama’s registry exactly (e.g., `qwen3:0.6b`, `phi`, `tinyllama`).
  - If a model isn’t available, check [Ollama Library](https://ollama.com/library) for updates.
- **Qwen3-0.6B in Ollama:**  
  - Now available as `qwen3:0.6b`. Earlier attempts failed due to incorrect naming.
- **RAM/Performance:**  
  - Qwen3-0.6B requires at least 4GB RAM (more recommended). If you run out of RAM, try a smaller model (e.g., `phi`, `tinyllama`).
  - Ollama runs in CPU mode if no GPU is detected—expect slower inference.
  - For best results on low-resource hardware, use quantized GGUF models.
- **Hugging Face Transformers:**  
  - Direct integration is possible for any model, but may be slow or crash on low-RAM systems.
  - Use quantized GGUF models with llama.cpp for best performance on older hardware.
- **Backend Modularity:**  
  - All LLM plumbing is modular and config-driven via `llm_router.py` and `agent_backends.yaml`.
  - Swapping models/providers is safe and easy.

---

## Agent/Workflow Gotchas

- **Agent LLM Calls:**  
  - All agent LLM calls must go through the router, never direct to a backend.
- **Testing:**  
  - Always test new backends with both CLI and automated tests.
- **Documentation:**  
  - Update QUICKSTART.md, AGENT_GUIDES/README.md, and MVP_IMPLEMENTATION_PLAN.md when adding or changing backends.

---

## See Also

- [QUICKSTART.md](QUICKSTART.md)
- [AGENT_GUIDES/README.md](AGENT_GUIDES/README.md)
- [MVP_IMPLEMENTATION_PLAN.md](MVP_IMPLEMENTATION_PLAN.md)
