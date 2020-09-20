import logging
from pymongo import ASCENDING
from pymongo import MongoClient


logger = logging.getLogger(__name__)

MONGODB_CLIENT = MongoClient("MONGO_URI")


def install(app):
    """Return a collection addresses from database viacep."""
    try:
        db = MONGODB_CLIENT.get_database("viacep")
        app.db = db.get_collection("addresses")
        db.addresses.create_index([("cep", ASCENDING)], unique=True)
        MONGODB_CLIENT.server_info()
    except Exception as e:
        logger.error(f"Error connect database: {e}")
        exit()
