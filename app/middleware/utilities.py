from passlib.context import CryptContext
from app.models.user_models import UserPublic, User
from app.config.db import get_mongo_client, get_database
from datetime import datetime, timedelta, timezone
from app.utils.load_env import get_JWT_key, get_algo
from typing import List
import jwt
import logging

SECRET_KEY = get_JWT_key()
ALGORITHM = get_algo()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
mongo_client = get_mongo_client()
db = get_database(mongo_client, "better_quizlet_db")


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

    user_data = db["users"].find_one({"username": username})
    if user_data:
        return UserPublic(**user_data)

def get_users() -> List[User]:
    """Fetches all users from the database."""
    if db is None:
        logging.error("Database connection is unavailable.")
        return []

    try:
        users_data = db["users"].find({})
        users = [User(**user) for user in users_data]
        return users
    except Exception as e:
        logging.error(f"Error fetching users from database: {e}")
        return []
    

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

