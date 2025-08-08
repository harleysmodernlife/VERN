from fastapi import APIRouter, status, Request
from pydantic import BaseModel

from vern_backend.app.errors import error_response

router = APIRouter(prefix="/users", tags=["users"])

class UserProfile(BaseModel):
    user_id: str
    username: str
    profile_data: dict = {}

USERS = [
    UserProfile(user_id="default_user", username="default", profile_data={})
]

@router.get("/{user_id}", response_model=UserProfile)
def get_user_profile(user_id: str):
    for user in USERS:
        if user.user_id == user_id:
            return user
    # If not found, return a neutral profile rather than treating as error for MVP
    return UserProfile(user_id=user_id, username="unknown", profile_data={})

@router.post("/")
def create_user(profile: UserProfile, request: Request):
    # Basic validation example
    if not profile.user_id or not profile.username:
        return error_response("VALIDATION_ERROR", status.HTTP_400_BAD_REQUEST, "user_id and username are required", request)
    # Conflict check
    if any(u.user_id == profile.user_id for u in USERS):
        return error_response("CONFLICT", status.HTTP_409_CONFLICT, f"user_id '{profile.user_id}' already exists", request)
    USERS.append(profile)
    return {"status": "created", "user_id": profile.user_id}
