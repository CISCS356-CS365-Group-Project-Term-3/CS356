#Tests for Store and OutputStore against MongoDB.
import pytest
from experiments_engine.store import Store
from experiments_engine.output_store import OutputStore


@pytest.fixture
def store():
    s = Store()
    for coll in ("experiments", "config", "spatial", "codecs", "source_files"):
        s._db[coll].delete_many({"_id": {"$regex": "^test_"}})
    yield s
    for coll in ("experiments", "config", "spatial", "codecs", "source_files"):
        s._db[coll].delete_many({"_id": {"$regex": "^test_"}})


@pytest.fixture
def output_store():
    os_ = OutputStore()
    for coll in ("results", "metrics", "configs"):
        os_._db[coll].delete_many({"_id": {"$regex": "^test_"}})
    os_._db.logs.delete_many({"experiment_id": {"$regex": "^test_"}})
    yield os_
    for coll in ("results", "metrics", "configs"):
        os_._db[coll].delete_many({"_id": {"$regex": "^test_"}})
    os_._db.logs.delete_many({"experiment_id": {"$regex": "^test_"}})


# ---- Store ----

def test_save_and_get_experiment(store):
    experiment = {
        "project": {"id": "test_proj_001", "codec": "HEVC"},
        "sequences": [{"order": 0, "qp": 28}],
    }
    store.save_experiment("test_exp_001", experiment)
    loaded = store.get_experiment("test_exp_001")

    assert loaded is not None
    assert loaded["project"]["codec"] == "HEVC"


def test_get_missing_experiment_returns_none(store):
    assert store.get_experiment("test_nonexistent") is None


def test_save_experiment_overwrites_existing(store):
    store.save_experiment("test_exp_002", {"codec": "AVC"})
    store.save_experiment("test_exp_002", {"codec": "HEVC"})
    assert store.get_experiment("test_exp_002")["codec"] == "HEVC"


def test_list_experiments_includes_saved(store):
    store.save_experiment("test_exp_003", {"codec": "AVC"})
    store.save_experiment("test_exp_004", {"codec": "HEVC"})
    ids = store.list_experiments()

    assert "test_exp_003" in ids
    assert "test_exp_004" in ids


# ---- OutputStore ----

def test_save_status_string(output_store):
    output_store.save_status("test_exp_005", "RUNNING")
    loaded = output_store.get_result("test_exp_005")

    assert loaded["status"] == "RUNNING"


def test_save_status_progresses(output_store):
    output_store.save_status("test_exp_006", "PENDING")
    output_store.save_status("test_exp_006", "RUNNING")
    output_store.save_status("test_exp_006", "COMPLETED")
    loaded = output_store.get_result("test_exp_006")

    assert loaded["status"] == "COMPLETED"


def test_save_status_dict_preserves_extra_fields(output_store):
    output_store.save_status("test_exp_007", {
        "status": "COMPLETED",
        "duration_seconds": 42,
    })
    loaded = output_store.get_result("test_exp_007")

    assert loaded["status"] == "COMPLETED"
    assert loaded["duration_seconds"] == 42


def test_save_and_get_metrics(output_store):
    output_store.save_metrics("test_exp_008", {
        "psnr": 38.5,
        "ssim": 0.92,
        "bitrate_kbps": 1234,
    })
    loaded = output_store.get_metrics("test_exp_008")

    assert loaded["psnr"] == 38.5
    assert loaded["bitrate_kbps"] == 1234


def test_save_log_creates_entry(output_store):
    output_store.save_log("test_exp_009", "Beauty", "encode started")
    output_store.save_log("test_exp_009", "Beauty", "encode finished")
    logs = output_store.get_logs("test_exp_009")

    assert len(logs) == 2
    assert all(log["experiment_id"] == "test_exp_009" for log in logs)

