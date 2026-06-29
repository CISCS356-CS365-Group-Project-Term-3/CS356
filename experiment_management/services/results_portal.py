from storage import results_store

def clean_result(doc):
    project = doc.get("project", {})
    result = doc.get("result", {})

    psnr_average = result.get("psnr", {}).get("average", {})
    ssim_average = result.get("ssim", {}).get("average", {})

    cleaned_doc = {
    "experimentId": project.get("experiment_id"),
    "groupId": project.get("group_id"),
    "userId": project.get("user_id"),
    "createdAt": project.get("created_at"),
    "sequence": doc.get("sequence"),
    "success": doc.get("success"),
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