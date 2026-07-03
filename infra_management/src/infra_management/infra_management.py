from flask import Flask, request
from .models.api_models import *
from .models.sql_models import *
from .util.engine import get_engine, Base, query_result_as_list, table_to_json
from .util.data_init import data_init
from .util.util import *
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from flask_cors import CORS
from pydantic import ValidationError


app = Flask(__name__)
CORS(app)
engine = None

def process_spacial(row):
    row["spacial"] = [row.get("spacial_x"), row.get("spacial_y")]

def standard_crud(request, table, handle_update, handle_create, post_model, put_model, proc=None):
    with Session(engine) as session:
        if request.method == "GET":
            rows = query_result_as_list(session.query(table).all())
            if proc:
                proc(rows)
            return rows
            
        elif request.method == "POST":
            try: 
                post_model.model_validate(request.json)
            except ValidationError as e:
                print("Json not in correct form")
                return {"status": False, "message": "Error, request malformed."}
            body = request.json # this mean that it is not a new project type
            id = body.get("id")
            rows = session.query(table).filter(table.id == id).all()
            if len(rows) == 1:
                row = rows[0]
                row = handle_update(row, body)
                session.commit()
                return {"status": True, "message": "row successfully updated."}
            else:
                print("id not found")
                {"status": False, "message": "Error, no rows matching ID"}
        elif request.method == "PUT":
            body = request.json
            try: 
                put_model.model_validate(request.json)
            except ValidationError as e:
                print("Json not in correct form")
                return {"status": False, "message": "Error, request malformed."}
            new_row = handle_create(table, body)
            session.add(new_row)
            session.commit()
            return {"status": True, "message": "row successfully created."}

        elif request.method == "DELETE":
            body = request.json
            try:
                IdDelete.model_validate(body)
            except ValidationError:
                print("JSON not in correct format")
                return {"status": False, "message": "Error, request malformed."}
            id = body.get("id")
            rows = session.query(table).filter(table.id == id).all()
            if len(rows) == 0:
                print("No rows found")
                return {"status": False, "message": "Error, no rows matching ID"}
            elif len(rows) > 1:
                print("Error: Multiple rows found.")
                {"status": False, "message": "Error, multiple rows found."}
            else:
                row = rows[0]
                session.delete(row)
                session.commit()
                return {"status": True, "message": "row successfully deleted."}

def standard_activate(request, table, proc=None):
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
            videos = query_result_as_list(session.query(VideoFile).filter(and_(or_(VideoFile.active == 1, filter == False), VideoFile.sequence_id == id)))
            for vid in videos:
                vid["spacial"] = [vid.get("spacial_x"), vid.get("spacial_y")]
                vid.pop("spacial_x", None)
                vid.pop("spacial_y", None)
            sequence["video_files"] = videos


        encoder_types = []
        for encoder_type in encoder_type_rows:
            encoder_type_json = table_to_json(encoder_type)
            active_codecs = [c.id for c in encoder_type.codecs if c.active == 1]
            encoder_type_json["active_codecs"] = active_codecs
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

@app.route("/rest/project_types", methods=["GET", "POST", "PUT"])
def project_types():
     return standard_crud(request, EncoderType, name_id_update, name_id_create, NameIdUpdate, NameIdCreate)

@app.route("/rest/encoder_types", methods=["GET", "POST", "PUT"])
def encoder_types():
    return standard_crud(request, EncoderType, name_id_update, name_id_create, NameIdUpdate, NameIdCreate)

@app.route("/rest/encoder_modes", methods=["GET", "POST", "PUT"])
def encoder_modes():
    return standard_crud(request, EncoderMode, name_id_update, name_id_create, NameIdUpdate, NameIdCreate)
            
@app.route("/rest/codecs", methods=["GET", "POST", "PUT"])
def codecs():
    return standard_crud(request, Codec, codec_update, codec_create, CodecUpdate, CodecCreate)

@app.route("/rest/topologies", methods=["GET", "POST", "PUT"])
def topologies():
    return standard_crud(request, Codec, name_id_update, name_id_create, NameIdUpdate, NameIdCreate)

@app.route("/rest/transmission_conditions", methods=["GET", "POST", "PUT"])
def transmission_conditions():
    return standard_crud(request, TransmissionCondition, transmission_update, transmission_create, TransmissionConditionUpdate, TransmissionConditionCreate)

@app.route("/rest/sequences", methods=["GET", "POST", "PUT"])
def sequences():
    return standard_crud(request, Sequence, sequence_update, sequence_create, SequenceUpdate, SequenceCreate)

@app.route("/rest/video_files", methods=["GET", "POST", "PUT"])
def video_files():
    return standard_crud(request, VideoFile, video_file_update, video_file_create, VideoFileUpdate, VideoFileCreate)

@app.route("/rest/mappings", methods=["GET"])
def get_mappings():
    output = {}
    with Session(engine) as session:
        file_rows = session.query(VideoFile)
        files = {}
        for file in file_rows:
            name = file.name
            id = str(file.id).rjust(3, "0")
            files[id] = name
        output["raw_file"] = files
        codec_rows = session.query(Codec)
        codecs = {}
        for codec in codec_rows:
            name = codec.name
            id = str(codec.id).rjust(3, "0")
            codecs[id] = name
        output["codec"] = codecs
    return output

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200

def main():
    global engine
    engine = get_engine()
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        if len(session.query(ProjectType).all()) == 0:
            data_init()
    app.run(host = "0.0.0.0", port=5001)
