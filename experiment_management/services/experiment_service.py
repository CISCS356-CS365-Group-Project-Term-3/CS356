from datetime import datetime

from queue_setup.publisher import publish_to_queue
from storage.experiment_store import save_experiment
from utils.encoding import generate_sequence_code

def create_experiment(data):
    """ create an experiment """
    # To-Do: once user details are retrieved then make this a mandatory field
    user_id = data["userId"]
    status = data["status"]

    experiment = {
        "userId": user_id,
        "name": data["name"],
        "status": status,
        "projectTypeId": data["projectTypeId"],
        "date": datetime.utcnow().isoformat(),
        "encoders": data.get("encoders", []),
        "sequences": []
    }
    saved = save_experiment(experiment)

    for encoder in saved["encoders"]:
        for seq in data.get("sequences", []):

            code = generate_sequence_code(seq, encoder)

            stored_sequence = {
                "videoFileId": seq["videoFileId"],
                "sequence_code": code
            }
            saved["sequences"].append(stored_sequence)
            # if status == "finalised":
            #    publish_to_queue({
            #        "experiment_id": saved["id"],
            #        "user_id": user_id,
            #        "date": saved["date"],
            #        "sequence_code": code
            #    })
            save_experiment(saved)
            payload = {
                "experiment_id": saved["id"],
                "date": saved["date"],
                "sequence_code": code,
                "videoFileId": seq["videoFileId"]
            }

            if user_id is not None:
                payload["userId"] = user_id
            print("Publishing to queue:", payload)
            publish_to_queue(payload)
    return saved