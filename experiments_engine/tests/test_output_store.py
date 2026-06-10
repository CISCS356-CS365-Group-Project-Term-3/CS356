# test the OutputStore class, responsible for saving experiment outputs, logs, and metrics.

import pytest
import os 
from experiments_engine.output_store import OutputStore

@pytest.fixture
def output_store():
    class _DummyDB:
        pass
    return OutputStore(store_connection=_DummyDB())

def test_save_file_copies_to_destination(output_store, tmp_path):
    # tests save_file correctly copies a file to the specified destination
    src = tmp_path / "source.txt"
    src.write_text("hello")
    dest = tmp_path / "destination" / "copied.txt"
    result = output_store.save_file(str(src), str(dest))
    
    assert os.path.exists(dest)
    assert dest.read_text() == "hello"

def test_save_file_creates_missing_directories(output_store, tmp_path):
    # tests save_file creates any missing directories in destination path
    src = tmp_path / "source.txt"
    src.write_text("hello")
    dest = tmp_path / "missing" / "dirs" / "copied.txt"
    result = output_store.save_file(str(src), str(dest))

    assert os.path.exists(dest)

def test_save_file_preserves_content(output_store, tmp_path):
    # tests save_file correctly copies the file content without modification
    src = tmp_path / "source.txt"
    src.write_bytes(b"\x00\x01\x02\x03")
    dest = tmp_path / "copy.bin"
    output_store.save_file(str(src), str(dest))

    assert dest.read_bytes() == b"\x00\x01\x02\x03"

def test_save_video_writes_to_videos_directory(output_store, tmp_path, monkeypatch):
    # tests save_video saves the video to the correct location under the output root
    monkeypatch.setenv("OUTPUT_ROOT", str(tmp_path))
    
    video = tmp_path / "video.mp4"
    video.write_bytes(b"video content")
    
    result = output_store.save_video(str(video))
    
    assert os.path.exists(result)
    assert str(tmp_path / "videos" / "video.mp4") == result
    assert (tmp_path / "videos" / "video.mp4").read_bytes() == b"video content"

def test_save_video_uses_default_output_root(output_store, tmp_path, monkeypatch):
    # tests to ensure that the save_video method uses the default output root when OUTPUT_ROOT is not set
    monkeypatch.delenv("OUTPUT_ROOT", raising=False)  
    monkeypatch.chdir(tmp_path)  

    video = tmp_path / "video.mp4"
    video.write_bytes(b"video content")

    result = output_store.save_video(str(video))

    assert "videos" in result
    assert "video.mp4" in result
    assert os.path.exists(result)

def test_organise_output_directory_creates_subdirectories(output_store, tmp_path, monkeypatch):
    # tests that organise_output_directory creates the expected subdirectories for an experiment
    monkeypatch.setenv("OUTPUT_ROOT", str(tmp_path))

    result = output_store.organise_output_directory(None)
    
    assert result == str(tmp_path)
    for subdir in ("videos", "logs", "metrics", "configs"):
        assert (tmp_path / subdir).exists()

def test_organise_output_directory_with_experiment_id(output_store, tmp_path, monkeypatch):
    # tests that organise_output_directory creates a subdirectory for the experiment_id and the expected subdirectories within it
    monkeypatch.setenv("OUTPUT_ROOT", str(tmp_path))

    experiment_id = "test_exp_001"
    result = output_store.organise_output_directory(experiment_id)

    assert result == str(tmp_path / experiment_id)
    for subdir in ("videos", "logs", "metrics", "configs"):
        assert (tmp_path / experiment_id / subdir).exists()

