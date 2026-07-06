import logging
import os
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS
from services import results_portal
from storage import results_store

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)

app = Flask(__name__)
CORS(app)

@app.route("/experiments-results", methods=["GET"])
def getresults():
    results = results_portal.get_all_result_summaries()
    return jsonify(results), 200

@app.route("/user/experiments-results", methods=["GET"])
def get_user_results():
    user_id = request.args.get("userId")

    results = results_portal.get_user_result_summaries(user_id)
    return jsonify(results), 200


@app.route("/experiments-results/<int:experiment_id>/frames", methods=["GET"])
def get_experiment_frames(experiment_id):
    frames = results_portal.get_experiment_frames(experiment_id)
    if frames is None:
        return {"error": "No results found for experiment"}, 404
    return jsonify(frames), 200

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(debug=True)
