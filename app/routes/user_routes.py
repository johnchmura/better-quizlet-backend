from fastapi import APIRouter, HTTPException
from app.middleware.utilities import get_user, get_users
from app.models.user_models import User, UserPublic

router = APIRouter()

@router.get("/users/{username}", tags=["users"], response_model=UserPublic)
async def user_profile(username: str):
    """Fetch a user's profile by username."""
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/")
async def users():
    """Fetch all users."""
    users = get_users()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users
