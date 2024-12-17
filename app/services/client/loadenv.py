import os
from dotenv import load_dotenv

def get_key():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

def get_org():
    load_dotenv()
    return os.getenv("ORGANIZATION_ID")