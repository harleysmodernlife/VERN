"""
Initialize the VERN SQLite database using the schema.sql file.
Align DB path resolution with backend canonical helper.
"""

import sqlite3
import os

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

# Resolve DB path via backend helper when available
try:
    from vern_backend.app.db_path import get_sqlite_path
    DB_PATH = get_sqlite_path()
except Exception:
    DB_PATH = os.environ.get("SQLITE_DB_PATH", "/app/data/vern.sqlite")

def _ensure_parent_dir(path: str):
    parent = os.path.dirname(path or "")
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

def init_db():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = f.read()
    _ensure_parent_dir(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(schema)
        print(f"Database initialized at {DB_PATH}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
