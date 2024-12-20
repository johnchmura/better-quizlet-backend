import os
from dotenv import load_dotenv

def get_OPENAI_key():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

def get_org():
    load_dotenv()
    return os.getenv("ORGANIZATION_ID")

def get_JWT_key():
    load_dotenv()
    return os.getenv("JWT_KEY")

def get_algo():
    load_dotenv()
    return os.getenv("ALGO")

def get_connect():
    load_dotenv()
    return os.getenv("CONNECT_DB")