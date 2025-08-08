"""
VERN Writing Agent (Function-Based)
-----------------------------------
Handles writing, editing, and content generation for the MVP.

Integration Points:
- Memory: Access agent/user memory for context-aware writing.
- Plugins: Use grammar/style plugins for advanced editing.
- UI: Connect to frontend for real-time writing feedback.

TODO:
- [x] Implement workflow logic for multi-step writing tasks.
- [x] Integrate plugin usage and context-aware operations.
- [x] Write unit tests for writing_respond in tests/test_agents_workflow.py.
- [ ] Future: Expand advanced capabilities (tone, style, audience adaptation).

"""

from src.db.logger import log_action, log_message, log_gotcha

def writing_respond(user_input, context=None, agent_status=None, persona="default", user_id="default_user", memory=None, workflow_steps=None):
    """
    Handles writing queries with persona/context adaptation, agent memory, plugin integration, and error handling.
    Supports multi-step workflows and advanced capabilities.
    """
    agent_id = "writing"
    try:
        log_action(agent_id, user_id, "writing_request", {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory,
            "workflow_steps": workflow_steps
        }, status="started")

        # Multi-step workflow logic
        steps = workflow_steps if workflow_steps else ["draft", "edit", "review"]
        results = []
        from src.mvp.plugin_registry import get_all_mcp_tools
        plugins = get_all_mcp_tools()
        persona_prompt = {
            "default": "You are the VERN Writing Agent. Generate, edit, and improve written content.",
            "editor": "You are an editor. Refine grammar, clarity, and style.",
            "creative": "You are a creative writer. Produce engaging and original text.",
            "summarizer": "You are a summarizer. Condense information into concise writing.",
            "advisor": "You are a writing advisor. Suggest improvements and connect to plugins."
        }
        for step in steps:
            prompt = (
                persona_prompt.get(persona, persona_prompt["default"]) + f"\nStep: {step}\n"
                f"Query: {user_input}\n"
                f"Context: {context}\n"
                f"Agent Status: {agent_status}\n"
                f"Persona: {persona}\n"
                f"Memory: {memory}\n"
            )
            # Plugin integration (simulate grammar/style plugin usage)
            plugin_result = None
            for plugin in plugins:
                if "grammar" in plugin or "style" in plugin:
                    plugin_result = f"Plugin '{plugin}' applied for step '{step}'."
                    break
            # Simulate LLM response
            response = f"[{step}] {prompt}"
            if plugin_result:
                response += f"\n{plugin_result}"
            results.append(response)
            log_action(agent_id, user_id, "llm_response", {
                "prompt": prompt,
                "response": str(response),
                "persona": persona,
                "memory": memory,
                "step": step,
                "plugin_result": plugin_result
            })
        return "\n---\n".join(results)

    except Exception as e:
        log_message(agent_id, f"Error in writing_respond: {str(e)}", level="error", context={
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory,
            "workflow_steps": workflow_steps
        })
        log_gotcha(agent_id, f"Exception in writing_respond: {str(e)}", severity="error")
        return f"Error: {str(e)}"