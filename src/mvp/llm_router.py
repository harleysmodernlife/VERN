"""
VERN LLM Router (Config-Driven)
-------------------------------
Routes agent LLM calls to the selected provider/model based on config/agent_backends.yaml.
Supports modular, extensible backend selection for future GUI/provider/model switching.
"""

import yaml
import os

# Load config from YAML
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../config/agent_backends.yaml')
def load_llm_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

LLM_CONFIG = load_llm_config()

def get_llm_backend():
    """
    Returns the current backend and model as selected in config/agent_backends.yaml.
    Example config:
      default: ollama-qwen3:0.6b
      backends:
        ollama-qwen3:0.6b:
          provider: ollama
          model: qwen3:0.6b
        ollama-phi:
          provider: ollama
          model: phi
        openai-gpt-4:
          provider: openai
          model: gpt-4
    """
    backend_key = LLM_CONFIG.get('default', 'ollama-qwen3:0.6b')
    backend = LLM_CONFIG['backends'].get(backend_key, {})
    return backend.get('provider', 'ollama'), backend.get('model', 'qwen3:0.6b')

def route_llm_call(prompt, **kwargs):
    """
    Routes the prompt to the selected LLM backend/model.
    """
    provider, model = get_llm_backend()
    if provider == 'ollama':
        from src.mvp.ollama_llm import call_ollama
        return call_ollama(prompt, model=model, **kwargs)
    elif provider == 'openai':
        # Placeholder: implement OpenAI backend
        return "[OpenAI backend not implemented yet]"
    elif provider == 'fake_llm':
        from src.mvp.fake_llm import call_fake_llm
        return call_fake_llm(prompt, **kwargs)
    else:
        return f"[Unknown LLM provider: {provider}]"
