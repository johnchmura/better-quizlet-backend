import os
from dotenv import load_dotenv

def get_connect():
    load_dotenv()
    return os.getenv("CONNECT_DB")