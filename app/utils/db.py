from flask_pymongo.wrappers import Database
from app import mongo


def get_db() -> Database:
    assert mongo.db is not None, "MongoDB is not initialized"
    return mongo.db
