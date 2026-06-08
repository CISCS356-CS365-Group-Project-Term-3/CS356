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
    with Session(engine) as session:
        project_types = query_result_as_list(session.query(ProjectType).all())
        encoder_types = query_result_as_list(session.query(EncoderType).all())
        codecs = query_result_as_list(session.query(Codec).all())
        encoder_modes = query_result_as_list(session.query(EncoderModes).all())
        sequences = query_result_as_list(session.query(Sequence).all())
        topologies = query_result_as_list(session.query(Topology).all())
        transmission_conditions = query_result_as_list(session.query(TransmissionCondition).all())
        for sequence in sequences:
            id = sequence.get("id")
            print(f"Looking for id: {id}")
            videos = query_result_as_list(session.query(VideoFile).filter(VideoFile.sequence_id == id))
            sequence["video_files"] = videos

        output = {
            "project_types": project_types,
            "encoder_modes": encoder_modes,
            "encoder_type": encoder_types,
            "codecs": codecs,
            "topologies": topologies,
            "transmission_conditions": transmission_conditions,
            "sequences": sequences
        }

        # try:
        #     UiOptions.model_dump(output)
        # except Exception as e:
        #     return f"Error occured.: {e}"
        
    return output

def main():
    global engine
    engine = get_engine()
    Base.metadata.create_all(engine)
    data_init()
    app.run(host = "0.0.0.0", port=5001)

main()
