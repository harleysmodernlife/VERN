"""
VERN Backend - Feedback API
----------------------------
This module defines endpoints for capturing, storing, and aggregating user feedback.
"""

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
import sqlite3
import os

from vern_backend.app.errors import error_response

try:
    from vern_backend.app.db_path import get_sqlite_path
    DB_PATH = get_sqlite_path()
except Exception:
    DB_PATH = os.environ.get("SQLITE_DB_PATH", "/app/data/vern.sqlite")

router = APIRouter()

class Feedback(BaseModel):
    user_id: str
    feedback_type: str = ""
    feedback_content: str

class AdaptationEvent(BaseModel):
    user_id: str
    event_type: str
    event_data: str
    triggered_by: str = ""

def get_db_conn():
    return sqlite3.connect(DB_PATH)

@router.post("/feedback")
async def submit_feedback(feedback: Feedback, request: Request):
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO feedback (user_id, feedback_type, feedback_content) VALUES (?, ?, ?)",
            (feedback.user_id, feedback.feedback_type, feedback.feedback_content)
        )
        conn.commit()
        conn.close()
        print(f"Feedback received from {feedback.user_id}: {feedback.feedback_content}")
        return {"status": "success", "message": "Feedback received"}
    except Exception as e:
        return error_response("UNKNOWN_ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR, "An unknown error occurred.", request, {"error": str(e)})

@router.get("/feedback/aggregate")
async def aggregate_feedback():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT feedback_content FROM feedback")
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return {"status": "success", "message": "No feedback available", "negative_count": 0, "total": 0}
    negative_keywords = ["error", "fail", "bad", "issue", "problem"]
    negative_count = 0
    for row in rows:
        text = row[0].lower()
        if any(keyword in text for keyword in negative_keywords):
            negative_count += 1
    total = len(rows)
    negative_ratio = negative_count / total if total else 0
    return {
        "status": "success",
        "total_feedback": total,
        "negative_feedback": negative_count,
        "negative_ratio": negative_ratio
    }

@router.post("/adaptation_event")
async def log_adaptation_event(event: AdaptationEvent, request: Request):
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO adaptation_events (user_id, event_type, event_data, triggered_by) VALUES (?, ?, ?, ?)",
            (event.user_id, event.event_type, event.event_data, event.triggered_by)
        )
        conn.commit()
        conn.close()
        # TODO: Trigger agent workflow update based on adaptation event
        return {"status": "success", "message": "Adaptation event logged"}
    except Exception as e:
        return error_response("UNKNOWN_ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR, "An unknown error occurred.", request, {"error": str(e)})

@router.get("/adaptation_events/{user_id}")
async def get_adaptation_events(user_id: str):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT event_type, event_data, triggered_by, created_at FROM adaptation_events WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "event_type": row[0],
            "event_data": row[1],
            "triggered_by": row[2],
            "created_at": row[3]
        }
        for row in rows
    ]

# TODO: Add feedback deletion and update endpoints if needed.
