from passlib.context import CryptContext
from app.config.db import get_mongo_client, get_database
from datetime import datetime, timedelta, timezone
from app.utils.load_env import get_JWT_key, get_algo
from app.utils.user_utils import get_user
import jwt

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

