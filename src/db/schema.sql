-- VERN Core Database Schema (SQLite)

CREATE TABLE IF NOT EXISTS clusters (
    cluster_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agents (
    agent_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cluster TEXT,
    role TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    profile_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS actions (
    action_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    agent_id INTEGER,
    user_id INTEGER,
    action_type TEXT,
    payload TEXT,
    status TEXT,
    gotcha_id INTEGER,
    tags TEXT,
    FOREIGN KEY(agent_id) REFERENCES agents(agent_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(gotcha_id) REFERENCES gotchas(gotcha_id)
);

CREATE TABLE IF NOT EXISTS handoffs (
    handoff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_agent_id INTEGER,
    to_agent_id INTEGER,
    action_id INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    gotcha_id INTEGER,
    context_snapshot TEXT,
    FOREIGN KEY(from_agent_id) REFERENCES agents(agent_id),
    FOREIGN KEY(to_agent_id) REFERENCES agents(agent_id),
    FOREIGN KEY(action_id) REFERENCES actions(action_id),
    FOREIGN KEY(gotcha_id) REFERENCES gotchas(gotcha_id)
);

CREATE TABLE IF NOT EXISTS gotchas (
    gotcha_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    agent_id INTEGER,
    description TEXT,
    severity TEXT,
    resolved BOOLEAN DEFAULT 0,
    resolution_notes TEXT,
    related_action_id INTEGER,
    related_handoff_id INTEGER,
    FOREIGN KEY(agent_id) REFERENCES agents(agent_id),
    FOREIGN KEY(related_action_id) REFERENCES actions(action_id),
    FOREIGN KEY(related_handoff_id) REFERENCES handoffs(handoff_id)
);

CREATE TABLE IF NOT EXISTS logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    agent_id INTEGER,
    message TEXT,
    level TEXT,
    context TEXT,
    FOREIGN KEY(agent_id) REFERENCES agents(agent_id)
);

CREATE TABLE IF NOT EXISTS config (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
