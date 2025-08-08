import os
import sqlite3
from typing import List

# Align DB path resolution with backend helper
try:
    from vern_backend.app.db_path import get_sqlite_path
    DB_PATH = get_sqlite_path()
except Exception:
    # Fallback to env/default if backend helper unavailable
    DB_PATH = os.environ.get("SQLITE_DB_PATH", "/app/data/vern.sqlite")

MIGRATIONS_DIR = os.environ.get("MIGRATIONS_DIR", os.path.join(os.path.dirname(__file__), "migrations"))

def ensure_parent_dir(path: str):
    parent = os.path.dirname(path or "")
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

def get_conn() -> sqlite3.Connection:
    ensure_parent_dir(DB_PATH)
    return sqlite3.connect(DB_PATH)

def list_migration_files() -> List[str]:
    if not os.path.isdir(MIGRATIONS_DIR):
        return []
    files = sorted(f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql"))
    return [os.path.join(MIGRATIONS_DIR, f) for f in files]

def applied_migrations(conn: sqlite3.Connection) -> set:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE NOT NULL,
            applied_at TEXT DEFAULT (datetime('now'))
        )
    """)
    rows = conn.execute("SELECT filename FROM schema_migrations").fetchall()
    return {r[0] for r in rows}

def apply_migration(conn: sqlite3.Connection, filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        sql = f.read()
    cur = conn.cursor()
    cur.executescript(sql)
    cur.execute("INSERT INTO schema_migrations (filename) VALUES (?)", (os.path.basename(filepath),))
    conn.commit()

def migrate():
    with get_conn() as conn:
        done = applied_migrations(conn)
        files = list_migration_files()
        for path in files:
            name = os.path.basename(path)
            if name in done:
                continue
            apply_migration(conn, path)
            print(f"[migrate] Applied {name}")

if __name__ == "__main__":
    migrate()