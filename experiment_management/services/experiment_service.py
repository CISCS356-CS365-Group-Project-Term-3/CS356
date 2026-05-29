from datetime import datetime

from queue_setup.publisher import publish_to_queue
from storage.experiment_store import save_experiment
from utils.encoding import generate_sequence_code

def create_experiment(data):
    """ create an experiment """
    user_id = data["user_id"]
    status = data["status"]

    experiment = {
        "user_id": user_id,
        "name": data["name"],
        "status": status,
        "project_type_id": data["project_type_id"],
        "date": datetime.utcnow().isoformat(),
        "encoders": data.get("encoders", []),
        "sequences": []
    }
    saved = save_experiment(experiment)

    for encoder in saved["encoders"]:
        for seq in data.get("sequences", []):

            code = generate_sequence_code(seq, encoder)

            stored_sequence = {
                "video_file_id": seq["video_file_id"],
                "resolution_id": seq["resolution_id"],
                "frame_rate_id": seq["frame_rate_id"],
                "quality_id": seq["quality_id"],
                "depth_id": seq["depth_id"],
                "gamut_id": seq["gamut_id"],
                "sequence_code": code
            }
            saved["sequences"].append(stored_sequence)
            if status == "finalised":
                publish_to_queue({
                    "experiment_id": saved["id"],
                    "user_id": user_id,
                    "date": saved["date"],
                    "sequence_code": code
                })
    return saved