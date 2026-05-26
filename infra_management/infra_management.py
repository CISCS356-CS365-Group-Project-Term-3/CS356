from flask import Flask, request
from models.api_models import UiOptions
from models.sql_models import ProjectType, EncoderModes, EncoderType, VideoFile
from util.engine import get_engine, Base
from util.data_init import data_init
from sqlalchemy.orm import Session


app = Flask(__name__)
engine = None

@app.route("/rest/get_ui_options", methods=["GET"])
def get_ui_options() -> UiOptions:
    global engine
    with Session(engine) as session:
        pass
        #result = session.query(TestTable).all()
        #print(result)
    return {}

def main():
    global engine
    engine = get_engine()
    Base.metadata.create_all(engine)
    data_init()
    app.run(host = "0.0.0.0", port=5001)

main()
