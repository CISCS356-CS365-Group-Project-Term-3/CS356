from flask import Flask, request , jsonify
from flask_cors import CORS
from services import experiment_service , results_portal
from storage import experiment_store, results_store
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
        "id": created_experiment["id"]
    }, 201

@app.route("/experiments", methods=["GET"])
def get_experiments():
    """ get all experiments or experiments by users id"""
    user_id = request.args.get("userId")

    if user_id:
        return experiment_store.get_all_by_user(int(user_id)), 200

    return experiment_store.get_all_experiments(),200

@app.route("/experiments/<int:experiment_id>", methods=["GET"])
def get_experiment(experiment_id):
    """ get an experiment by id """
    experiment = experiment_store.get_by_id(experiment_id)

    if not experiment:
        return {"error": "Experiment not found"}, 404
    return experiment, 200

@app.route("/experiments/<int:experiment_id>", methods=["PATCH"])
def update_experiment(experiment_id):
    """ update an experiment """
    data = request.get_json()
    updated_experiment = experiment_service.update_experiment(experiment_id, data)
    if not updated_experiment:
        return {"error": "Experiment not found"}, 404
    return updated_experiment, 200


@app.route("/experiments-results", methods=["GET"])
def getresults():
    results = results_portal.get_result_summaries()
    return jsonify(results), 200

if __name__ == "__main__":
    app.run(debug=True)
