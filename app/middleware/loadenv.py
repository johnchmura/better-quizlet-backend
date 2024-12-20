import os
from dotenv import load_dotenv

def get_key():
    load_dotenv()
    return os.getenv("JWT_KEY")

def get_algo():
    load_dotenv()
    return os.getenv("ALGO")