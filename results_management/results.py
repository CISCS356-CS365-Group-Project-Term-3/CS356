from flask import Flask, jsonify
from flask_cors import CORS
from services import results_portal
from storage import results_store

app = Flask(__name__)
CORS(app)

@app.route("/experiments-results", methods=["GET"])
def getresults():
    results = results_portal.get_result_summaries()
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