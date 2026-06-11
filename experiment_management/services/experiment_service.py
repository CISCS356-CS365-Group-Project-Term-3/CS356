from datetime import datetime

from queue_setup.publisher import publish_to_queue
from storage.experiment_store import save_experiment
from utils.encoding import generate_sequence_code


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
