from flask import Flask, request

app = Flask(__name__)

@app.route("/rest/get_ui_options", methods=["GET"])
def get_ui_options():
    return {}

