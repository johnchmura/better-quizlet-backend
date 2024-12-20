from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from .loadenv import get_key, get_algo
from app.models.user_models import User, UserInDB
from app.models.token_models import Token, TokenData
from app.config.db import get_mongo_client, get_database
import logging

# Environment configurations
SECRET_KEY = get_key()
ALGORITHM = get_algo()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize MongoDB client and database
mongo_client = get_mongo_client()
db = get_database(mongo_client, "your_database_name")  # Replace with your database name

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# FastAPI app instance
router = APIRouter()

# Test user creation function
def create_test_user():
    """Creates a test user in the database."""
    test_user = db["users"].find_one({"username": "testuser"})
    if not test_user:
        hashed_password = get_password_hash("testpassword")  # Replace with desired password
        db["users"].insert_one({
            "username": "testuser",
            "hashed_password": hashed_password,
            "disabled": False  # Set to True if you want the user to be disabled
        })
        logging.info("Test user created.")
    else:
        logging.info("Test user already exists.")

# Utility Functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if the plain password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hashes the provided password."""
    return pwd_context.hash(password)


def get_user(username: str):
    """Fetches the user from the MongoDB database by username."""
    if db is None:
        logging.error("Database connection is unavailable.")
        return None

    user_data = db["users"].find_one({"username": username})  # Adjust "users" to your collection name
    if user_data:
        return UserInDB(**user_data)


def authenticate_user(username: str, password: str):
    """Authenticates the user by verifying username and password."""
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Generates a JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Dependencies
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    """Fetches the current user from the token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Ensures the user is active."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


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
