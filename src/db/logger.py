"""
VERN DB Logger API (MVP)

Provides functions to log actions, handoffs, gotchas, and general logs to the SQLite database.
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = "db/vern.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def log_action(agent_id, user_id, action_type, payload, status="success", gotcha_id=None, tags=None):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO actions (timestamp, agent_id, user_id, action_type, payload, status, gotcha_id, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.utcnow(), agent_id, user_id, action_type, json.dumps(payload), status, gotcha_id, json.dumps(tags) if tags else None)
        )
        conn.commit()

def log_handoff(from_agent_id, to_agent_id, action_id, notes="", gotcha_id=None, context_snapshot=None):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO handoffs (from_agent_id, to_agent_id, action_id, timestamp, notes, gotcha_id, context_snapshot) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (from_agent_id, to_agent_id, action_id, datetime.utcnow(), notes, gotcha_id, json.dumps(context_snapshot) if context_snapshot else None)
        )
        conn.commit()

def log_gotcha(agent_id, description, severity="warning", resolved=False, resolution_notes=None, related_action_id=None, related_handoff_id=None):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO gotchas (timestamp, agent_id, description, severity, resolved, resolution_notes, related_action_id, related_handoff_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.utcnow(), agent_id, description, severity, int(resolved), resolution_notes, related_action_id, related_handoff_id)
        )
        conn.commit()

def log_message(agent_id, message, level="info", context=None):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO logs (timestamp, agent_id, message, level, context) VALUES (?, ?, ?, ?, ?)",
            (datetime.utcnow(), agent_id, message, level, json.dumps(context) if context else None)
        )
        conn.commit()
