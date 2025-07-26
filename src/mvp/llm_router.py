"""
LLM Router: Modular backend selector for VERN agents.

Supports: ollama, fake_llm, qwen3 (transformers), and future backends.
"""

import yaml
import os

from fake_llm import call_llm as fake_llm_call
from ollama_llm import generate_ollama

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'agent_backends.yaml')

def load_backend_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

def call_llm_for_agent(agent_name, prompt, context=None, **kwargs):
    backend_config = load_backend_config()
    backend = backend_config.get(agent_name, "fake_llm")
    if backend == "fake_llm":
        return fake_llm_call(prompt, context)
    elif backend.startswith("ollama"):
        # Format: ollama-<model>
        # Example: ollama-qwen3:0.6b
        model = backend.split("-", 1)[1] if "-" in backend else "qwen3:0.6b"
        return generate_ollama(prompt, model=model, context=context, **kwargs)
    elif backend == "qwen3-0.6b":
        # Placeholder for direct transformers integration
        from qwen3_llm import Qwen3LLM
        llm = Qwen3LLM()
        result = llm.generate(prompt, context=context)
        return result["content"]
    else:
        return f"[LLM Router] No backend configured for agent '{agent_name}'. Prompt: {prompt}"
