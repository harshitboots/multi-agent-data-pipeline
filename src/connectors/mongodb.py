import pandas as pd
from pymongo import MongoClient

def connect(uri: str, database: str) -> tuple:
    client = MongoClient(uri)
    db = client[database]
    return client, db

def list_collections(uri: str, database: str) -> list:
    client, db = connect(uri, database)
    try:
        return db.list_collection_names()
    finally:
        client.close()

def fetch_collection(uri: str, database: str, collection: str, limit: int = 1000) -> pd.DataFrame:
    client, db = connect(uri, database)
    try:
        cursor = db[collection].find({}, {"_id": 0}, limit=limit)
        return pd.DataFrame(list(cursor))
    finally:
        client.close()
