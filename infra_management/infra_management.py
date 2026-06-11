from flask import Flask, request
from flask_cors import CORS
from models.api_models import *
from models.sql_models import *
from util.engine import get_engine, Base, query_result_as_list
from util.data_init import data_init
from sqlalchemy.orm import Session


app = Flask(__name__)
CORS(app)
engine = None

def name_id_create(table, body):
    name = body.get("name") #Name should already be validated at this point.
    return table(name=name)

def name_id_update(row, body):
    name = body.get("name")
    row.name = name
    return row

def transmission_create(table, body): #These could be further colapsed into a single function that creates a new instance using **kwargs
    name = body.get("name")
    lower_bound = body.get("lower_bound")
    upper_bound = body.get("upper_bound")
    return table(
        name = name,
        lower_bound = lower_bound,
        upper_bound = upper_bound
    )

def transmission_update(row, body):
    name = body.get("name")
    lower_bound = body.get("lower_bound")
    upper_bound = body.get("upper_bound")
    row.name = name if name else row.name
    row.lower_bound = lower_bound if lower_bound else row.lower_bound
    row.upper_bound = upper_bound if upper_bound else row.upper_bound
    return row

def sequence_create(table, body):
    name = body.get("name")
    description = body.get("description")
    return table(name = name, description = description)

def sequence_update(row, body):
    name = body.get("name")
    description = body.get("description")
    row.name = name if name else row.name
    row.description = description if description else row.description
    return row

def video_file_create(table, body):
    return table(
        sequence_id = body.get("sequence_id"),
        name = body.get("name"),
        filepath = body.get("filepath"),
        spacial_x = body.get("spacial")[0],
        spacial_y = body.get("spacial")[1],
        temporal = body.get("temporal"),
        depth = body.get("depth"),
        quality = body.get("quality"),
        gamut = body.get("gamut")
    )

def video_file_update(row, body):
    row.sequence_id = body.get("sequence_id") if body.get("sequence_id") else row.sequence_id
    row.name = body.get("name") if body.get("name") else row.name
    row.filepath = body.get("filepath") if body.get("filepath") else row.filepath
    row.depth = body.get("depth") if body.get("depth") else row.depth
    row.quality = body.get("quality") if body.get("quality") else row.quality
    row.gamut = body.get("gamut") if body.get("gamut") else row.gamut
    if body.get("spacial"):
        row.spacial_x = body.get("spacial")[0]
        row.spacial_y = body.get("spacial")[1]
    row.spacial_x = body.get("spacial") if body.get("spacial") else row.spacial
    return row

def codec_update(row, body):
    row.version = body.get("version") if body.get("version") else row.version
    row.satus = body.get("status") if body.get("status") else row.status
    row.filepath = body.get("filepath") if body.get("filepath") else row.filepath
    row.name = body.get("name") if body.get("name") else row.name

def codec_create(table, body):
    return table(
        name = body.get("name"),
        status = body.get("status"),
        version = body.get("version")
    )

def process_spacial(row):
    row["spacial"] = [row.get("spacial_x"), row.get("spacial_y")]

def standard_crud(request, table, handle_update, handle_create, post_model, delete_model, proc=None):
    with Session(engine) as session:
        if request.method == "GET":
            rows = query_result_as_list(session.query(table).all())
            if proc:
                proc(rows)
            return rows
            
        elif request.method == "POST":
            if not post_model.model_validate(request.json):
                print("Json not in correct form")
                return {"status": False, "message": "Error, request malformed."}
            print("Got a POST request")
            body = request.json
            if body.get("id"): # this mean that it is not a new project type
                id = body.get("id")
                if id:
                    rows = session.query(table).filter(table.id == id).all()
                    if len(rows) == 1:
                        row = rows[0]
                        row = handle_update(row, body)
                        session.commit()
                        return {"status": True, "message": "row successfully updated."}
                    else:
                        print("id not found")
                        {"status": False, "message": "Error, no rows matching ID"}
            else:
                print("No ID found, creating new row.")
                new_row = handle_create(table, body)
                session.add(new_row)
                session.commit()
                return {"status": True, "message": "row successfully created."}

        elif request.method == "DELETE":
            body = request.json
            if not delete_model.model_validate(body):
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

@app.route("/rest/get_ui_options", methods=["GET"])
def get_ui_options():
    global engine
    with Session(engine) as session:
        project_types = query_result_as_list(session.query(ProjectType).all())
        encoder_types = query_result_as_list(session.query(EncoderType).all())
        codecs = query_result_as_list(session.query(Codec).all())
        encoder_modes = query_result_as_list(session.query(EncoderMode).all())
        sequences = query_result_as_list(session.query(Sequence).all())
        topologies = query_result_as_list(session.query(Topology).all())
        transmission_conditions = query_result_as_list(session.query(TransmissionCondition).all())
        for sequence in sequences:
            id = sequence.get("id")
            print(f"Looking for id: {id}")
            videos = query_result_as_list(session.query(VideoFile).filter(VideoFile.sequence_id == id))
            for vid in videos:
                vid["spacial"] = [vid.get("spacial_x"), vid.get("spacial_y")]
                vid.pop("spacial_x", None)
                vid.pop("spacial_y", None)
            sequence["video_files"] = videos


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

@app.route("/rest/project_types", methods=["GET", "POST", "DELETE"])
def project_types():
    return standard_crud(request, ProjectType, name_id_update, name_id_create, NameIdPost, IdDelete)

@app.route("/rest/encoder_types", methods=["GET", "POST", "DELETE"])
def encoder_types():
    return standard_crud(request, EncoderType, sequence_update, sequence_create, SequencePost, IdDelete) #Happens to share the same structure as the sequences, no point duplicating.

@app.route("/rest/encoder_modes", methods=["GET", "POST", "DELETE"])
def encoder_modes():
    return standard_crud(request, EncoderMode, name_id_update, name_id_create, NameIdPost, IdDelete)
            
@app.route("/rest/codecs", methods=["GET", "POST", "DELETE"])
def codecs():
    return standard_crud(request, Codec, codec_update, codec_create, CodecPost, IdDelete)

@app.route("/rest/topologies", methods=["GET", "POST", "DELETE"])
def topologies():
    return standard_crud(request, Topology, name_id_update, name_id_create, NameIdPost, IdDelete)

@app.route("/rest/transmission_conditions", methods=["GET", "POST", "DELETE"])
def transmission_conditions():
    return standard_crud(request, TransmissionCondition, transmission_update, transmission_create, TransmissionConditionPost, IdDelete)

@app.route("/rest/sequences", methods=["GET", "POST", "DELETE"])
def sequences():
    return standard_crud(request, Sequence, sequence_update, sequence_create, SequencePost, IdDelete)

@app.route("/rest/video_files", methods=["GET", "POST", "DELETE"])
def video_files():
    return standard_crud(request, VideoFile, video_file_update, video_file_create, VideoFilePost, IdDelete)

def main():
    global engine
    engine = get_engine()
    Base.metadata.create_all(engine)
    data_init()
    app.run(host = "0.0.0.0", port=5001)

main()
