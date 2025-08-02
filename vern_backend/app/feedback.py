"""
VERN Backend - Feedback API
----------------------------
This module defines endpoints for capturing, storing, and aggregating user feedback.
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import statistics

router = APIRouter()

# Global in-memory storage for feedback submissions
feedback_storage = []

class Feedback(BaseModel):
    feedback: str

@router.post("/feedback")
async def submit_feedback(feedback: Feedback, request: Request):
    try:
        # Store feedback in memory (in production, this should be persisted to a database)
        feedback_entry = {
            "feedback": feedback.feedback,
            "client": request.client.host
        }
        feedback_storage.append(feedback_entry)
        print(f"Feedback received from {request.client.host}: {feedback.feedback}")
        return {"status": "success", "message": "Feedback received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedback/aggregate")
async def aggregate_feedback():
    """
    Aggregates feedback based on simple sentiment analysis.
    For demonstration, we simulate sentiment by counting occurrences of negative words.
    """
    if not feedback_storage:
        return {"status": "success", "message": "No feedback available", "negative_count": 0, "total": 0}
    
    negative_keywords = ["error", "fail", "bad", "issue", "problem"]
    negative_count = 0
    for entry in feedback_storage:
        text = entry["feedback"].lower()
        if any(keyword in text for keyword in negative_keywords):
            negative_count += 1

    total = len(feedback_storage)
    # Calculate a simple negative feedback ratio (if needed, more complex analysis can be added)
    negative_ratio = negative_count / total

    return {
        "status": "success",
        "total_feedback": total,
        "negative_feedback": negative_count,
        "negative_ratio": negative_ratio
    }
