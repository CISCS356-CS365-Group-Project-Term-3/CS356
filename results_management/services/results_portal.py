from storage import results_store
import requests
import os
import json

def get_experiment_metadata(experiment_id):
    """ look up the postgres experiment row tied to a mongo result, if any """
    if experiment_id is None:
        return None

    try:

        EXPERIMENT_MANAGEMENT_ADDRESS = os.getenv("EXPERIMENT_MANAGEMENT_ADDRESS", "localhost:5000")
        url = f"{EXPERIMENT_MANAGEMENT_ADDRESS}/experiments/{experiment_id}"

        response = requests.get(url)
        if response.status_code != 200:
            print("experiment metadata request to experiment managament container failed", flush=True)
            return None
        return response.json()
    except Exception as e:
        print(f'experiment metadata lookup failed: {e}', flush=True)
        return None

def clean_result(doc):
    project = doc.get("project", {})
    result = doc.get("result", {})

    psnr_average = result.get("psnr", {}).get("average", {})
    ssim_average = result.get("ssim", {}).get("average", {})
    psnr_raw_combined = result.get("psnr", {}).get("raw", {}).get("combined", [])

    experiment = get_experiment_metadata(project.get("experiment_id"))
    encoder = (experiment.get("encoders") or [{}])[0] if experiment else {}
    sequence = (experiment.get("sequences") or [{}])[0] if experiment else {}

    cleaned_doc = {
    "experimentId": project.get("experiment_id"),
    "experimentName": experiment.get("name") if experiment else None,
    "batchId": experiment.get("batchId") if experiment else None,
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

def get_result_summaries():
    raw_results = results_store.get_all_results()

    cleaned_results = []

    for raw_doc in raw_results:
        cleaned = clean_result(raw_doc)
        cleaned_results.append(cleaned)

    return cleaned_results