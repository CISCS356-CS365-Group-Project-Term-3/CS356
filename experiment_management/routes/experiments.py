from flask import Flask, request
from services import experiment_service

""" 
Endpoints are defined here should be simple and modular 
I will add 
1. Retrieving experiment information api from storage
"""
app = Flask(__name__)

@app.route("/experiments", methods=["POST"])
def create_experiment():
    data = request.get_json()
    experiment_service.create_experiment(data)

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)