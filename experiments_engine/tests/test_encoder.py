import pytest
import os
from experiments_engine.encoder import Encoder
from experiments_engine.encoding_result import EncodingResult

DIRECTORY_NAME = os.path.dirname(__file__)
TEST_ENCODED_VIDEO_PATH: str = os.path.join(DIRECTORY_NAME, 'test_data/encoded_akiyo_qcif')
TEST_RAW_VIDEO_PATH: str = os.path.join(DIRECTORY_NAME, 'test_data/akiyo_qcif.y4m')


def test_encode_h261(capfd):
    out = encode(capfd=capfd, encoder='h261')
    assert 'Stream #0:0 -> #0:0 (rawvideo (native) -> h261 (native))' in out

def test_encode_h263(capfd):
    out = encode(capfd=capfd, encoder='h263')
    assert 'Stream #0:0 -> #0:0 (rawvideo (native) -> h263 (native))' in out

def test_encode_h264(capfd):
    out = encode(capfd=capfd, encoder='libx264')
    assert 'Stream #0:0 -> #0:0 (rawvideo (native) -> h264 (libx264))' in out

def test_encode_h265(capfd):
    out = encode(capfd=capfd, encoder='libx265')
    assert 'Stream #0:0 -> #0:0 (rawvideo (native) -> hevc (libx265))' in out


def encode(capfd, encoder: str):
    e = Encoder()

    remove_output(TEST_ENCODED_VIDEO_PATH)
    command: list[str] = e.build_command((encoder,TEST_RAW_VIDEO_PATH,TEST_ENCODED_VIDEO_PATH), '')
    result: EncodingResult = e.run(command=command)
    out, err = capfd.readouterr()

    assert result.to_dict()['status'] == 0
    return err

    

def remove_output(path):
    if os.path.exists(path):
        os.remove(path)
