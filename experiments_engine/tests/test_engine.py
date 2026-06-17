import pytest

from experiments_engine.config import Settings
from experiments_engine.engine import Engine


VALID_SEQUENCE = "000000000000000000"


class FakeConfigStore:
    def __init__(self, config=None):
        self.config = config

    def get_config(self):
        return self.config


class FakeOutputStore:
    def __init__(self):
        self.results = []

    def store_experiment_result(self, result):
        self.results.append(result)


@pytest.fixture
def config():
    return {
        "raw_file": {"000": "input.y4m"},
        "codec": {"000": "h264"},
        "encoder_type": {"000": "standard"},
        "loss": "DECIMAL",
        "delay": "INTEGER",
        "jitter": "INTEGER",
    }


@pytest.fixture
def experiment():
    return {
        "project": {"experiment_id": "exp_001"},
        "sequence": VALID_SEQUENCE,
    }


@pytest.fixture
def engine(config):
    return Engine(FakeConfigStore(config), FakeOutputStore())


def test_validate_request_accepts_current_experiment_shape(
    engine, experiment, config
):
    assert engine.validate_request(experiment, config) is True


@pytest.mark.parametrize(
    "bad_experiment",
    [
        None,
        {},
        {"project": {"experiment_id": "exp_001"}},
        {"sequence": VALID_SEQUENCE},
        {"project": {"experiment_id": ""}, "sequence": VALID_SEQUENCE},
    ],
)
def test_validate_request_rejects_missing_required_fields(
    engine, bad_experiment, config
):
    assert engine.validate_request(bad_experiment, config) is False


def test_validate_request_rejects_missing_config(engine, experiment):
    assert engine.validate_request(experiment, None) is False


def test_run_adds_sequence_result(monkeypatch, config, experiment):
    engine = Engine(FakeConfigStore(config), FakeOutputStore())

    def run_sequence(sequence, run_config, experiment_id):
        assert sequence == VALID_SEQUENCE
        assert run_config == config
        assert experiment_id == "exp_001"
        return True, {"psnr": 31.5}

    monkeypatch.setattr(engine, "run_sequence", run_sequence)

    success, experiment_id, result = engine.run(experiment)

    assert success is True
    assert experiment_id == "exp_001"
    assert result["success"] is True
    assert result["result"] == {"psnr": 31.5}


def test_run_returns_failure_for_invalid_request(experiment):
    engine = Engine(FakeConfigStore(None), FakeOutputStore())

    success, experiment_id, result = engine.run(experiment)

    assert success is False
    assert experiment_id == ""
    assert result["success"] is False
    assert result["result"]["reason"] == "experiment run failed: invalid request"


def test_process_stores_result_and_returns_success(monkeypatch, experiment):
    output_store = FakeOutputStore()
    engine = Engine(FakeConfigStore({}), output_store)

    def run(experiment):
        engine.status = "RUNNING"
        return True, "exp_001", {"success": True, "result": {"psnr": 31.5}}

    monkeypatch.setattr(engine, "run", run)

    assert engine.process(experiment) is True
    assert output_store.results == [{"success": True, "result": {"psnr": 31.5}}]


def test_run_sequence_calls_transcoders_and_metrics(
    monkeypatch, tmp_path, config, engine
):
    input_dir = tmp_path / "input"
    temp_dir = tmp_path / "temp"
    output_dir = tmp_path / "output"
    calls = []

    monkeypatch.setattr(Settings, "input_directory", str(input_dir))
    monkeypatch.setattr(Settings, "temp_directory", str(temp_dir))
    monkeypatch.setattr(Settings, "output_directory", str(output_dir))

    def call_encoder(payload):
        calls.append(("encoder", payload))
        return {"return_code": 0}

    def call_decoder(payload):
        calls.append(("decoder", payload))
        return {"return_code": 0}

    def calculate_metrics(reference_path, decoded_path):
        assert reference_path == str(input_dir / "input.y4m")
        assert decoded_path == str(output_dir / VALID_SEQUENCE)
        return {"psnr": 31.5, "ssim": 0.98}

    monkeypatch.setattr(engine, "call_encoder", call_encoder)
    monkeypatch.setattr(engine, "call_decoder", call_decoder)
    monkeypatch.setattr(engine, "_calculate_metrics", calculate_metrics)

    success, result = engine.run_sequence(VALID_SEQUENCE, config, "exp_001")

    assert success is True
    assert result == {"psnr": 31.5, "ssim": 0.98}
    assert calls == [
        (
            "encoder",
            ("h264", str(input_dir / "input.y4m"), str(temp_dir / "temp")),
        ),
        (
            "decoder",
            ("h264", str(temp_dir / "temp"), str(output_dir / VALID_SEQUENCE)),
        ),
    ]


def test_run_sequence_returns_failure_reason(monkeypatch, config, engine):
    def call_encoder(payload):
        raise RuntimeError("encoding failed")

    monkeypatch.setattr(engine, "call_encoder", call_encoder)

    success, result = engine.run_sequence(VALID_SEQUENCE, config, "exp_001")

    assert success is False
    assert "Experiment exp_001 error" in result["reason"]
    assert "encoding failed" in result["reason"]


def test_transcoder_result_returns_success(engine):
    result = {"return_code": 0, "stderr": ""}

    assert engine.transcoder_result(result, "encoding") == result


def test_transcoder_result_raises_for_failure(engine):
    with pytest.raises(RuntimeError, match="encoding failed"):
        engine.transcoder_result(
            {"return_code": 1, "stderr": "bad input"},
            "encoding",
        )


def test_parse_metric_values(engine):
    assert engine._parse_psnr("average:37.25 min:30.0") == 37.25
    assert engine._parse_psnr("average:inf min:30.0") == float("inf")
    assert engine._parse_ssim("All:0.987654 (19.12)") == 0.987654
