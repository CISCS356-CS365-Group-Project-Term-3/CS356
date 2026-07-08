from flask import Flask, request
from flask_cors import CORS
from services import experiment_service
from storage import experiment_store
from storage.db import engine, Base

app = Flask(__name__)
Base.metadata.create_all(bind=engine)
CORS(app)

@app.route("/experiments", methods=["POST"])
def create_experiment_endpoint():
    """ create an experiment endpoint """
    data = request.get_json()
    created_experiment = experiment_service.create_experiment(data)

    return {
        "id": created_experiment["group"]["id"]
    }, 201

@app.route("/experiments", methods=["GET"])
def get_experiments():
    """ get all experiments or experiments by users id"""
    user_id = request.args.get("userId")

    if user_id:
        return experiment_store.get_groups_by_userID(int(user_id)), 200

    return experiment_store.get_all_groups(), 200

@app.route("/experiments/user/<int:user_id>", methods=["GET"])
def get_experiments_by_user(user_id):
    """ get all experiments or experiments by users id"""

    if user_id:
        return experiment_store.get_groups_by_userID(int(user_id)), 200

    return experiment_store.get_all_groups(), 200

@app.route("/experiments/<int:group_id>", methods=["PATCH"])
def update_experiment(group_id):
    """ update an experiment """
    data = request.get_json()
    updated_experiment = experiment_service.update_experiment(group_id, data)
    if not updated_experiment:
        return {"error": "Experiment not found"}, 404
    return updated_experiment, 200

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200

@app.route("/experiments/runs/<int:run_id>/running", methods=["POST"])
def mark_run_running(run_id):
    """mark run as running."""
    experiment_store.update_run_status(run_id, "running")
    return {"message": "Run marked as running"}, 200

@app.route("/experiments/runs/<int:run_id>/complete", methods=["POST"])
def mark_run_complete(run_id):
    """mark run as complete."""
    experiment_store.update_run_status(run_id, "complete")
    return {"message": "Run marked as complete"}, 200

@app.route("/experiments/runs/<int:run_id>/failed", methods=["POST"])
def mark_run_failed(run_id):
    """mark run as failed."""
    experiment_store.update_run_status(run_id, "failed")
    return {"message": "Run marked as failed"}, 200
if __name__ == "__main__":
    app.run(debug=True)
