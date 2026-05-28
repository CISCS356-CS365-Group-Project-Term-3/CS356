from flask import Flask, request
from services import experiment_service
from storage import experiment_store

app = Flask(__name__)

@app.route("/experiments", methods=["POST"])
def create_experiment_endpoint():
    """ create an experiment endpoint """
    data = request.get_json()
    experiment_service.create_experiment(data)

    return "", 204

@app.route("/experiments", methods=["GET"])
def get_experiments():
    user_id = int(request.args.get("user_id"))
    # Ideally we dont want this function to live with the DB logic but should be in the service layer
    # But I am just going with it for now to test
    return experiment_store.get_all_by_user(user_id)

if __name__ == "__main__":
    app.run(debug=True)