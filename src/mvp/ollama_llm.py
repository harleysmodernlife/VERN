"""
Ollama LLM Backend for VERN (Debug Streaming, Toggleable)
---------------------------------------------------------
Calls the local Ollama server for real LLM responses.
Debug output for every streamed line is now toggleable via DEBUG_OLLAMA environment variable.
"""

import requests
import os

DEBUG_OLLAMA = os.environ.get("DEBUG_OLLAMA", "0") == "1"

def call_ollama(prompt, model="qwen3:0.6b", timeout=600, stream=False, **kwargs):
    """
    Calls the local Ollama server for a real LLM response.
    Timeout is now configurable (default 600s = 10min).
    If stream=True, returns tokens as they arrive (generator).
    Prints every line received for debugging if DEBUG_OLLAMA=1.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    try:
        if stream:
            with requests.post(url, json=payload, timeout=timeout, stream=True) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        try:
                            data = line.decode("utf-8")
                            if DEBUG_OLLAMA:
                                print("[Ollama DEBUG] Raw line:", data)
                            import json
                            token = json.loads(data).get("response", "")
                            if token:
                                yield token
                            else:
                                if DEBUG_OLLAMA:
                                    yield f"[Ollama DEBUG] No 'response' field: {data}"
                        except Exception as e:
                            if DEBUG_OLLAMA:
                                yield f"[Ollama DEBUG] Exception parsing line: {e} | Raw: {line}"
        else:
            response = requests.post(url, json=payload, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
    except requests.exceptions.Timeout:
        if stream:
            yield f"[Ollama error: Timeout after {timeout}s]"
        else:
            return f"[Ollama error: Timeout after {timeout}s]"
    except Exception as e:
        if stream:
            yield f"[Ollama error: {e}]"
        else:
            return f"[Ollama error: {e}]"
