"""
VERN Dev Team Agent (Function-Based)
------------------------------------
Handles feature/code requests for the MVP.
"""

class DevTeam:
    """
    Enhanced DevTeam class with persona tuning, agent memory/context, and workflow support.
    """
    def respond(self, user_input, context=None, agent_status=None, persona="default", memory=None):
        from src.mvp.llm_router import route_llm_call
        persona_prompt = {
            "default": "You are the VERN Dev Team Agent. Analyze requirements, generate a code plan, and provide a code snippet or actionable steps.",
            "architect": "You are a senior software architect. Design scalable, maintainable solutions and explain tradeoffs.",
            "mentor": "You are a friendly coding mentor. Teach best practices and guide the user step-by-step.",
            "reviewer": "You are a strict code reviewer. Point out flaws, suggest improvements, and enforce standards.",
            "rapid": "You are a rapid prototyper. Deliver quick, working code with minimal boilerplate."
        }
        prompt = (
            persona_prompt.get(persona, persona_prompt["default"]) + "\n"
            f"Request: {user_input}\n"
            f"Context: {context}\n"
            f"Agent Status: {agent_status}\n"
            f"Persona: {persona}\n"
            f"Memory: {memory}\n"
        )
        response = route_llm_call(prompt, context=context, agent_status=agent_status, agent_name="dev_team")
        if hasattr(response, "__iter__") and not isinstance(response, str):
            response = "".join(list(response))
        return response

    def implement_feature(self, user_input, context=None, agent_status=None, persona="default", memory=None):
        # Alias for respond, for test compatibility
        return self.respond(user_input, context=context, agent_status=agent_status, persona=persona, memory=memory)

from db.logger import log_action, log_message, log_gotcha

def dev_team_respond(user_input, context=None, agent_status=None, persona="default", user_id="default_user", memory=None):
    """
    Handles feature/code requests with logging, persona/context adaptation, agent memory, and error handling.
    """
    agent_id = "dev_team"
    try:
        log_action(agent_id, user_id, "dev_request", {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        }, status="started")

        from src.mvp.llm_router import route_llm_call
        persona_prompt = {
            "default": "You are the VERN Dev Team Agent. Analyze requirements, generate a code plan, and provide a code snippet or actionable steps.",
            "architect": "You are a senior software architect. Design scalable, maintainable solutions and explain tradeoffs.",
            "mentor": "You are a friendly coding mentor. Teach best practices and guide the user step-by-step.",
            "reviewer": "You are a strict code reviewer. Point out flaws, suggest improvements, and enforce standards.",
            "rapid": "You are a rapid prototyper. Deliver quick, working code with minimal boilerplate."
        }
        prompt = (
            persona_prompt.get(persona, persona_prompt["default"]) + "\n"
            f"Request: {user_input}\n"
            f"Context: {context}\n"
            f"Agent Status: {agent_status}\n"
            f"Persona: {persona}\n"
            f"Memory: {memory}\n"
        )
        response = route_llm_call(prompt, context=context, agent_status=agent_status, agent_name="dev_team")
        log_action(agent_id, user_id, "llm_response", {
            "prompt": prompt,
            "response": str(response),
            "persona": persona,
            "memory": memory
        })
        # If response is a generator, join its output
        if hasattr(response, "__iter__") and not isinstance(response, str):
            response = "".join(list(response))
        # Patch: If backend is not configured, escalate to orchestrator for error handling
        if "No backend configured" in response or "[Ollama error: No response received]" in response:
            from src.mvp.orchestrator import orchestrator_respond
            error_context = {
                "user_input": user_input,
                "context": context,
                "agent_status": agent_status,
                "persona": persona,
                "memory": memory,
                "error": response
            }
            return orchestrator_respond(
                f"Dev Team Agent encountered a backend error: {response}. Please escalate or suggest next steps.",
                error_context,
                agent_status,
                user_id
            )
        return response

    except Exception as e:
        log_message(agent_id, f"Error in dev_team_respond: {str(e)}", level="error", context={
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        })
        log_gotcha(agent_id, f"Exception in dev_team_respond: {str(e)}", severity="error")
        from src.mvp.orchestrator import orchestrator_respond
        error_context = {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory,
            "error": str(e)
        }
        return orchestrator_respond(
            f"Dev Team Agent encountered an error: {str(e)}. Please escalate or suggest next steps.",
            error_context,
            agent_status,
            user_id
        )
