"""
VERN Orchestrator Agent (LLM-Powered, Multi-Agent)
-------------------------------------------------
Routes user input, delegates to clusters, aggregates results, and manages priorities.
"""

from src.mvp.qwen3_llm import call_qwen3
from src.mvp.research import research_respond
from src.mvp.finance_resource import finance_respond
from src.mvp.health_wellness import health_respond
from src.mvp.admin import admin_respond
from src.mvp.learning_education import learning_respond
from src.mvp.social_relationship import social_respond
from src.mvp.environment_systems import environment_respond
from src.mvp.legal_compliance import legal_respond
from src.mvp.creativity_media import creativity_respond
from src.mvp.career_work import career_respond
from src.mvp.travel_logistics import travel_respond
from src.mvp.security_privacy import security_respond
from src.mvp.archetype_phoenix import archetype_respond
from src.mvp.emergent_agent import emergent_respond
from src.mvp.knowledge_broker import knowledge_broker_respond
from src.mvp.id10t_monitor import id10t_monitor_respond

# Map cluster names to agent functions
CLUSTER_AGENTS = {
    "research": research_respond,
    "finance": finance_respond,
    "health": health_respond,
    "admin": admin_respond,
    "learning": learning_respond,
    "social": social_respond,
    "environment": environment_respond,
    "legal": legal_respond,
    "creativity": creativity_respond,
    "career": career_respond,
    "travel": travel_respond,
    "security": security_respond,
    "archetype": archetype_respond,
    "emergent": emergent_respond,
    "knowledge_broker": knowledge_broker_respond,
    "id10t_monitor": id10t_monitor_respond,
}

def orchestrator_respond(user_input, context, agent_status=None):
    """
    Orchestrator LLM: routes, delegates, and aggregates multi-agent responses.
    """
    # Step 1: Ask the LLM which clusters to involve and what plan to follow
    plan_prompt = (
        "You are the Orchestrator Agent in the VERN system. "
        "Your job is to read the user's message, recent context, and agent status, then decide which agent clusters should be involved. "
        "Output a plan of action as a JSON list of clusters to involve (e.g., [\"research\", \"finance\"]) and a brief plan summary. "
        "If the user request is simple, you may answer directly. Otherwise, delegate to the relevant clusters and aggregate their responses.\n\n"
        f"Context: {context}\n"
        f"Agent Status: {agent_status}\n"
        f"User: {user_input}\n"
        "Orchestrator:"
    )
    llm_response = call_qwen3(plan_prompt)
    # Try to extract clusters and plan from LLM output
    import re, json
    clusters = []
    plan_summary = ""
    match = re.search(r"\[([^\]]+)\]", llm_response)
    if match:
        try:
            clusters = json.loads("[" + match.group(1) + "]")
        except Exception:
            clusters = []
    # Fallback: look for cluster names in text if JSON parse fails
    if not clusters:
        for name in CLUSTER_AGENTS:
            if name in llm_response.lower():
                clusters.append(name)
    # Extract plan summary (text after the cluster list)
    plan_match = re.search(r"\]\s*(.+)", llm_response)
    if plan_match:
        plan_summary = plan_match.group(1).strip()
    else:
        plan_summary = llm_response.strip()
    # Step 2: Delegate to clusters and aggregate results
    results = []
    for cluster in clusters:
        fn = CLUSTER_AGENTS.get(cluster.lower())
        if fn:
            result = fn(user_input, context, agent_status)
            results.append(f"[{cluster.capitalize()}]: {result}")
    # Step 3: Aggregate and return
    if results:
        return f"(plan: {plan_summary})\n" + "\n".join(results)
    else:
        # If no clusters, fallback to Orchestrator LLM direct answer
        return llm_response
