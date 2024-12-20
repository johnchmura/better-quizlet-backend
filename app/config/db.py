import logging
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .loadenv import get_connect

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_mongo_client():
    """
    Establishes and returns a MongoDB client.
    """
    uri = get_connect()
    if not uri:
        logging.error("MongoDB connection URI not found.")
        return None
    
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        client.admin.command('ping')
        logging.info("Successfully connected to MongoDB.")
        return client
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        return None

def get_database(client, db_name):
    """
    Retrieves a specific database from the client.
    """
    if client:
        return client[db_name]
    else:
        logging.error("MongoDB client is not available.")
        return None
