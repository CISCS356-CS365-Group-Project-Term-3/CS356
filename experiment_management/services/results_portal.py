from storage import results_store
from storage.experiment_store import get_by_id as get_experiment_by_id

def get_experiment_metadata(experiment_id):
    """ look up the postgres experiment row tied to a mongo result, if any """
    if experiment_id is None:
        return None

    try:
        return get_experiment_by_id(int(experiment_id))
    except (TypeError, ValueError):
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

def get_result_summaries():
    raw_results = results_store.get_all_results()

    cleaned_results = []

    for raw_doc in raw_results:
        cleaned = clean_result(raw_doc)
        cleaned_results.append(cleaned)

    return cleaned_results