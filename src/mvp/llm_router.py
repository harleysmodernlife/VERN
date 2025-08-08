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

import asyncio

async def route_llm_call_async(prompt, **kwargs):
    """
    Async version: Routes the prompt to the selected LLM backend/model.
    Returns a string or a generator (for streaming).
    Includes robust error handling.
    """
    provider, model = get_llm_backend(kwargs.get("agent_name"))
    stream = kwargs.get("stream", False)
    # Ensure model is always a string
    if not model:
        model = "qwen3:0.6b"
    try:
        if provider == 'ollama':
            from mvp.ollama_llm import call_ollama
            if asyncio.iscoroutinefunction(call_ollama):
                response = await call_ollama(prompt, model=model, **kwargs)
            else:
                loop = asyncio.get_event_loop()
                # Only pass prompt and model as positional args, rest as kwargs
                response = await loop.run_in_executor(None, lambda: call_ollama(prompt, model=model, **kwargs))
            if stream and hasattr(response, "__iter__") and not isinstance(response, str):
                for token in response:
                    yield token
            else:
                # If not streaming, join tokens if response is iterable, else return string
                if hasattr(response, "__iter__") and not isinstance(response, str):
                    result = "".join(str(token) for token in response)
                    yield result
                else:
                    yield response
        elif provider == 'openai':
            yield {"error": "OpenAI backend not implemented yet", "code": "OPENAI_NOT_IMPLEMENTED"}
        else:
            yield {"error": "No backend configured", "code": "NO_BACKEND_CONFIGURED"}
    except Exception as e:
        yield {"error": str(e), "code": "LLM_ERROR"}

def route_llm_call(prompt, **kwargs):
    """
    Sync wrapper for backward compatibility.
    Returns a string if stream=False, else returns an iterator.
    """
    stream = kwargs.get("stream", False)
    coro = route_llm_call_async(prompt, **kwargs)
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If already in an event loop, just return the coroutine (caller must await)
            return coro
        else:
            if stream:
                # Consume async generator and yield tokens synchronously
                async def consume():
                    result = []
                    async for token in coro:
                        result.append(token)
                    return result
                # Await the coroutine to get the async generator, then iterate
                async_gen = loop.run_until_complete(coro)
                for token in async_gen:
                    yield token
            else:
                # Await the coroutine and concatenate all results into a string
                async def get_full_string():
                    gen = await coro
                    result = ""
                    for chunk in gen:
                        result += str(chunk)
                    return result
                return loop.run_until_complete(get_full_string())
    except Exception as e:
        return {"error": str(e), "code": "LLM_ERROR"}
