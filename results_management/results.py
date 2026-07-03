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
