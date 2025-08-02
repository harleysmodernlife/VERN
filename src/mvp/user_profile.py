"""
VERN User Profile Management
---------------------------
Handles persistent storage and update of user resonance profiles (base-14 archetype vectors).
Uses SQLite for storage; can be swapped for ChromaDB/LlamaIndex for advanced memory/RAG.

Profile schema:
- user_id: str
- resonance: JSON string (dict of archetype names to float scores)
- last_updated: timestamp

See archetype_cluster.py for resonance vector details.
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "db/vern.db"

def get_connection():
    if not os.path.exists("db"):
        os.makedirs("db")
    return sqlite3.connect(DB_PATH)

def init_user_profile_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id TEXT PRIMARY KEY,
            resonance TEXT,
            last_updated TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_user_profile(user_id: str, resonance: dict):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO user_profiles (user_id, resonance, last_updated)
        VALUES (?, ?, ?)
    """, (user_id, json.dumps(resonance), datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def load_user_profile(user_id: str, default_resonance: dict) -> dict:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT resonance FROM user_profiles WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        try:
            return json.loads(row[0])
        except Exception:
            return default_resonance
    else:
        return default_resonance

def update_user_resonance(user_id: str, updates: dict, default_resonance: dict):
    profile = load_user_profile(user_id, default_resonance)
    for k, v in updates.items():
        if k in profile:
            profile[k] = v
    save_user_profile(user_id, profile)
    return profile

# Initialize DB on import
init_user_profile_db()

# Example usage:
# from src.mvp.archetype_cluster import ArchetypeCluster
# cluster = ArchetypeCluster()
# default_profile = cluster.default_user_profile()
# save_user_profile("user123", default_profile)
# profile = load_user_profile("user123", default_profile)
# profile = update_user_resonance("user123", {"Nurturer": 0.8}, default_profile)
