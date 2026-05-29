import pytest
from experiments_engine.engine import Engine
from experiments_engine.encoding_result import EncodingResult


class FakeStore:
    """Simulates database interactions for experiments and system configurations."""
    def __init__(self, experiment=None, config=None):
        self.experiment = experiment
        self.config = config

    def get_experiment(self, experiment_id):
        return self.experiment

    def get_config(self):
        return self.config


class FakeEncoder:
    """Mocks backend hardware encoding profiles and shell execution pipelines."""
    def __init__(self, should_fail=False):
        self.should_fail = should_fail
        self.commands_built = []
        self.commands_run = []

    def build_command(self, decoded_sequence, config):
        cmd = ["ffmpeg", "-i", "input.y4m", "-o", "output.mp4"]
        self.commands_built.append(cmd)
        return cmd

    def run(self, command, timeout=None):
        self.commands_run.append(command)
        if self.should_fail:
            return {
                "return_code": 1, 
                "stderr": "encoding error", 
                "output_path": None, 
                "log_path": None, 
                "config_path": None
            }
        return {
            "return_code": 0, 
            "stderr": "", 
            "output_path": "experiments_engine/tests/test_data/akiyo_qcif.y4m",
            "log_path": "/output/log.txt",
            "config_path": "/output/config.json"
        }

    def check_output(self, return_code, stderr):
        return return_code == 0


class FakeOutputStore:
    """Tracks state updates and target metrics without filesystem I/O overhead."""
    def __init__(self):
        self.statuses = []
        self.logs = []

    def save_status(self, experiment_id, status_dict):
        self.statuses.append({"experiment_id": experiment_id, "results": status_dict})

    def save_log(self, experiment_id, sequence_name, log_data):
        self.logs.append({
            "experiment_id": experiment_id, 
            "sequence_name": sequence_name, 
            "log_data": log_data
        })
        
    def save_video(self, path): pass
    def save_metrics(self, experiment_id, metrics): pass
    def save_configs(self, experiment_id, config_path): pass


class FakeDecoder:
    """Mocks code bitstream processing and structural parameters."""
    def __init__(self, should_fail=False):
        self.should_fail = should_fail

    def decode(self, code, config):
        if self.should_fail:
            raise ValueError(f"Invalid code: {code}")
        return {
            "encoder_type": "standard", 
            "codec": "AVC", 
            "spatial": "HD1080", 
            "raw_file": "experiments_engine/tests/test_data/akiyo_qcif.y4m"
        }

    def decode_video(self, encoded_path, **kwargs):
        return "experiments_engine/tests/test_data/akiyo_qcif.y4m"


@pytest.fixture
def valid_experiment():
    return {
        "_id": "exp_001",
        "project": {"codec": "AVC", "encoder_type": "standard"},
        "sequences": [
            {"name": "seq_1", "code": "0" * 30},
            {"name": "seq_2", "code": "1" * 30},
        ]
    }


@pytest.fixture
def valid_config():
    return {
        "encoder_type": {"000": "standard"},
        "codec": {"000": "AVC"},
    }


@pytest.fixture
def engine(valid_experiment, valid_config):
    store = FakeStore(experiment=valid_experiment, config=valid_config)
    encoder = FakeEncoder()
    output_store = FakeOutputStore()
    decoder = FakeDecoder()
    return Engine(store=store, encoder=encoder, output_store=output_store, decoder=decoder)


class TestValidation:
    def test_valid_experiment_passes(self, engine, valid_experiment, valid_config):
        assert engine.validate_request(valid_experiment, valid_config) is True

    def test_none_experiment_fails(self, engine, valid_config):
        assert engine.validate_request(None, valid_config) is False

    def test_missing_sequences_fails(self, engine, valid_config):
        assert engine.validate_request({}, valid_config) is False

    def test_empty_sequences_fails(self, engine, valid_config):
        assert engine.validate_request({"sequences": []}, valid_config) is False

    def test_sequence_missing_code_fails(self, engine, valid_config):
        experiment = {"sequences": [{"name": "test"}]}
        assert engine.validate_request(experiment, valid_config) is False

    def test_none_config_fails(self, engine, valid_experiment):
        assert engine.validate_request(valid_experiment, None) is False


class TestFetchExperiment:
    def test_fetches_from_store(self, engine, valid_experiment):
        result = engine.fetch_experiment("exp_001")
        assert result == valid_experiment

    def test_returns_none_if_not_found(self, valid_config):
        store = FakeStore(experiment=None, config=valid_config)
        eng = Engine(store=store, encoder=FakeEncoder(), output_store=FakeOutputStore(), decoder=FakeDecoder())
        assert eng.fetch_experiment("nonexistent") is None


class TestRunSequences:
    def test_runs_all_sequences(self, engine, valid_experiment, valid_config):
        sequences = valid_experiment["sequences"]
        results = engine.run_sequences(sequences, valid_config, "exp_001")
        assert len(results) == 2

    def test_successful_sequences_have_completed_status(self, engine, valid_experiment, valid_config):
        sequences = valid_experiment["sequences"]
        results = engine.run_sequences(sequences, valid_config, "exp_001")
        assert all(r.status == "COMPLETED" for r in results)

    def test_encoder_is_called_for_each_sequence(self, valid_experiment, valid_config):
        store = FakeStore(experiment=valid_experiment, config=valid_config)
        encoder = FakeEncoder()
        output_store = FakeOutputStore()
        eng = Engine(store=store, encoder=encoder, output_store=output_store, decoder=FakeDecoder())

        eng.run_sequences(valid_experiment["sequences"], valid_config, "exp_001")
        assert len(encoder.commands_run) == 2


class TestFailureSkipping:
    def test_continues_after_failed_sequence(self, valid_experiment, valid_config):
        store = FakeStore(experiment=valid_experiment, config=valid_config)
        encoder = FakeEncoder()
        output_store = FakeOutputStore()
        decoder = FakeDecoder(should_fail=True)
        eng = Engine(store=store, encoder=encoder, output_store=output_store, decoder=decoder)

        results = eng.run_sequences(valid_experiment["sequences"], valid_config, "exp_001")
        assert len(results) == 2
        assert all(r.status == "FAILED" for r in results)

    def test_failed_sequence_logs_error(self, valid_experiment, valid_config):
        store = FakeStore(experiment=valid_experiment, config=valid_config)
        encoder = FakeEncoder()
        output_store = FakeOutputStore()
        decoder = FakeDecoder(should_fail=True)
        eng = Engine(store=store, encoder=encoder, output_store=output_store, decoder=decoder)

        eng.run_sequences(valid_experiment["sequences"], valid_config, "exp_001")
        assert len(output_store.logs) == 2

    def test_encoder_failure_skips_to_next(self, valid_experiment, valid_config):
        store = FakeStore(experiment=valid_experiment, config=valid_config)
        encoder = FakeEncoder(should_fail=True)
        output_store = FakeOutputStore()
        decoder = FakeDecoder()
        eng = Engine(store=store, encoder=encoder, output_store=output_store, decoder=decoder)

        results = eng.run_sequences(valid_experiment["sequences"], valid_config, "exp_001")
        assert len(results) == 2
        assert all(r.status == "FAILED" for r in results)


class TestSendResults:
    def test_sends_completed_status(self, valid_config):
        store = FakeStore(experiment=None, config=valid_config)
        output_store = FakeOutputStore()
        eng = Engine(store=store, encoder=FakeEncoder(), output_store=output_store, decoder=FakeDecoder())
        
        eng.status = "COMPLETED"
        results = [
            EncodingResult(status="COMPLETED", sequence_name="seq1", video_path="/a.mp4", log_path="/a.log"),
            EncodingResult(status="COMPLETED", sequence_name="seq2", video_path="/b.mp4", log_path="/b.log"),
        ]
        eng.send_results("exp_001", results)

        last = output_store.statuses[-1]
        assert last["results"]["status"] == "COMPLETED"

    def test_sends_failed_status_when_all_fail(self, valid_config):
        store = FakeStore(experiment=None, config=valid_config)
        output_store = FakeOutputStore()
        eng = Engine(store=store, encoder=FakeEncoder(), output_store=output_store, decoder=FakeDecoder())

        eng.status = "FAILED"
        results = [
            EncodingResult(status="FAILED", sequence_name="seq1", video_path=None, log_path=None, error="err"),
        ]
        eng.send_results("exp_001", results)

        last = output_store.statuses[-1]
        assert last["results"]["status"] == "FAILED"

    def test_accepts_single_encoding_result(self, valid_config):
        store = FakeStore(experiment=None, config=valid_config)
        output_store = FakeOutputStore()
        eng = Engine(store=store, encoder=FakeEncoder(), output_store=output_store, decoder=FakeDecoder())

        eng.status = "FAILED"
        single_result = EncodingResult(status="FAILED", sequence_name="seq1", video_path=None, log_path=None, error="validation")
        eng.send_results("exp_001", single_result)

        last = output_store.statuses[-1]
        assert last["results"]["status"] == "FAILED"


class TestProcess:
    def test_successful_process(self, valid_experiment, valid_config):
        store = FakeStore(experiment=valid_experiment, config=valid_config)
        encoder = FakeEncoder()
        output_store = FakeOutputStore()
        decoder = FakeDecoder()
        eng = Engine(store=store, encoder=encoder, output_store=output_store, decoder=decoder)

        results = eng.process("exp_001")

        assert results is not None
        assert len(results) == 2
        assert all(r.status == "COMPLETED" for r in results)

    def test_failed_validation_returns_none(self, valid_config):
        store = FakeStore(experiment=None, config=valid_config)
        output_store = FakeOutputStore()
        eng = Engine(store=store, encoder=FakeEncoder(), output_store=output_store, decoder=FakeDecoder())

        result = eng.process("nonexistent")
        assert result is None

    def test_status_updates_are_saved(self, valid_experiment, valid_config):
        store = FakeStore(experiment=valid_experiment, config=valid_config)
        output_store = FakeOutputStore()
        eng = Engine(store=store, encoder=FakeEncoder(), output_store=output_store, decoder=FakeDecoder())

        eng.process("exp_001")

        saved_statuses = [s["results"]["status"] for s in output_store.statuses]
        assert "COMPLETED" in saved_statuses


class TestGenerateScript:
    def test_generates_bash_script(self, engine, valid_experiment, valid_config):
        script = engine.generate_script(valid_experiment["sequences"], valid_config)
        assert script.startswith("#!/bin/bash")

    def test_script_has_command_per_sequence(self, engine, valid_experiment, valid_config):
        script = engine.generate_script(valid_experiment["sequences"], valid_config)
        assert "# Sequence 0" in script
        assert "# Sequence 1" in script