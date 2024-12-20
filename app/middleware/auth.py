from datetime import timedelta
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from .loadenv import get_key, get_algo
from app.models.user_models import User
from app.models.token_models import Token
from app.config.db import get_mongo_client, get_database
from .utilities import create_access_token, authenticate_user
from .dependencies import get_current_active_user

SECRET_KEY = get_key()
ALGORITHM = get_algo()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

mongo_client = get_mongo_client()
db = get_database(mongo_client, "your_database_name")  # Replace with your database name

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

# Routes
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """Login to get an access token."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Fetch the current logged-in user's details."""
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Fetch items owned by the current user."""
    return [{"item_id": "Foo", "owner": current_user.username}]
