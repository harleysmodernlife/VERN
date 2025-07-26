"""
Automated tests for all horizontally scaffolded agents.
Validates instantiation, stub method, and DB logging for each agent.
"""

import sys
import os
import sqlite3

sys.path.insert(0, "./src/mvp")
sys.path.insert(0, "./src/db")

from research import Research
from finance_resource import FinanceResource
from health_wellness import HealthWellness
from learning_education import LearningEducation
from social_relationship import SocialRelationship
from environment_systems import EnvironmentSystems
from legal_compliance import LegalCompliance
from creativity_media import CreativityMedia
from career_work import CareerWork
from travel_logistics import TravelLogistics
from archetype_phoenix import ArchetypePhoenix
from emergent_agent import EmergentAgent
from id10t_monitor import Id10tMonitor

DB_PATH = "db/vern.db"

def fetch_latest(table, limit=1):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table} ORDER BY timestamp DESC LIMIT ?", (limit,))
        return cursor.fetchall()

def test_agent(agent_class, method, arg, log_table, log_field, expected):
    agent = agent_class()
    result = getattr(agent, method)(arg)
    logs = fetch_latest(log_table)
    assert logs, f"No logs found for {agent_class.__name__}"
    assert expected in logs[0][log_field], f"{agent_class.__name__} log missing expected content"
    print(f"{agent_class.__name__} stub: PASS")

def run_tests():
    print("Running horizontal agent scaffold tests...")
    test_agent(Research, "handle_request", "AI research", "actions", 5, "AI research")
    test_agent(FinanceResource, "handle_request", "budget review", "actions", 5, "budget review")
    test_agent(HealthWellness, "handle_request", "wellness check", "actions", 5, "wellness check")
    test_agent(LearningEducation, "handle_request", "learning plan", "actions", 5, "learning plan")
    test_agent(SocialRelationship, "handle_request", "team building", "actions", 5, "team building")
    test_agent(EnvironmentSystems, "handle_request", "system audit", "actions", 5, "system audit")
    test_agent(LegalCompliance, "handle_request", "compliance check", "actions", 5, "compliance check")
    test_agent(CreativityMedia, "handle_request", "media campaign", "actions", 5, "media campaign")
    test_agent(CareerWork, "handle_request", "career coaching", "actions", 5, "career coaching")
    test_agent(TravelLogistics, "handle_request", "trip planning", "actions", 5, "trip planning")
    test_agent(ArchetypePhoenix, "integrate", "integration test", "actions", 5, "integration test")
    test_agent(EmergentAgent, "handle_request", "emergent scenario", "actions", 5, "emergent scenario")
    test_agent(Id10tMonitor, "sanity_check", "sanity test", "actions", 5, "sanity test")
    print("All horizontal agent scaffold tests passed.")

if __name__ == "__main__":
    run_tests()
