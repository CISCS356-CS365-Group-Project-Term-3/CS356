from flask import Flask, request
from services import experiment_service
app = Flask(__name__)

@app.route("/experiments", methods=["POST"])
def create_experiment_endpoint():
    """ create an experiment endpoint """
    data = request.get_json()
    experiment_service.create_experiment(data)

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)