"""
prompt_utils.py

Centralized utilities for constructing agent prompts in VERN.
All agents should use these functions for prompt assembly to ensure consistency and maintainability.

Functions:
    - build_prompt(agent_name, task, context, persona=None, tools=None): Returns a standardized prompt string.
    - sanitize_prompt(prompt): Cleans and formats prompt text.
    - add_tool_descriptions(prompt, tools): Appends tool descriptions to the prompt.

Unit tests for these functions should be added in tests/test_prompt_utils.py.
"""

from typing import Optional, List, Dict

def build_prompt(agent_name: str, task: str, context: Dict, persona: Optional[str] = None, tools: Optional[List[str]] = None) -> str:
    """
    Assemble a standardized prompt for an agent.
    """
    prompt = f"Agent: {agent_name}\nTask: {task}\nContext: {context}\n"
    if persona:
        prompt += f"Persona: {persona}\n"
    if tools:
        prompt += f"Available Tools: {', '.join(tools)}\n"
    return sanitize_prompt(prompt)

def sanitize_prompt(prompt: str) -> str:
    """
    Clean and format prompt text (e.g., strip whitespace, normalize line endings).
    """
    return prompt.strip().replace('\r\n', '\n')

def add_tool_descriptions(prompt: str, tools: Optional[List[str]]) -> str:
    """
    Append tool descriptions to the prompt.
    """
    if not tools:
        return prompt
    tool_desc = "\nTool Descriptions:\n" + "\n".join([f"- {tool}" for tool in tools])
    return f"{prompt}\n{tool_desc}"

# TODO: Add more utility functions as needed for prompt construction.
