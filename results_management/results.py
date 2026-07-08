import logging
import math
import os
import sys

from flask import Flask, jsonify, request
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS
from services import results_portal
from storage import results_store


# JSON cannot represent Infinity/NaN
PERFECT_PSNR_DB = 0


def _json_safe(value):
    if isinstance(value, float):
        if math.isnan(value):
            return None
        if math.isinf(value):
            return PERFECT_PSNR_DB if value > 0 else None
        return value
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return value


class SafeJSONProvider(DefaultJSONProvider):
    def dumps(self, obj, **kwargs):
        return super().dumps(_json_safe(obj), **kwargs)

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)

app = Flask(__name__)
app.json = SafeJSONProvider(app)
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
