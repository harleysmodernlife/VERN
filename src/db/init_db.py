"""
Initialize the VERN SQLite database using the schema.sql file.
"""

import sqlite3
import os

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")
DB_PATH = os.path.join(os.path.dirname(__file__), "../../db/vern.db")

def init_db():
    with open(SCHEMA_PATH, "r") as f:
        schema = f.read()
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(schema)
        print(f"Database initialized at {DB_PATH}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
