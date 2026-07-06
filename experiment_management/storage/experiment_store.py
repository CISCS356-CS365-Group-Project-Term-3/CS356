from storage.db import SessionLocal

from storage.experiment_group_model import ExperimentGroup
from storage.experiment_run_model import ExperimentRun

def save_group(group):
    session = SessionLocal()
    db_group = ExperimentGroup(
        userId=group["userId"],
        name=group["name"],
        status=group["status"],
        projectTypeId=group["projectTypeId"],
        createdAt=group.get("date"),
        draftData=group.get("draftData")
    )
    session.add(db_group)
    session.commit()
    session.refresh(db_group)
    group["id"] = db_group.id
    session.close()
    return group

def save_run(run):
    session = SessionLocal()
    db_run = ExperimentRun(
        groupId=run.get("groupId"),
        sequenceCode=run.get("sequenceCode"),
        status=run.get("status"),
        createdAt=run.get("date"),
        encoderData=run.get("encoderData"),
        sequenceData=run.get("sequenceData"),
        networkData=run.get("networkData")
    )
    session.add(db_run)
    session.commit()
    session.refresh(db_run)
    run["id"] = db_run.id
    session.close()
    return run

def get_runs_by_group_id(group_id):
    session = SessionLocal()
    runs = session.query(ExperimentRun).filter(
        ExperimentRun.groupId == group_id
    ).all()
    result = []
    for run in runs:
        result.append({
            "id": run.id,
            "groupId": run.groupId,
            "sequenceCode": run.sequenceCode,
            "status": run.status,
            "date": run.createdAt.isoformat() if run.createdAt else None,
            "encoderData": run.encoderData,
            "sequenceData": run.sequenceData,
            "networkData": run.networkData
        })
    session.close()
    return result

def get_groups_by_userID(user_id):
    session = SessionLocal()
    groups = session.query(ExperimentGroup).filter(
        ExperimentGroup.userId == user_id
    ).all()
    result = []
    for group in groups:
        runs = get_runs_by_group_id(group.id)
        group_dict = {
            "groupID": group.id,
            "userId": group.userId,
            "name": group.name,
            "status": group.status,
            "projectTypeId": group.projectTypeId,
            "date": group.createdAt.isoformat()
        }
        if group.status == "draft":
            group_dict["draftData"] = group.draftData
        group_dict["runs"] = runs
        result.append(group_dict)
    session.close()

    return result

def get_all_groups():
    session = SessionLocal()
    groups = session.query(ExperimentGroup).all()
    result = []
    for group in groups:
        runs = get_runs_by_group_id(group.id)
        group_dict = {
            "groupID": group.id,
            "userId": group.userId,
            "name": group.name,
            "status": group.status,
            "projectTypeId": group.projectTypeId,
            "date": group.createdAt.isoformat()
        }
        if group.status == "draft":
            group_dict["draftData"] = group.draftData
        group_dict["runs"] = runs
        result.append(group_dict)
    session.close()
    return result

def get_group_by_id(group_id):
    session = SessionLocal()
    group = session.query(ExperimentGroup).filter(
        ExperimentGroup.id == group_id
    ).first()
    session.close()
    if not group:
        return None
    runs = get_runs_by_group_id(group_id)
    group_dict = {
        "groupID": group.id,
        "userId": group.userId,
        "name": group.name,
        "status": group.status,
        "projectTypeId": group.projectTypeId,
        "date": group.createdAt.isoformat()
    }
    if group.status == "draft":
        group_dict["draftData"] = group.draftData
    group_dict["runs"] = runs
    return group_dict

def update_group_by_id(group_id, group_data):
    session = SessionLocal()
    group = session.query(ExperimentGroup).filter(
        ExperimentGroup.id == group_id
    ).first()

    if not group:
        session.close()
        return None
    group.userId = group_data["userId"]
    group.name = group_data["name"]
    group.status = group_data["status"]
    group.projectTypeId = group_data["projectTypeId"]
    group.createdAt = group_data["date"]
    group.draftData = group_data["draftData"]

    session.commit()
    session.refresh(group)

    runs = get_runs_by_group_id(group_id)
    group_dict = {
        "groupID": group.id,
        "userId": group.userId,
        "name": group.name,
        "status": group.status,
        "projectTypeId": group.projectTypeId,
        "date": group.createdAt.isoformat()
    }
    if group.status == "draft":
        group_dict["draftData"] = group.draftData
    group_dict["runs"] = runs

    session.close()

    return group_dict
# update a runs status field in the db
def update_run_status(run_id, status):
    session = SessionLocal()
    run = (
        session.query(ExperimentRun)
        .filter(ExperimentRun.id == run_id)
        .first()
    )
    if not run:
        session.close()
        return None

    run.status = status
    session.commit()
    session.refresh(run)
    session.close()
    return run