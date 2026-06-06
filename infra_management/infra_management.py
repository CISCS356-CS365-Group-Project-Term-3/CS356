from flask import Flask, request
from models.api_models import *
from models.sql_models import *
from util.engine import get_engine, Base, query_result_as_list
from util.data_init import data_init
from sqlalchemy.orm import Session


app = Flask(__name__)
engine = None

@app.route("/rest/get_ui_options", methods=["GET"])
def get_ui_options():
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

@app.route("/rest/encoder_types", methods=["GET", "POST", "DELETE"])
def project_types():
    if request.method == "GET":
        with Session(engine) as session:
            project_types = query_result_as_list(session.query(EncoderType).all())
            return project_types
        
    elif request.method == "POST":
        if not PostProjectType.model_validate(request.json):
            print("Json not in correct form")
            return {"status": False, "message": "Error, request malformed."}
        print("Got a POST request")
        body = request.json
        if body.get("id"): # this mean that it is not a new project type
            id = body.get("id")
            with Session(engine) as session:
                if id:
                    rows = session.query(ProjectType).filter(ProjectType.id == id).all()
                    if len(rows) == 1:
                        row = rows[0]
                        row.name = body.get("name") if body.get("name") else row.name
                        session.commit()
                        return {"status": True, "message": "row successfully updated."}
                    else:
                        print("id not found")
                        {"status": False, "message": "Error, no rows matching ID"}
        else:
            print("No ID found, creating new row.")
            with Session(engine) as session:
                new_row = ProjectType(
                    name = body.get("name")
                )
                session.add(new_row)
                session.commit()
                return {"status": True, "message": "row successfully created."}

    elif request.method == "DELETE":
        body = request.json
        if not DeleteProjectType.model_validate(body):
            print("JSON not in correct format")
            return {"status": False, "message": "Error, request malformed."}
        id = body.get("id")
        with Session(engine) as session:
            rows = session.query(ProjectType).filter(ProjectType.id == id).all()
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

@app.route("/rest/encoder_types", methods=["GET", "POST", "DELETE"])
def encoder_types():
    if request.method == "GET":
        with Session(engine) as session:
            encoder_types = query_result_as_list(session.query(EncoderType).all())
            return encoder_types
        
    elif request.method == "POST":
        if not PostProjectType.model_validate(request.json):
            print("Json not in correct form")
            return {"status": False, "message": "Error, request malformed."}
        print("Got a POST request")
        body = request.json
        if body.get("id"): # this mean that it is not a new project type
            id = body.get("id")
            with Session(engine) as session:
                if id:
                    rows = session.query(EncoderType).filter(EncoderType.id == id).all()
                    if len(rows) == 1:
                        row = rows[0]
                        row.name = body.get("name") if body.get("name") else row.name
                        session.commit()
                        return {"status": True, "message": "row successfully updated."}
                    else:
                        print("id not found")
                        {"status": False, "message": "Error, no rows matching ID"}
        else:
            print("No ID found, creating new row.")
            with Session(engine) as session:
                new_row = EncoderType(
                    name = body.get("name")
                )
                session.add(new_row)
                session.commit()
                return {"status": True, "message": "row successfully created."}

    elif request.method == "DELETE":
        body = request.json
        if not DeleteProjectType.model_validate(body):
            print("JSON not in correct format")
            return {"status": False, "message": "Error, request malformed."}
        id = body.get("id")
        with Session(engine) as session:
            rows = session.query(EncoderType).filter(EncoderType.id == id).all()
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

def main():
    global engine
    engine = get_engine()
    Base.metadata.create_all(engine)
    data_init()
    app.run(host = "0.0.0.0", port=5001)

main()
