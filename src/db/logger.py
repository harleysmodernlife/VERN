"""
VERN DB Logger API (MVP)

Provides functions to log actions, handoffs, gotchas, and general logs to the SQLite database.
This version uses the backend's canonical DB path resolver and auto-initializes schema.
"""

import sqlite3
import json
import os
from datetime import datetime, timezone

# Align DB path with backend helper; fall back to env/default if unavailable
try:
    from vern_backend.app.db_path import get_sqlite_path
    DB_PATH = get_sqlite_path()
except Exception:
    DB_PATH = os.environ.get("SQLITE_DB_PATH", "/app/data/vern.sqlite")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS actions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,
  agent_id TEXT,
  user_id TEXT,
  action_type TEXT,
  payload TEXT,
  status TEXT,
  gotcha_id INTEGER,
  tags TEXT
);
CREATE TABLE IF NOT EXISTS handoffs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  from_agent_id TEXT,
  to_agent_id TEXT,
  action_id INTEGER,
  timestamp TEXT NOT NULL,
  notes TEXT,
  gotcha_id INTEGER,
  context_snapshot TEXT
);
CREATE TABLE IF NOT EXISTS gotchas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,
  agent_id TEXT,
  description TEXT,
  severity TEXT,
  resolved INTEGER,
  resolution_notes TEXT,
  related_action_id INTEGER,
  related_handoff_id INTEGER
);
CREATE TABLE IF NOT EXISTS logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,
  agent_id TEXT,
  message TEXT,
  level TEXT,
  context TEXT
);
"""

def _ensure_parent_dir(path: str):
    parent = os.path.dirname(path or "")
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

def _init_schema(conn: sqlite3.Connection):
    conn.executescript(SCHEMA_SQL)
    conn.commit()

def get_conn():
    _ensure_parent_dir(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    # Initialize schema on first connect
    _init_schema(conn)
    return conn

def log_action(agent_id, user_id, action_type, payload, status="success", gotcha_id=None, tags=None):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO actions (timestamp, agent_id, user_id, action_type, payload, status, gotcha_id, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), agent_id, user_id, action_type, json.dumps(payload), status, gotcha_id, json.dumps(tags) if tags else None)
        )
        conn.commit()

def log_handoff(from_agent_id, to_agent_id, action_id, notes="", gotcha_id=None, context_snapshot=None):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO handoffs (from_agent_id, to_agent_id, action_id, timestamp, notes, gotcha_id, context_snapshot) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (from_agent_id, to_agent_id, action_id, datetime.now(timezone.utc).isoformat(), notes, gotcha_id, json.dumps(context_snapshot) if context_snapshot else None)
        )
        conn.commit()

def log_gotcha(agent_id, description, severity="warning", resolved=False, resolution_notes=None, related_action_id=None, related_handoff_id=None):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO gotchas (timestamp, agent_id, description, severity, resolved, resolution_notes, related_action_id, related_handoff_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), agent_id, description, severity, int(resolved), resolution_notes, related_action_id, related_handoff_id)
        )
        conn.commit()

def log_message(agent_id, message, level="info", context=None):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO logs (timestamp, agent_id, message, level, context) VALUES (?, ?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), agent_id, message, level, json.dumps(context) if context else None)
        )
        conn.commit()
