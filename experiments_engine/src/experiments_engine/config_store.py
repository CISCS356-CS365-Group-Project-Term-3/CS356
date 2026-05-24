# mongodb backed ConfigStore for system configuration.

#Provides the ability to read/lookup and save system configuration information to the database.

import os
from pymongo import MongoClient


class ConfigStore:
    def __init__(self, db_connection=None):
        # create config store backed by MongoDB
        # if db_connection == None, connect through MONGO_URI environment variable
        if db_connection is None:
            uri = os.getenv(
                "MONGO_URI",
                "mongodb://admin:admin@localhost:27017/",
            )
            db_name = os.getenv("MONGO_DB_NAME", "experiment_storage")
            self._client = MongoClient(uri)
            self._db = self._client[db_name]
        else:
            self._db = db_connection

    def get_config(self):
        # retrieve the system configuration from the database
        result = self._db.config.find_one({"_id": "system"})
        return result

    def save_config(self, config: dict) -> None:
        # save the system configuration to the database
        self._db.config.replace_one(
            {"_id": "system"},
            {"_id": "system", **config},
            upsert=True,
        )
