"""
Startup Import Self-Test for VERN

Attempts to import all major modules and prints any import errors.
Run this script before starting the backend to verify import hygiene.

Usage:
    python scripts/check_imports.py
"""

import sys

MODULES = [
    "src.db.logger",
    "src.db.init_db",
    "src.mvp.admin",
    "src.mvp.agent_utils",
    "src.mvp.career_work",
    "src.mvp.creativity_media",
    "src.mvp.dev_team_agent",
    "src.mvp.emergent_agent",
    "src.mvp.environment_systems",
    "src.mvp.finance_resource",
    "src.mvp.health_wellness",
    "src.mvp.id10t_monitor",
    "src.mvp.knowledge_broker",
    "src.mvp.legal_compliance",
    "src.mvp.llm_router",
    "src.mvp.orchestrator",
    "src.mvp.plugin_registry",
    "src.mvp.prompt_utils",
    "src.mvp.research",
    "src.mvp.security_privacy",
    "src.mvp.social_relationship",
    "src.mvp.travel_logistics",
    "src.mvp.archetype_phoenix",
    "src.mvp.context_builder",
    "src.mvp.user_profile",
    "src.mvp.vision_agent",
    "src.mvp.voice_agent",
    "src.mvp.mcp_server"
]

def check_import(module):
    try:
        __import__(module)
        print(f"[OK] {module}")
    except Exception as e:
        print(f"[ERROR] {module}: {e}")

if __name__ == "__main__":
    print("VERN Startup Import Self-Test\n-----------------------------")
    for mod in MODULES:
        check_import(mod)
