"""
VERN LLM Router (Config-Driven, Robust Error Handling)
-------------------------------
Routes agent LLM calls to the selected provider/model based on config/agent_backends.yaml.
Supports modular, extensible backend selection for future GUI/provider/model switching.
Now includes robust error handling and streaming support.
"""

import yaml
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../config/agent_backends.yaml')
def load_llm_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

LLM_CONFIG = load_llm_config()

def get_llm_backend(agent_name=None):
    if agent_name and 'agents' in LLM_CONFIG and agent_name in LLM_CONFIG['agents']:
        backend_key = LLM_CONFIG['agents'][agent_name]
    else:
        backend_key = LLM_CONFIG.get('default', 'ollama-qwen3:0.6b')
    backend = LLM_CONFIG['backends'].get(backend_key)
    if backend is None:
        return None, None
    return backend.get('provider', 'ollama'), backend.get('model', 'qwen3:0.6b')

def route_llm_call(prompt, **kwargs):
    """
    Routes the prompt to the selected LLM backend/model.
    Returns a string or a generator (for streaming).
    Includes robust error handling.
    """
    provider, model = get_llm_backend(kwargs.get("agent_name"))
    try:
        if provider == 'ollama':
            from mvp.ollama_llm import call_ollama
            response = call_ollama(prompt, model=model, **kwargs)
            # If streaming, ensure at least one token is yielded
            if hasattr(response, "__iter__") and not isinstance(response, str):
                yielded = False
                for token in response:
                    yielded = True
                    yield token
                if not yielded:
                    yield "[Ollama error: No response received]"
            else:
                return response
        elif provider == 'openai':
            return "[OpenAI backend not implemented yet]"
        # Removed fake_llm support for production robustness
        else:
            if kwargs.get("stream", False):
                yield "No backend configured"
            else:
                return "No backend configured"
    except Exception as e:
        yield f"[LLM error: {e}]"
