"""
VERN Knowledge Broker Agent (Function-Based)
--------------------------------------------
Handles context lookup and cross-cluster queries for the MVP.
"""

class KnowledgeBroker:
    """
    Enhanced KnowledgeBroker class with persona tuning, agent memory/context, and workflow support.
    """
    def lookup(self, query, context=None, agent_status=None, persona="default", memory=None):
        from mvp.llm_router import route_llm_call
        from mvp.prompt_utils import build_prompt
        persona_descriptions = {
            "default": "Search context, documents, and knowledge bases, and provide a concise, actionable answer.",
            "researcher": "Provide deep, well-cited answers and suggest next steps.",
            "summarizer": "Boil down complex information into clear, digestible points.",
            "advisor": "Recommend actions and connect the user to relevant agents or plugins.",
            "cross_cluster": "Aggregate responses from multiple clusters and synthesize a unified answer."
        }
        context = context or {}
        context["persona_description"] = persona_descriptions.get(persona, persona_descriptions["default"])
        prompt = build_prompt(
            agent_name="knowledge_broker",
            task=query,
            context=context,
            persona=persona
        )
        return route_llm_call(prompt, context=context, agent_status=agent_status)

    def context_lookup(self, query, context=None, agent_status=None, persona="default", memory=None):
        # Alias for lookup, for test compatibility
        return self.lookup(query, context=context, agent_status=agent_status, persona=persona, memory=memory)

from src.db.logger import log_action, log_message, log_gotcha

def knowledge_broker_context_lookup(query, context=None, agent_status=None, persona="default", user_id="default_user", memory=None):
    """
    Handles context lookup requests with logging, persona/context adaptation, agent memory, and error handling.
    """
    agent_id = "knowledge_broker"
    try:
        log_action(agent_id, user_id, "context_lookup", {
            "query": query,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        }, status="started")

        from mvp.llm_router import route_llm_call
        from mvp.prompt_utils import build_prompt
        from mvp.llm_router import route_llm_call
        from mvp.prompt_utils import build_prompt
        persona_descriptions = {
            "default": "Search context, documents, and knowledge bases, and provide a concise, actionable answer.",
            "researcher": "Provide deep, well-cited answers and suggest next steps.",
            "summarizer": "Boil down complex information into clear, digestible points.",
            "advisor": "Recommend actions and connect the user to relevant agents or plugins.",
            "cross_cluster": "Aggregate responses from multiple clusters and synthesize a unified answer."
        }
        context = context or {}
        context["persona_description"] = persona_descriptions.get(persona, persona_descriptions["default"])
        prompt = build_prompt(
            agent_name="knowledge_broker",
            task=query,
            context=context,
            persona=persona
        )
        response = route_llm_call(prompt, context=context, agent_status=agent_status)
        log_action(agent_id, user_id, "llm_response", {
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
            try:
                from mvp.orchestrator import orchestrator_respond
                error_context = {
                    "query": query,
                    "context": context,
                    "agent_status": agent_status,
                    "persona": persona,
                    "memory": memory,
                    "error": response.get("error"),
                    "error_code": response.get("code")
                }
                return orchestrator_respond(
                    f"Knowledge Broker Agent encountered a backend error: {response.get('error')} (code: {response.get('code')}). Please escalate or suggest next steps.",
                    error_context,
                    agent_status,
                    user_id
                )
            except Exception as orchestrator_error:
                log_gotcha(agent_id, f"Orchestrator escalation failed: {str(orchestrator_error)}", severity="critical")
                return f"Critical error: Knowledge Broker and Orchestrator both failed. Details: {str(orchestrator_error)}"
        return response

    except Exception as e:
        log_message(agent_id, f"Error in knowledge_broker_context_lookup: {str(e)}", level="error", context={
            "query": query,
            "context": context,
            "agent_status": agent_status,
            "persona": persona,
            "memory": memory
        })
        log_gotcha(agent_id, f"Exception in knowledge_broker_context_lookup: {str(e)}", severity="error")
        # Escalate to orchestrator for fallback handling
        try:
            from mvp.orchestrator import orchestrator_respond
            fallback_context = {
                "error": str(e),
                "agent": agent_id,
                "query": query,
                "context": context,
                "agent_status": agent_status,
                "persona": persona,
                "memory": memory
            }
            return orchestrator_respond(
                f"[Knowledge Broker Escalation] {query}",
                fallback_context,
                agent_status
            )
        except Exception as orchestrator_error:
            log_gotcha(agent_id, f"Orchestrator escalation failed: {str(orchestrator_error)}", severity="critical")
            return f"Critical error: Knowledge Broker and Orchestrator both failed. Details: {str(orchestrator_error)}"

def knowledge_broker_cross_cluster_query(req, context=None, agent_status=None, persona="default", memory=None):
    """
    Handles cross-cluster query requests with persona/context adaptation and agent memory.
    """
    from mvp.llm_router import route_llm_call
    from mvp.prompt_utils import build_prompt
    persona_descriptions = {
        "default": "Coordinate with relevant agent clusters, aggregate their responses, and provide a unified, actionable answer.",
        "cross_cluster": "Aggregate responses from multiple clusters and synthesize a unified answer."
    }
    context = context or {}
    context["persona_description"] = persona_descriptions.get(persona, persona_descriptions["default"])
    prompt = build_prompt(
        agent_name="knowledge_broker",
        task=req,
        context=context,
        persona=persona
    )
    return route_llm_call(prompt, context=context, agent_status=agent_status)
