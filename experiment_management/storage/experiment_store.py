from storage.db import SessionLocal
from storage.experiment_model import Experiment

def save_experiment(experiment):
    """ save an experiment to the database """
    session = SessionLocal()

    db_experiment = Experiment(
        user_id=experiment["user_id"],
        name=experiment["name"],
        status=experiment["status"],
        project_type_id=experiment["project_type_id"],
        created_at=experiment["date"],
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

def get_all_by_user(user_id):
    session = SessionLocal()

    experiments = session.query(Experiment).filter(
        Experiment.user_id == user_id
    ).all()

    result = [serialize(e) for e in experiments]

    session.close()
    return result

def serialize(exp):
    return {
        "id": exp.id,
        "user_id": exp.user_id,
        "name": exp.name,
        "status": exp.status,
        "project_type_id": exp.project_type_id,
        "date": exp.created_at.isoformat() if exp.created_at else None,
        "encoders": exp.data.get("encoders", []),
        "sequences": exp.data.get("sequences", [])
    }