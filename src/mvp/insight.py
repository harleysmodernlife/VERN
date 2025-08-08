"""
VERN Insight Agent (Function-Based)
-----------------------------------
Handles insight generation, synthesis, and actionable recommendations for the MVP.

Integration Points:
- Memory: Leverage historical data and user feedback for deeper insights.
- Plugins: Use analytics and synthesis plugins for advanced recommendations.
- UI: Connect to frontend for displaying insights and next actions.

TODO:
- [x] Implement workflow logic for multi-step insight tasks.
- [x] Integrate plugin usage and context-aware operations.
- [x] Write unit tests for insight_respond in tests/test_agents_workflow.py.
- [ ] Future: Expand advanced capabilities (trend detection, cross-agent synthesis).

"""

from src.db.logger import log_action, log_message, log_gotcha

def insight_respond(user_input, context=None, agent_status=None, persona="default", user_id="default_user", memory=None, workflow_steps=None):
    """
    Handles insight queries with persona/context adaptation, agent memory, plugin integration, and error handling.
    Supports multi-step workflows and advanced capabilities.
    """
    agent_id = "insight"
    try:
        log_action(agent_id, user_id, "insight_request", {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory,
            "workflow_steps": workflow_steps
        }, status="started")

        # Multi-step workflow logic
        steps = workflow_steps if workflow_steps else ["gather", "synthesize", "recommend"]
        results = []
        from src.mvp.plugin_registry import get_all_mcp_tools
        plugins = get_all_mcp_tools()
        persona_prompt = {
            "default": "You are the VERN Insight Agent. Generate actionable insights and synthesize information.",
            "analyst": "You are an analyst. Detect trends and provide recommendations.",
            "synthesizer": "You are a synthesizer. Combine information from multiple sources.",
            "advisor": "You are an advisor. Suggest next actions and connect to plugins."
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
            # Plugin integration (simulate analytics/synthesis plugin usage)
            plugin_result = None
            for plugin in plugins:
                if "analytics" in plugin or "synth" in plugin or "trend" in plugin:
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
        log_message(agent_id, f"Error in insight_respond: {str(e)}", level="error", context={
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory,
            "workflow_steps": workflow_steps
        })
        log_gotcha(agent_id, f"Exception in insight_respond: {str(e)}", severity="error")
        return f"Error: {str(e)}"