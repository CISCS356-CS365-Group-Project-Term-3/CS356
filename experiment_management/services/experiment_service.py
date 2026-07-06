from datetime import datetime

from queue_setup.publisher import publish_to_queue
from storage.experiment_store import save_group, save_run
from storage.experiment_store import update_group_by_id
from storage.experiment_store import get_group_by_id
from utils.encoding import generate_sequence_code

from experiment_management.storage.experiment_store import update_run_status


def create_experiment(data):
    user_id = data.get("userId")
    status = data.get("status", "draft")
    name = data.get("name")
    project_type_id = data.get("projectTypeId")
    encoders = data.get("encoders") or []
    sequences = data.get("sequences") or []
    networkEmulation = data.get("networkEmulation") or {}
    date = datetime.utcnow().isoformat()

    group = save_group({
        "userId": user_id,
        "name": name,
        "status": "draft" if status == "draft" else "pending",
        "projectTypeId": project_type_id,
        "date": date,
        "draftData": {
            "encoders": encoders,
            "sequences": sequences,
            "networkEmulation": networkEmulation
        } if status == "draft" else None
    })
    if status == "draft":
        return {
            "group": group,
            "draftData": group.get("draftData")
        }
    runs = []
    packet_losses = networkEmulation.get("packetLoss", [])
    delays = networkEmulation.get("delay", [])
    jitters = networkEmulation.get("jitter", [])

    for encoder in encoders:
        for seq in sequences:
            for i in range(max(len(packet_losses), len(delays), len(jitters))):
                condition = {
                    "packetLoss": packet_losses[i] if i < len(packet_losses) else "000",
                    "delay": delays[i] if i < len(delays) else "000",
                    "jitter": jitters[i] if i < len(jitters) else "000"
                }
                code = generate_sequence_code(seq, encoder, condition)

                run = save_run({
                    "groupId": group["id"],
                    "sequenceCode": code,
                    "status": "pending",
                    "date": date,
                    "encoderData": encoder,
                    "sequenceData": seq,
                    "networkData": condition
                })
                runs.append(run)
                publish_to_queue({
                    "group_id": group["id"],
                    "run_id": run["id"],
                    "date": date,
                    "sequence_code": code,
                    "userId": user_id
                })
    return {
        "group": group,
        "runs": runs
    }

def update_experiment(group_id, data):
    existing = get_group_by_id(group_id)
    if not existing:
        return None
    draft = existing.get("draftData", {})
    updated = {
        "userId": data.get("userId", existing["userId"]),
        "name": data.get("name", existing["name"]),
        "status": data.get("status", existing["status"]),
        "projectTypeId": data.get("projectTypeId", existing["projectTypeId"]),
        "encoders": data.get("encoders", draft.get("encoders", [])),
        "sequences": data.get("sequences", draft.get("sequences", [])),
        "networkEmulation": data.get("networkEmulation", draft.get("networkEmulation", {})),
        "date": datetime.utcnow().isoformat()
    }

    if updated["status"] == "draft":
        group = update_group_by_id(group_id, {
            "userId": updated["userId"],
            "name": updated["name"],
            "status": updated["status"],
            "projectTypeId": updated["projectTypeId"],
            "date": updated["date"],
            "draftData": {
                "encoders": updated["encoders"],
                "sequences": updated["sequences"],
                "networkEmulation": updated["networkEmulation"]
            }
        })
        return {
            "group": group,
            "draftData": group.get("draftData")
        }

    runs = []
    network_emulation = updated["networkEmulation"]
    packet_losses = network_emulation.get("packetLoss", [])
    delays = network_emulation.get("delay", [])
    jitters = network_emulation.get("jitter", [])

    group = update_group_by_id(group_id, {
        "userId": updated["userId"],
        "name": updated["name"],
        "status": "pending",
        "projectTypeId": updated["projectTypeId"],
        "date": updated["date"],
        "draftData": None
    })
    for encoder in updated["encoders"]:
        for seq in updated["sequences"]:
            for i in range(max(len(packet_losses), len(delays), len(jitters))):
                condition = {
                    "packetLoss": packet_losses[i] if i < len(packet_losses) else "000",
                    "delay": delays[i] if i < len(delays) else "000",
                    "jitter": jitters[i] if i < len(jitters) else "000"
                }
                code = generate_sequence_code(seq, encoder, condition)
                run = save_run({
                    "groupId": group_id,
                    "sequenceCode": code,
                    "status": "pending",
                    "date": updated["date"],
                    "encoderData": encoder,
                    "sequenceData": seq,
                    "networkData": condition
                })
                runs.append(run)
                publish_to_queue({
                    "group_id": group_id,
                    "run_id": run["id"],
                    "date": updated["date"],
                    "sequence_code": code,
                    "userId": updated["userId"]
                })
    return {
        "group": group,
        "runs": runs
    }
# service functions for engine to use
# difficult to check the state of the message queue from publisher so
# going to check from consumer side and provide these service functions
def mark_run_running(run_id):
    update_run_status(run_id, "running")
def mark_run_complete(run_id):
    update_run_status(run_id, "complete")
def mark_run_failed(run_id):
    update_run_status(run_id, "failed")