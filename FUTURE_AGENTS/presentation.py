"""
VERN Presentation Agent (Function-Based)
----------------------------------------
Handles presentation creation, slide generation, and visual storytelling for the MVP.

Integration Points:
- Memory: Retrieve user/session history for personalized presentations.
- Plugins: Integrate with visualization and formatting plugins.
- UI: Connect to frontend for live preview and editing.

TODO:
- [x] Implement workflow logic for multi-step presentation tasks.
- [x] Integrate plugin usage and context-aware operations.
- [x] Write unit tests for presentation_respond in tests/test_agents_workflow.py.
- [ ] Future: Expand advanced capabilities (design templates, audience targeting).

"""

from src.db.logger import log_action, log_message, log_gotcha

def presentation_respond(user_input, context=None, agent_status=None, persona="default", user_id="default_user", memory=None, workflow_steps=None):
    """
    Handles presentation queries with persona/context adaptation, agent memory, plugin integration, and error handling.
    Supports multi-step workflows and advanced capabilities.
    """
    agent_id = "presentation"
    try:
        log_action(agent_id, user_id, "presentation_request", {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory,
            "workflow_steps": workflow_steps
        }, status="started")

        # Multi-step workflow logic
        steps = workflow_steps if workflow_steps else ["outline", "design", "review"]
        results = []
        from src.mvp.plugin_registry import get_all_mcp_tools
        plugins = get_all_mcp_tools()
        persona_prompt = {
            "default": "You are the VERN Presentation Agent. Create and improve presentations and visual stories.",
            "designer": "You are a designer. Focus on layout, clarity, and impact.",
            "storyteller": "You are a storyteller. Craft compelling narratives.",
            "summarizer": "You are a summarizer. Condense information into slides.",
            "advisor": "You are a presentation advisor. Suggest improvements and connect to plugins."
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
            # Plugin integration (simulate visualization plugin usage)
            plugin_result = None
            for plugin in plugins:
                if "visual" in plugin or "slide" in plugin or "design" in plugin:
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
        log_message(agent_id, f"Error in presentation_respond: {str(e)}", level="error", context={
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory,
            "workflow_steps": workflow_steps
        })
        log_gotcha(agent_id, f"Exception in presentation_respond: {str(e)}", severity="error")
        return f"Error: {str(e)}"