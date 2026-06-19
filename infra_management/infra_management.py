from flask import Flask, request
from models.api_models import *
from models.sql_models import *
from util.engine import get_engine, Base, query_result_as_list, table_to_json
from util.data_init import data_init
from sqlalchemy.orm import Session
from sqlalchemy import or_
from flask_cors import CORS
from pydantic import ValidationError


app = Flask(__name__)
CORS(app)
engine = None

def process_spacial(row):
    row["spacial"] = [row.get("spacial_x"), row.get("spacial_y")]

def standard_crud(request, table, proc=None):
    with Session(engine) as session:
        if request.method == "GET":
            rows = query_result_as_list(session.query(table).all())
            if proc:
                proc(rows)
            return rows
            
        elif request.method == "POST":
            try: 
                ToggleActiveRequest.model_validate(request.json)
            except ValidationError as e:
                print("Json not in correct form")
                return {"status": False, "message": "Error, request malformed."}
            print("Got a POST request")
            body = request.json
            id = body.get("id")
            rows = session.query(table).filter(table.id == id).all()
            if len(rows) != 1:
                print(f"Could not find a row with id {id}")
                return {"status": False, "message": f"Error, could not find row with id {id}"}
            row = rows[0]
            row.active = body.get("active")
            session.commit()
            return {"status": True, "message": f"Successfully set row with id {id} to active {body.get("active")}"}


def get_ui_options(filter=False):
    global engine
    with Session(engine) as session:
        project_types = query_result_as_list(session.query(ProjectType).filter(or_(ProjectType.active == 1, filter == False)).all())
        encoder_type_rows = session.query(EncoderType).filter(or_(EncoderType.active == 1, filter == False)).all()
        codecs = query_result_as_list(session.query(Codec).filter(or_(Codec.active == 1, filter == False)).all())
        encoder_modes = query_result_as_list(session.query(EncoderMode).filter(or_(EncoderMode.active == 1, filter == False)).all())
        sequences = query_result_as_list(session.query(Sequence).filter(or_(Sequence.active == 1, filter == False)).all())
        topologies = query_result_as_list(session.query(Topology).filter(or_(Topology.active == 1, filter == False)).all())
        transmission_conditions = query_result_as_list(session.query(TransmissionCondition).filter(or_(TransmissionCondition.active == 1, filter == False)).all())
        for sequence in sequences:
            id = sequence.get("id")
            videos = query_result_as_list(session.query(VideoFile).filter(or_(VideoFile.sequence_id == id, VideoFile.active == 1, filter == False)))
            for vid in videos:
                vid["spacial"] = [vid.get("spacial_x"), vid.get("spacial_y")]
                vid.pop("spacial_x", None)
                vid.pop("spacial_y", None)
            sequence["video_files"] = videos


        encoder_types = []
        for encoder_type in encoder_type_rows:
            encoder_type_json = table_to_json(encoder_type)
            active_codecs = [c.id for c in encoder_type.codecs if c.active == 1]
            encoder_type_json["active_codeds"] = active_codecs
            encoder_types.append(encoder_type_json)

        output = {
            "project_types": project_types,
            "encoder_modes": encoder_modes,
            "encoder_types": encoder_types,
            "codecs": codecs,
            "topologies": topologies,
            "transmission_conditions": transmission_conditions,
            "sequences": sequences
        }

        return output
    
@app.route("/rest/get_ui_options", methods=["GET"])
def get_all_ui_options():
    return get_ui_options(filter=False)

@app.route("/rest/get_active_ui_options", methods=["GET"])
def get_active_ui_options():
    return get_ui_options(filter=True)

@app.route("/rest/project_types", methods=["GET", "POST"])
def project_types():
    return standard_crud(request, ProjectType)

@app.route("/rest/encoder_types", methods=["GET", "POST"])
def encoder_types():
    return standard_crud(request, EncoderType)

@app.route("/rest/encoder_modes", methods=["GET", "POST"])
def encoder_modes():
    return standard_crud(request, EncoderMode)
            
@app.route("/rest/codecs", methods=["GET", "POST"])
def codecs():
    return standard_crud(request, Codec)

@app.route("/rest/topologies", methods=["GET", "POST"])
def topologies():
    return standard_crud(request, Topology)

@app.route("/rest/transmission_conditions", methods=["GET", "POST"])
def transmission_conditions():
    return standard_crud(request, TransmissionCondition)

@app.route("/rest/sequences", methods=["GET", "POST"])
def sequences():
    return standard_crud(request, Sequence)

@app.route("/rest/video_files", methods=["GET", "POST"])
def video_files():
    return standard_crud(request, VideoFile)

def main():
    global engine
    engine = get_engine()
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        if len(session.query(ProjectType).all()) == 0:
            data_init()
    app.run(host = "0.0.0.0", port=5001)

main()
