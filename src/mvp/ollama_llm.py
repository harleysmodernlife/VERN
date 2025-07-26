"""
Ollama LLM Wrapper for VERN

Handles sending prompts to Ollama's OpenAI-compatible API for any model.
Supports modular, pluggable LLM backend design.
"""

import requests

OLLAMA_API_URL = "http://localhost:11434/v1/chat/completions"

def generate_ollama(prompt, model="qwen3:0.6b", context=None, max_tokens=256, temperature=0.7, system_prompt=None):
    """
    Send a prompt to Ollama's API and return the response.
    Args:
        prompt (str): The user prompt.
        model (str): The Ollama model name/tag.
        context (list, optional): Conversation history as a list of dicts.
        max_tokens (int): Max tokens to generate.
        temperature (float): Sampling temperature.
        system_prompt (str, optional): System prompt for role/context.
    Returns:
        str: The model's response.
    """
    # Forward-thinking: allow system prompts and flexible context
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if isinstance(context, list):
        messages.extend(context)
    # If context is a dict (agent context), ignore for chat history but could be used for system prompt in future
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False
    }
    try:
        resp = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        return f"[Ollama LLM Error] {e}"

# Example usage (for testing)
if __name__ == "__main__":
    result = generate_ollama("What is VERN and how can it help developers?", model="qwen3:0.6b")
    print("Ollama response:", result)
