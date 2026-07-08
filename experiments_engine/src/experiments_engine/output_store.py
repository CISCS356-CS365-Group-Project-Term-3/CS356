# Handles saving videos, logs,metrics, and experiment outputs.

import os 
import shutil
import json
from pymongo import MongoClient
from datetime import datetime

from .config import Settings

class OutputStore:

    def __init__(self, store_connection=None):
        """Create an OutputStore backed by MongoDB.

        If store_connection is None, connects using MONGO_URI from env
        (or a local default).
        """
        if store_connection is None:
            uri = Settings.output_mongo_uri
            db_name = Settings.output_mongo_db_name
            self._client = MongoClient(uri)
            self._db = self._client[db_name]
        else:
            self._db = store_connection
    
    def store_experiment_result(self, experiment_result):
        self._db.experiment_results.insert_one((experiment_result))


    def save_file(self, file_path: str, destination: str) -> str:
        # saves encoded output file
        # copy file to destination and return the new path
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy2(file_path, destination)
        return destination

    def save_log(self, experiment_id: str, sequence_name: str, log_data: str):
        # saves encoding log entry to the database, with timestamp
        self._db.logs.insert_one({
            "experiment_id": experiment_id,
            "sequence_name": sequence_name,
            "log_data": log_data,
            "timestamp": datetime.utcnow().isoformat(),
        })

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
        # saves the video to a destination and returns the path.
        output_root = Settings.output_directory
        videos_dir = os.path.join(output_root, "videos")
        filename = os.path.basename(video_path)
        destination = os.path.join(videos_dir, filename)
        return self.save_file(video_path, destination)

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
        # creates experiment output folders and subfolders using experiment_id (if provided)
        # returns the root output path
        output_root = Settings.output_directory
        if experiment_id is None:
            for subdir in ("videos", "logs", "metrics", "configs"):
                os.makedirs(os.path.join(output_root, subdir), exist_ok=True)
            return output_root
        experiment_root = os.path.join(output_root, experiment_id)
        for subdir in ("videos", "logs", "metrics", "configs"):
            os.makedirs(os.path.join(experiment_root, subdir), exist_ok=True)
        return experiment_root
        
    def get_result(self, experiment_id: str):
        # retrieves results for an experiment
        return self._db.results.find_one({"_id": experiment_id})
    
    def get_logs(self, experiment_id: str):
        # retrieves logs for an experiment
        return list(self._db.logs.find({"experiment_id": experiment_id}))
    
    def get_metrics(self, experiment_id: str):
        # retrieves metrics for an experiment
        return self._db.metrics.find_one({"_id": experiment_id})