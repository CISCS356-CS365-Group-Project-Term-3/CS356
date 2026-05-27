from queue_setup.publisher import publish_to_queue
from storage.experiment_store import save_experiment
from utils.encoding import generate_sequence_code

""" 
This is what I have come up with initially but I am not following the final API contract
I will make changes as the API contract changes but this is for just so we can start getting
the frontend and backend connected

Based on an example output scott sent me from what he expects the frontend to send the backend

1. Create experiment 
2. Store it 
3. Publish it to a queue 

Initial Message definition involves three fields
A user id to map experiments together 
A sequence code defining a users choices 
A id for easy greater than or less than logic to check order of experiments if necessary
(this might be removed if unnecessary or smarter logic may be implemented)

"""

def create_experiment(data):
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