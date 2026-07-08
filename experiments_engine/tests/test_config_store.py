import pytest
from unittest.mock import patch, Mock
from experiments_engine.config_store import ConfigStore
from experiments_engine.output_store import OutputStore


#@pytest.fixture
def config_store():
    cs = ConfigStore()
    #cs._db.config.delete_one({"_id": "system"})
    yield cs
    #cs._db.config.delete_one({"_id": "system"})

#@pytest.fixture
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

def _test_get_config_raises_when_unset(config_store):
    assert config_store.get_config() is None
    
def _test_get_config_includes_static_fields(mock_api):
    cs = ConfigStore()
    config = cs.get_config()
    assert config["loss"] == "PERCENT_TENTHS"
    assert config["delay"] == "INTEGER"
    assert config["jitter"] == "INTEGER"
    assert config["encoder_type"] == {"000": "standard", "001": "scalable"}


def _test_save_and_get_config(config_store):
    config_store.save_config({"version": "1.0", "default_codec": "HEVC"})
    loaded = config_store.get_config()

    assert loaded is not None
    assert loaded["version"] == "1.0"
    assert loaded["default_codec"] == "HEVC"



MOCK_MAPPINGS = {
    "raw_file": {"001": "blue_sky_1080p25.y4m", "002": "bus_cif.y4m"},
    "codec": {"001": "h264", "002": "h265"}
}


@pytest.fixture
def mock_api():
    mock_response = Mock()
    mock_response.json.return_value = MOCK_MAPPINGS
    mock_response.raise_for_status.return_value = None
    with patch("experiments_engine.config_store.requests.get", return_value=mock_response) as mock_get:
        yield mock_get


def test_get_config_returns_api_mappings(mock_api):
    cs = ConfigStore()
    config = cs.get_config()
    assert config["raw_file"] == MOCK_MAPPINGS["raw_file"]
    assert config["codec"] == MOCK_MAPPINGS["codec"]


# ---- ConfigStore ----

def _test_get_config_raises_when_unset(config_store):
    assert config_store.get_config() is None
    
def _test_get_config_includes_static_fields(mock_api):
    cs = ConfigStore()
    config = cs.get_config()
    assert config["loss"] == "PERCENT_TENTHS"
    assert config["delay"] == "INTEGER"
    assert config["jitter"] == "INTEGER"
    assert config["encoder_type"] == {"000": "standard", "001": "scalable"}


def test_calls_correct_endpoint(mock_api):
    ConfigStore()
    called_url = mock_api.call_args[0][0]
    assert called_url.endswith("/rest/mappings")


def test_raises_on_api_error():
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("API unavailable")
    with patch("experiments_engine.config_store.requests.get", return_value=mock_response):
        with pytest.raises(Exception):
            ConfigStore()
