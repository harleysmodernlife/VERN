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
        from mvp.llm_router import route_llm_call
        from mvp.prompt_utils import build_prompt
        persona_descriptions = {
            "default": "Analyze requirements, generate a code plan, and provide a code snippet or actionable steps.",
            "architect": "Design scalable, maintainable solutions and explain tradeoffs.",
            "mentor": "Teach best practices and guide the user step-by-step.",
            "reviewer": "Point out flaws, suggest improvements, and enforce standards.",
            "rapid": "Deliver quick, working code with minimal boilerplate."
        }
        context = context or {}
        context["persona_description"] = persona_descriptions.get(persona, persona_descriptions["default"])
        prompt = build_prompt(
            agent_name="dev_team",
            task=user_input,
            context=context,
            persona=persona
        )
        response = route_llm_call(prompt, context=context, agent_status=agent_status, agent_name="dev_team")
        if hasattr(response, "__iter__") and not isinstance(response, str):
            response = "".join(list(response))
        return response

    def implement_feature(self, user_input, context=None, agent_status=None, persona="default", memory=None):
        # Alias for respond, for test compatibility
        return self.respond(user_input, context=context, agent_status=agent_status, persona=persona, memory=memory)

from src.mvp.agent_utils import log_agent_action, log_agent_message, log_agent_exception, escalate_to_orchestrator

def dev_team_respond(user_input, context=None, agent_status=None, persona="default", user_id="default_user", memory=None):
    """
    Handles feature/code requests with logging, persona/context adaptation, agent memory, and error handling.
    """
    agent_id = "dev_team"
    try:
        log_agent_action(agent_id, user_id, "dev_request", {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        }, status="started")

        # Memory subsystem integration example
        import requests
        memory_api = "http://localhost:8000/memory"
        # Add/update agent context as entity
        entity_payload = {
            "entity_id": user_id,
            "properties": {
                "last_request": user_input,
                "persona": persona,
                "agent_status": agent_status
            }
        }
        try:
            requests.post(f"{memory_api}/entity", json=entity_payload, timeout=2)
        except Exception:
            pass  # Ignore if memory API is not running

        from mvp.llm_router import route_llm_call
        from mvp.prompt_utils import build_prompt
        persona_descriptions = {
            "default": "Analyze requirements, generate a code plan, and provide a code snippet or actionable steps.",
            "architect": "Design scalable, maintainable solutions and explain tradeoffs.",
            "mentor": "Teach best practices and guide the user step-by-step.",
            "reviewer": "Point out flaws, suggest improvements, and enforce standards.",
            "rapid": "Deliver quick, working code with minimal boilerplate."
        }
        context = context or {}
        context["persona_description"] = persona_descriptions.get(persona, persona_descriptions["default"])
        prompt = build_prompt(
            agent_name="dev_team",
            task=user_input,
            context=context,
            persona=persona
        )
        response = route_llm_call(prompt, context=context, agent_status=agent_status, agent_name="dev_team")
        log_agent_action(agent_id, user_id, "llm_response", {
            "prompt": prompt,
            "response": str(response),
            "persona": persona,
            "memory": memory
        })
        # If response is a generator, join its output
        if hasattr(response, "__iter__") and not isinstance(response, str):
            response = "".join(list(response))
        # Patch: If backend returns structured error, escalate to orchestrator for error handling
        if isinstance(response, dict) and "error" in response:
            from mvp.orchestrator import orchestrator_respond
            error_context = {
                "user_input": user_input,
                "context": context,
                "agent_status": agent_status,
                "persona": persona,
                "memory": memory,
                "error": response.get("error"),
                "error_code": response.get("code")
            }
            return orchestrator_respond(
                f"Dev Team Agent encountered a backend error: {response.get('error')} (code: {response.get('code')}). Please escalate or suggest next steps.",
                error_context,
                agent_status,
                user_id
            )
        return response

    except Exception as e:
        log_agent_message(agent_id, f"Error in dev_team_respond: {str(e)}", level="error", context={
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        })
        log_agent_exception(agent_id, f"Exception in dev_team_respond: {str(e)}", severity="error")
        error_context = {
            "user_input": user_input,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory,
            "error": str(e)
        }
        return escalate_to_orchestrator(
            f"Dev Team Agent encountered an error: {str(e)}. Please escalate or suggest next steps.",
            error_context,
            agent_status,
            user_id
        )
