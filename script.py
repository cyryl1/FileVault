#!/usr/bin/env python3
from pymongo import MongoClient
from vault.config import Config

client = MongoClient(Config.MONGODB_URI)
db = client[Config.DATABASE_NAME]
db.files.delete_many({"id": None})
db.files.delete_many({"file_id": None})  # In case file_id exists
try:
    print("------------------Resetting database--------------------")
    db.files.drop_index("file_id_1")
except:
    pass
db.files.create_index("id", unique=True)