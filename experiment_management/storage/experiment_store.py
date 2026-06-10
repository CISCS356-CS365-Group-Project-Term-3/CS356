from storage.db import SessionLocal
from storage.experiment_model import Experiment

def save_experiment(experiment):
    """ save an experiment to the database """
    session = SessionLocal()

    db_experiment = Experiment(
        userId=experiment["userId"],
        name=experiment["name"],
        status=experiment["status"],
        projectTypeId=experiment["projectTypeId"],
        createdAt=experiment["date"],
        data={
            "encoders": experiment["encoders"],
            "sequences": experiment["sequences"]
        }
    )

    session.add(db_experiment)
    session.commit()
    session.refresh(db_experiment)

    experiment["id"] = db_experiment.id

    session.close()

    return experiment

# filter experiments by user id
def get_all_experiments():
    session = SessionLocal()

    experiments = session.query(Experiment).all()

    result = []
    for e in experiments:
        result.append(serialize(e))

    session.close()
    return result

def get_by_id(experiment_id):
    session = SessionLocal()

    exp = session.query(Experiment).filter(Experiment.id == experiment_id).first()

    session.close()

    if not exp:
        return None

    return serialize(exp)

def get_all_by_user(userId):
    session = SessionLocal()

    experiments = session.query(Experiment).filter(
        Experiment.userId == userId
    ).all()

    result = [serialize(e) for e in experiments]

    session.close()
    return result

def serialize(exp):
    return {
        "id": exp.id,
        "userId": exp.userId,
        "name": exp.name,
        "status": exp.status,
        "projectTypeId": exp.projectTypeId,
        "date": exp.createdAt.isoformat() if exp.createdAt else None,
        "encoders": exp.data.get("encoders", []),
        "sequences": exp.data.get("sequences", [])
    }