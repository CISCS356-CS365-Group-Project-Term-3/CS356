from datetime import datetime

from queue_setup.publisher import publish_to_queue
from storage.experiment_store import save_experiment
from utils.encoding import generate_sequence_code


def create_experiment(data):
    """ create an experiment """
    # To-Do: once user details are retrieved then make this a mandatory field
    user_id = data["userId"]
    status = data["status"]

    date = datetime.utcnow().isoformat()
    last_saved = None

    for encoder in data.get("encoders", []):
        for seq in data.get("sequences", []):
            code = generate_sequence_code(seq, encoder)
            job = {
                "userId": user_id,
                "name": data["name"],
                "status": status,
                "projectTypeId": data["projectTypeId"],
                "date": date,
                "encoders": [encoder],
                "sequences": [{"videoFileId": seq["videoFileId"], "sequence_code": code}]
            }
            last_saved = save_experiment(job)
            # if status == "finalised":
            #    publish_to_queue({
            #        "experiment_id": last_saved["id"],
            #        "user_id": user_id,
            #        "date": last_saved["date"],
            #        "sequence_code": code
            #    })
            payload = {
                "experiment_id": last_saved["id"],
                "date": last_saved["date"],
                "sequence_code": code,
                "videoFileId": seq["videoFileId"]
            }
            if user_id is not None:
                payload["userId"] = user_id
            print("Publishing to queue:", payload)
            publish_to_queue(payload)

    return last_saved
