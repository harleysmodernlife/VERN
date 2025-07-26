"""
FakeLLM module for simulating LLM calls in agent logic layers.

Replace this with a real LLM integration (OpenAI, local, etc.) as needed.
"""

def call_llm(prompt, context=None):
    """
    Simulate an LLM call.
    Args:
        prompt (str): The prompt or instruction for the LLM.
        context (dict, optional): Additional context for the LLM.
    Returns:
        str: Simulated LLM response.
    """
    context_str = f" | Context: {context}" if context else ""
    return f"[FakeLLM] Response to: '{prompt}'{context_str}"
