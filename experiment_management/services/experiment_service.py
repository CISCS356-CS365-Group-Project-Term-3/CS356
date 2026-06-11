from datetime import datetime

from queue_setup.publisher import publish_to_queue
from storage.experiment_store import save_experiment
from utils.encoding import generate_sequence_code
from storage.experiment_store import get_by_id
from storage.experiment_store import update_experiment_by_id


def create_experiment(data):
    """ create an experiment """
    user_id = data.get("userId")
    status = data.get("status", "draft")
    name = data.get("name")
    project_type_id = data.get("projectTypeId")
    encoders = data.get("encoders") or []
    sequences = data.get("sequences") or []
    date = datetime.utcnow().isoformat()

    if status == "draft":
        job = {
            "userId": user_id,
            "name": name,
            "status": "draft",
            "projectTypeId": project_type_id,
            "date": date,
            "encoders": encoders,
            "sequences": sequences
        }

        saved = save_experiment(job)
        return saved
    if status == "finalised":
        last_saved = None
        for encoder in encoders:
            for seq in sequences:
                code = generate_sequence_code(seq, encoder)
                job = {
                    "userId": data["userId"],
                    "name": data["name"],
                    "status": status,
                    "projectTypeId": data["projectTypeId"],
                    "date": date,
                    "encoders": [encoder],
                    "sequences": [{"videoFileId": seq["videoFileId"], "sequence_code": code}]
                }
                last_saved = save_experiment(job)
                payload = {
                    "experiment_id": last_saved["id"],
                    "date": last_saved["date"],
                    "sequence_code": code,
                    "videoFileId": seq["videoFileId"],
                    "userId": data["userId"]
                }
                print("Publishing to queue:", payload)
                publish_to_queue(payload)
        return last_saved

def update_experiment(experiment_id, data):
    """ update an experiment """
    existing = get_by_id(experiment_id)
    if not existing:
        return None
    updated = {
        "userId": data.get("userId", existing["userId"]),
        "name": data.get("name", existing["name"]),
        "status": data.get("status", existing["status"]),
        "projectTypeId": data.get("projectTypeId", existing["projectTypeId"]),
        "encoders": data.get("encoders", existing.get("encoders", [])),
        "sequences": data.get("sequences", existing.get("sequences", [])),
        "date": datetime.utcnow().isoformat()
    }
    saved = update_experiment_by_id(experiment_id, updated)
    if updated["status"] == "draft":
        return saved
    if updated["status"] == "finalised":
        last_saved = None
        for encoder in updated["encoders"]:
            for seq in updated["sequences"]:
                code = generate_sequence_code(seq, encoder)
                job = {
                    "userId": updated["userId"],
                    "name": updated["name"],
                    "status": "finalised",
                    "projectTypeId": updated["projectTypeId"],
                    "date": updated["date"],
                    "encoders": [encoder],
                    "sequences": [{"videoFileId": seq["videoFileId"],"sequence_code": code}]
                }
                last_saved = update_experiment_by_id(experiment_id, job)
                payload = {
                    "experiment_id": experiment_id,
                    "date": updated["date"],
                    "sequence_code": code,
                    "videoFileId": seq["videoFileId"],
                    "userId": updated["userId"]
                }
                print("Publishing to queue:", payload)
                publish_to_queue(payload)
        return last_saved
    return saved