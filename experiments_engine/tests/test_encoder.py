import pytest
import os
from experiments_engine.encoder import Encoder

DIRECTORY_NAME = os.path.dirname(__file__)
TEST_RAW_VIDEO_PATH = os.path.join(DIRECTORY_NAME, 'test_data/akiyo_qcif.y4m')
TEST_ENCODED_VIDEO_PATH = os.path.join(DIRECTORY_NAME, 'test_data/akiyo_qcif.mp4')


def test_encode_h264(capfd):
    out = encode(capfd=capfd, encoder='libx264')

    assert 'Stream #0:0 -> #0:0 (rawvideo (native) -> h264 (libx264))' in out


def encode(capfd, encoder: str):
    e = Encoder()

    remove_output(TEST_ENCODED_VIDEO_PATH)
    command: list[str] = e.build_command((encoder,TEST_RAW_VIDEO_PATH,TEST_ENCODED_VIDEO_PATH), '')
    e.run(command=command)

    out, err = capfd.readouterr()
    return err

    

def remove_output(path):
    if os.path.exists(path):
        os.remove(path)
