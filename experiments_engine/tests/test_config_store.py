#Tests for Store and OutputStore against MongoDB.
import pytest
from experiments_engine.config_store import ConfigStore
from experiments_engine.output_store import OutputStore


@pytest.fixture
def config_store():
    cs = ConfigStore()
    cs._db.config.delete_one({"_id": "system"})
    yield cs
    cs._db.config.delete_one({"_id": "system"})

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


# ---- ConfigStore ----

def test_get_config_raises_when_unset(config_store):
    assert config_store.get_config() is None


def test_save_and_get_config(config_store):
    config_store.save_config({"version": "1.0", "default_codec": "HEVC"})
    loaded = config_store.get_config()

    assert loaded is not None
    assert loaded["version"] == "1.0"
    assert loaded["default_codec"] == "HEVC"


def test_save_config_overwrites_existing(config_store):
    config_store.save_config({"version": "1.0"})
    config_store.save_config({"version": "2.0"})

    assert config_store.get_config()["version"] == "2.0"


def test_save_config_preserves_extra_fields(config_store):
    config_store.save_config({
        "version": "1.0",
        "default_codec": "HEVC",
        "max_layers": 4,
    })
    loaded = config_store.get_config()

    assert loaded["version"] == "1.0"
    assert loaded["default_codec"] == "HEVC"
    assert loaded["max_layers"] == 4

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

