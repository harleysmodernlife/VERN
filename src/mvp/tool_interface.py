"""
VERN Tool Interface (Python Functions)
--------------------------------------
Defines core tools as Python functions for direct agent invocation.
"""

def echo(text):
    """Returns the input string."""
    return text

def add(a, b):
    """Returns the sum of two numbers."""
    return a + b

def journal_entry(entry, db_path="db/vern.db"):
    """Adds a health/wellness journal entry to the database."""
    import sqlite3
    import datetime
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        entry TEXT
    )
    """)
    c.execute("INSERT INTO journal (timestamp, entry) VALUES (?, ?)",
              (datetime.datetime.now().isoformat(), entry))
    conn.commit()
    conn.close()
    return "Journal entry saved."

def schedule_event(details):
    """Schedules an event (mock implementation)."""
    return f"Event scheduled: {details}"

def finance_balance():
    """Returns a mock finance/resource balance."""
    return {"balance": 1000, "currency": "USD"}

def get_user_profile(user_id, db_path="db/vern.db"):
    """Fetches a user profile from the database (mock implementation)."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS user_profile (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )
    """)
    c.execute("SELECT name, email FROM user_profile WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"user_id": user_id, "name": row[0], "email": row[1]}
    else:
        return {"error": "User not found."}
