from flask import Flask, request
from models.api_models import UiOptions
from models.sql_models import *
from util.engine import get_engine, Base, query_result_as_list
from util.data_init import data_init
from sqlalchemy.orm import Session


app = Flask(__name__)
engine = None

@app.route("/rest/get_ui_options", methods=["GET"])
def get_ui_options() -> UiOptions:
    global engine
    output = {}
    with Session(engine) as session:
        project_types = query_result_as_list(session.query(ProjectType).all())
        encoder_types = query_result_as_list(session.query(EncoderType).all())
        codecs = query_result_as_list(session.query(Codec).all())
        encoder_modes = query_result_as_list(session.query(EncoderModes).all())
        video_files = query_result_as_list(session.query(VideoFile).all())
        codecs = query_result_as_list(session.query(Codec).all())
        topologies = query_result_as_list(session.query(Topology).all())
        transmission_conditions = query_result_as_list(session.query(TransmissionCondition).all())
        output = {
            "project_types": project_types,
            "encoder_types": encoder_types,
            "codecs": codecs,
            "encoder_modes": encoder_modes,
            "video_files": video_files,
            "topologies": topologies,
            "transmission_conditions": transmission_conditions
        }


    return output

def main():
    global engine
    engine = get_engine()
    Base.metadata.create_all(engine)
    data_init()
    app.run(host = "0.0.0.0", port=5001)

main()
