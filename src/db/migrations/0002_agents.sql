-- 0002_agents.sql
-- Agent Registry schema (idempotent). Stores live agent presence/metadata.

BEGIN;

CREATE TABLE IF NOT EXISTS agents (
  name TEXT PRIMARY KEY,
  cluster TEXT,
  status TEXT,
  capabilities TEXT,
  last_seen REAL,
  meta TEXT
);

CREATE INDEX IF NOT EXISTS idx_agents_cluster ON agents(cluster);

COMMIT;