import json
import logging
import os

import requests

from storage import results_store


logger = logging.getLogger(__name__)


def _metadata_object(value):
    """Return metadata stored as an object, including legacy one-item lists."""
    if isinstance(value, list):
        value = value[0] if value else {}
    return value if isinstance(value, dict) else {}


def get_all_user_experiment_metadata(user_id, all_users=False):
    """ look up the postgres experiment row tied to a mongo result, if any """
    if user_id is None and all_users == False:
        return None
    try:
        EXPERIMENT_MANAGEMENT_ADDRESS = os.getenv("EXPERIMENT_MANAGEMENT_ADDRESS", "localhost:5000")

        if all_users:
            url = f"{EXPERIMENT_MANAGEMENT_ADDRESS}/experiments"
        else:
            url = f"{EXPERIMENT_MANAGEMENT_ADDRESS}/experiments/user/{user_id}"

        response = requests.get(url)
        if response.status_code != 200:
            logger.error(
                "Experiment metadata request failed: url=%s status=%s response=%s",
                url,
                response.status_code,
                response.text,
            )
            return None

        body = response.json()

        logger.info("experiment metadata response: %s", body)

        runs = []
        for group in body:
            for run in group.get("runs"):
                run['name']=group.get('name')
                runs.append(run)

        return runs
    except Exception:
        logger.exception("Experiment metadata lookup failed")
        return None
    

def clean_result(doc, metadata):
    project = doc.get("project", {})
    result = doc.get("result", {})

    psnr_average = result.get("psnr", {}).get("average", {})
    ssim_average = result.get("ssim", {}).get("average", {})
    psnr_raw_combined = result.get("psnr", {}).get("raw", {}).get("combined", [])

    experiment = metadata or {}
    encoder = _metadata_object(experiment.get("encoderData"))
    sequence = _metadata_object(experiment.get("sequenceData"))

    cleaned_doc = {
    "experimentId": project.get("experiment_id"),
    "experimentName": experiment.get("name") if experiment else None,
    "batchId": experiment.get("groupId") if experiment else None,
    "groupId": project.get("group_id"),
    "userId": project.get("user_id"),
    "createdAt": project.get("created_at"),
    "sequenceCode": doc.get("sequence"),
    "videoFileId": sequence.get("videoFileId"),
    "codecId": encoder.get("codecId"),
    "success": doc.get("success"),
    "failureReason": result.get("reason"),
    "frameCount": len(psnr_raw_combined),
    "psnrAverage": {
        "y": psnr_average.get("y"),
        "u": psnr_average.get("u"),
        "v": psnr_average.get("v"),
        "combined": psnr_average.get("combined"),
    },
    "ssimAverage": {
        "y": ssim_average.get("y"),
        "u": ssim_average.get("u"),
        "v": ssim_average.get("v"),
        "combined": ssim_average.get("combined"),
    },
}

    return cleaned_doc

def get_experiment_frames(experiment_id):
    doc = results_store.get_frame_data(experiment_id)
    if not doc:
        return None
    result = doc.get("result", {})
    return {
        "psnr": result.get("psnr", {}).get("raw", {}),
        "ssim": result.get("ssim", {}).get("raw", {}),
    }

def get_user_result_summaries(user_id):
    raw_results = results_store.get_all_results_by_user(user_id)
    
    raw_metadata = get_all_user_experiment_metadata(user_id)

    return _get_result_summaries(raw_results, raw_metadata)

def get_all_result_summaries():
    raw_results = results_store.get_all_results()
    
    raw_metadata = get_all_user_experiment_metadata(user_id=None, all_users=True)

    logger.info("Raw experiment metadata: %s", raw_metadata)

    return _get_result_summaries(raw_results, raw_metadata)

def _get_result_summaries(raw_results, raw_metadata):
    metadata_by_id = {
          str(metadata.get("id")): metadata
          for metadata in (raw_metadata or [])
      }

    cleaned_results = []

    for raw_result in raw_results:
        cleaned = clean_result(raw_result, metadata_by_id.get(
            str(raw_result.get("project", {}).get("experiment_id"))
        ))
        cleaned_results.append(cleaned)

    return cleaned_results
