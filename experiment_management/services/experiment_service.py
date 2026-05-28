from queue_setup.publisher import publish_to_queue
from storage.experiment_store import save_experiment
from utils.encoding import generate_sequence_code

def create_experiment(data):
    """ create an experiment """
    user_id = data["user_id"]

    experiment = {
        "user_id": user_id,
        "name": data["name"],
        "status": data["status"],
        "project_type_id": data["project_type_id"],
        "sequences": []
    }
    saved = save_experiment(experiment)

    for seq in data.get("sequences", []):
        code = generate_sequence_code(seq)
        saved["sequences"].append({
            "sequence_code": code
        })
        publish_to_queue({
            "experiment_id": saved["id"],
            "user_id": user_id,
            "sequence_code": code
        })
    return saved