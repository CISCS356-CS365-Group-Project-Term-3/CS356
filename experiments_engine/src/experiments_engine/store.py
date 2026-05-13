"""MongoDB-backed Store for experiment and config data.

Handles read operations the engine needs to process an experiment:
experiment retrieval, system config, and lookup tables.
"""
#commented code are EXAMPLES

import os
from pymongo import MongoClient
class Store:

    def __init__(self, db_connection=None):
        # Database connection
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
    
    def save_experiment(self, experiment_id: str, data: dict):
        # Saves experiment information to the database
        self._db.experiments.replace_one(
            {"_id": experiment_id},
            {"_id": experiment_id, **data},
            upsert=True
        )

    def get_experiment(self, experiment_id: str):
        # Retrieves experiment information
        # from the database
        return self._db.experiments.find_one({"_id": experiment_id})

    def save_config(self,config: dict) -> None:
        # Saves system configuration information
        self._db.config.replace_one(
            {"_id": "system"},
            {"_id": "system", **config},
            upsert=True
        )

    def get_config(self):
        # Retrieves system configuration
        # information
        return self._db.config.find_one({"_id": "system"})

    def lookup_spatial(self, spatial_id):
        # Retrieves spatial settings
        # such as resolution
        return self._db.spatial.find_one({"_id": spatial_id})

    def lookup_codec(self, codec_id):
        # Retrieves codec information
 
        return self._db.codecs.find_one({"_id": codec_id})

    def lookup_source_file(self, file_id):
        # Retrieves source video path/file info
        return self._db.source_files.find_one({"_id": file_id})

    def list_experiments(self):
        # Lists all experiments in the database
        return [
            doc["_id"] for doc in self._db.experiments.find({}, {"_id": 1})
        ]
