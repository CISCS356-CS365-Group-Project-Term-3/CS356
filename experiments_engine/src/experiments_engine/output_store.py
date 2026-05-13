# Handles saving videos, logs,metrics, and experiment outputs.

import os 
from pymongo import MongoClient
from datetime import datetime

class OutputStore:

    def __init__(self, store_connection=None):
        """Create an OutputStore backed by MongoDB.

        If store_connection is None, connects using MONGO_URI from env
        (or a local default).
        """
        if store_connection is None:
            uri = os.getenv(
                "MONGO_URI",
                "mongodb://admin:admin@localhost:27017/",
            )
            db_name = os.getenv("MONGO_DB_NAME", "experiment_storage")
            self._client = MongoClient(uri)
            self._db = self._client[db_name]
        else:
            self._db = store_connection
      

    def save_log(self, experiment_id: str, sequence_name: str, log_data: str):
        # saves encoding log entry to the database, with timestamp
        self._db.logs.insert_one({
            "experiment_id": experiment_id,
            "sequence_name": sequence_name,
            "log_data": log_data,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def save_file(self, file_path, destination):

        # saves encoded output file

        pass

    def save_status(self, experiment_id, results):
        #save the current status of an experiment.
        #accepts either a status string ("RUNNING", "COMPLETED", "FAILED")
        #or a full result dict. Both are merged into the results document.
        
        if isinstance(results, str):
            payload = {"status": results}
        else:
            payload = dict(results)

        payload["updated_at"] = datetime.utcnow().isoformat()

        self._db.results.update_one(
            {"_id": experiment_id},
            {"$set": payload},
            upsert=True,
        )

    def save_video(self, video_path):

        # saves encoded video

        pass

    def save_metrics(self, experiment_id: str, metrics: dict):
        # saves encoding metrics/statistics
        self._db.metrics.replace_one(
            {"_id": experiment_id},
            {"_id": experiment_id, **metrics},
            upsert=True,
        )

    def save_configs(self, experiment_id: str, config: dict):
        # saves configuration information
        self._db.configs.replace_one(
            {"_id": experiment_id},
            {"_id": experiment_id, **config},
            upsert=True,
        )

    def organise_output_directory(self, experiment_id):

        # org experiment output folders

        pass

    def get_result(self, experiment_id: str):
        # retrieves results for an experiment
        return self._db.results.find_one({"_id": experiment_id})
    
    def get_logs(self, experiment_id: str):
        # retrieves logs for an experiment
        return list(self._db.logs.find({"experiment_id": experiment_id}))
    
    def get_metrics(self, experiment_id: str):
        # retrieves metrics for an experiment
        return self._db.metrics.find_one({"_id": experiment_id})