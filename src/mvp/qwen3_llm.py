"""
Qwen3 LLM Integration for VERN
------------------------------
Provides a simple interface to call Qwen3-0.6B via Ollama for agent reasoning.
"""

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:0.6b"

def call_qwen3(prompt, system_prompt=None, temperature=0.2, max_tokens=512):
    """
    Calls Qwen3-0.6B via Ollama and returns the generated response.
    """
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
    }
    if system_prompt:
        payload["system"] = system_prompt
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=180)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except Exception as e:
        return f"[Qwen3 LLM error: {e}]"
