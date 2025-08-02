from fastapi import APIRouter
from pydantic import BaseModel

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
    return UserProfile(user_id=user_id, username="unknown", profile_data={})

@router.post("/")
def create_user(profile: UserProfile):
    USERS.append(profile)
    return {"status": "created", "user_id": profile.user_id}
