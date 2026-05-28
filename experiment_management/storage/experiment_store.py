experiments = []
experiment_id = 1

def save_experiment(experiment):
    """ save an experiment to the database """
    global experiment_id
    experiment["id"] = experiment_id
    experiments.append(experiment)
    experiment_id += 1
    return experiment

# filter experiments by user id
def get_all_by_user(user_id):
    return [e for e in experiments if e["user_id"] == user_id]