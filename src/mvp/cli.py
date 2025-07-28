"""
VERN CLI Chat Interface (LLM-Powered, Multi-Agent)
--------------------------------------------------
A smart command-line chat interface for the VERN agent system.
Supports persistent memory (SQLite), direct Python tool invocation, LLM-powered Orchestrator, and logging.
"""

import sys
import readline
import sqlite3
import datetime
import os

# Fix import for direct CLI run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.mvp.tool_interface import echo, add, journal_entry, schedule_event, finance_balance, get_user_profile
from src.mvp.orchestrator import orchestrator_respond

DB_PATH = "db/vern.db"

def ensure_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS chat_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        sender TEXT,
        message TEXT
    )
    """)
    conn.commit()
    conn.close()

def log_message(sender, message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO chat_log (timestamp, sender, message) VALUES (?, ?, ?)",
              (datetime.datetime.now().isoformat(), sender, message))
    conn.commit()
    conn.close()

def get_last_user_message():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT message FROM chat_log WHERE sender='user' ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def print_history(n=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp, sender, message FROM chat_log ORDER BY id DESC LIMIT ?", (n,))
    rows = c.fetchall()
    conn.close()
    for row in reversed(rows):
        print(f"[{row[0][:19]}] {row[1]}: {row[2]}")

def get_recent_history(n=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT sender, message FROM chat_log ORDER BY id DESC LIMIT ?", (n,))
    rows = c.fetchall()
    conn.close()
    # Format as a conversation string for LLM context
    return "\n".join([f"{sender}: {msg}" for sender, msg in reversed(rows)])

def vern_response(user_input):
    # Direct tool invocation for explicit commands
    if user_input.startswith("echo "):
        text = user_input[5:]
        result = echo(text)
        return f"(echo tool) {result}"
    elif user_input.startswith("add "):
        try:
            parts = user_input[4:].split()
            a, b = float(parts[0]), float(parts[1])
            result = add(a, b)
            return f"(add tool) {result}"
        except Exception as e:
            return f"Error: {e}"
    elif user_input.startswith("journal "):
        entry = user_input[8:]
        result = journal_entry(entry)
        return f"(journal tool) {result}"
    elif user_input.startswith("schedule "):
        details = user_input[9:]
        result = schedule_event(details)
        return f"(schedule tool) {result}"
    elif user_input == "finance":
        result = finance_balance()
        return f"(finance tool) {result}"
    elif user_input.startswith("profile "):
        try:
            user_id = int(user_input[8:])
            result = get_user_profile(user_id)
            return f"(profile tool) {result}"
        except Exception as e:
            return f"Error: {e}"
    elif user_input == "last":
        last = get_last_user_message()
        return f"Last thing you said: {last}" if last else "No previous messages found."
    elif user_input == "history":
        print_history()
        return ""
    else:
        # Default: route to Orchestrator LLM agent for smart response
        context = get_recent_history(10)
        agent_status = "All agents online."
        result = orchestrator_respond(user_input, context, agent_status)
        return f"(orchestrator) {result}"

def main():
    ensure_db()
    print("Welcome to VERN CLI Chat!")
    print("Type your message. Try natural language or commands like 'echo <text>', 'add <a> <b>', 'journal <entry>', 'schedule <details>', 'finance', 'profile <user_id>', 'last', or 'history'. Ctrl+C to exit.")
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            log_message("user", user_input)
            response = vern_response(user_input)
            if response:
                print(response)
                log_message("vern", response)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
