from fastapi import APIRouter, status, Request
from pydantic import BaseModel
import sqlite3
import os

from vern_backend.app.errors import error_response

try:
    from vern_backend.app.db_path import get_sqlite_path
    DB_PATH = get_sqlite_path()
except Exception:
    DB_PATH = os.environ.get("SQLITE_DB_PATH", "/app/data/vern.sqlite")

router = APIRouter(prefix="/users", tags=["users"])

class UserProfile(BaseModel):
    user_id: str
    username: str
    preferences: str = ""
    profile_data: dict = {}

def get_db_conn():
    return sqlite3.connect(DB_PATH)

@router.get("/{user_id}", response_model=UserProfile)
def get_user_profile(user_id: str):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, preferences FROM user_profiles WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return UserProfile(user_id=row[0], username=row[1], preferences=row[2], profile_data={})
    # TODO: Load profile_data from preferences JSON if needed
    return UserProfile(user_id=user_id, username="unknown", preferences="", profile_data={})

@router.post("/")
def create_user(profile: UserProfile, request: Request):
    if not profile.user_id or not profile.username:
        return error_response("VALIDATION_ERROR", status.HTTP_400_BAD_REQUEST, "user_id and username are required", request)
    conn = get_db_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO user_profiles (user_id, preferences) VALUES (?, ?)", (profile.user_id, str(profile.profile_data)))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return error_response("CONFLICT", status.HTTP_409_CONFLICT, f"user_id '{profile.user_id}' already exists", request)
    conn.close()
    return {"status": "created", "user_id": profile.user_id}

@router.put("/{user_id}")
def update_user_profile(user_id: str, profile: UserProfile, request: Request):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("UPDATE user_profiles SET preferences = ? WHERE user_id = ?", (str(profile.profile_data), user_id))
    conn.commit()
    conn.close()
    return {"status": "updated", "user_id": user_id}

@router.get("/")
def list_user_profiles():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, preferences FROM user_profiles")
    rows = cur.fetchall()
    conn.close()
    return [UserProfile(user_id=row[0], username=row[1], preferences=row[2], profile_data={}) for row in rows]

# TODO: Add delete endpoint and improve profile_data handling.
