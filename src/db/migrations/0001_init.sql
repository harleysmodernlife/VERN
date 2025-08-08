-- 0001_init.sql
-- Core logging schema for VERN (idempotent)

BEGIN;

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

COMMIT;