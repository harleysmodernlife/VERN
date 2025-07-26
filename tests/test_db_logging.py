"""
Automated test for VERN MVP DB logging

Validates that actions, logs, and notifications are recorded in db/vern.db.
"""

import sys
import os
import sqlite3

sys.path.insert(0, "./src/mvp")
sys.path.insert(0, "./src/db")

from orchestrator import Orchestrator
from dev_team import DevTeam
from admin import Admin

DB_PATH = "db/vern.db"

def fetch_latest(table, limit=1):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table} ORDER BY timestamp DESC LIMIT ?", (limit,))
        return cursor.fetchall()

def test_feature_request_logging():
    dev_team = DevTeam()
    admin = Admin()
    orchestrator = Orchestrator(dev_team, admin)
    # Simulate feature request
    feature = "weather updates"
    result = dev_team.implement_feature(feature)
    # Check actions table
    actions = fetch_latest("actions")
    assert actions, "No actions logged"
    assert feature in actions[0][5], "Feature request not logged in actions"
    print("Feature request action logged: PASS")

def test_meeting_logging():
    admin = Admin()
    # Simulate meeting scheduling
    details = "chris lunch at 3pm"
    result = admin.schedule_meeting(details)
    # Check actions table
    actions = fetch_latest("actions")
    assert actions, "No actions logged"
    assert details in actions[0][5], "Meeting details not logged in actions"
    print("Meeting scheduling action logged: PASS")

def test_admin_notification_logging():
    admin = Admin()
    msg = "Test notification"
    admin.notify_user(msg)
    # Check logs table
    logs = fetch_latest("logs")
    assert logs, "No logs found"
    assert msg in logs[0][3], "Notification not logged"
    print("Admin notification log: PASS")

def run_tests():
    print("Running DB logging tests...")
    test_feature_request_logging()
    test_meeting_logging()
    test_admin_notification_logging()
    print("All DB logging tests passed.")

if __name__ == "__main__":
    run_tests()
