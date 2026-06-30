import os
from pymongo import MongoClient

MONGO_URI = os.getenv("OUTPUT_MONGO_URI", "mongodb://admin:admin@localhost:27017/")
MONGO_DB_NAME = os.getenv("OUTPUT_MONGO_DB_NAME", "experiment_storage")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
experiment_results = db["experiment_results"]

def get_frame_data(experiment_id):
    doc = experiment_results.find_one(
        {"project.experiment_id": experiment_id},
        {
            "_id": 0,
            "result.psnr.raw": 1,
            "result.ssim.raw": 1,
        }
    )
    return doc

def get_all_results(limit=100):
    docs = (
        experiment_results.find(
            {},
            {
                "_id": 0,
                "project.experiment_id": 1,
                "project.group_id": 1,
                "project.user_id": 1,
                "project.created_at": 1,
                "sequence": 1,
                "success": 1,
                "result.psnr.average": 1,
                "result.psnr.raw.combined": 1,
                "result.ssim.average": 1,
                "result.reason": 1,
            },
        )
        .sort("project.created_at", -1)
        .limit(limit)
    )

    return list(docs)

