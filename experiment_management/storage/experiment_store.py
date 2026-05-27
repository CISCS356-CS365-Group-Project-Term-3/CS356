"""
Creating an in memory storage so I can test out the functionality before integrating Database
Ordering based off larger id for now to determine order in the future this may be
replaced with smarter logic
"""

experiments = []
experiment_id = 1

def save_experiment(experiment):
    global experiment_id
    experiment["id"] = experiment_id
    experiments.append(experiment)
    experiment_id += 1
    return experiment

# filter experiments by user id
def get_all_by_user(user_id):
    return [e for e in experiments if e["user_id"] == user_id]