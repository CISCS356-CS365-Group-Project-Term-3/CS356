import pytest
import os
from experiments_engine.decoder import Decoder
from coding_helpers import encode, remove_output, TEST_RAW_VIDEO_PATH, TEST_ENCODED_VIDEO_PATH

DIRECTORY_NAME = os.path.dirname(__file__)
TEST_DECODED_VIDEO_PATH: str = os.path.join(DIRECTORY_NAME, 'test_data/decoded_akiyo_qcif')


def test_decode_h261():
    out = decode(codec='h261')
    assert 'Stream #0:0 -> #0:0 (h261 (native) -> rawvideo (native))' in out

def test_decode_h263():
    out = decode(codec='h263')
    assert 'Stream #0:0 -> #0:0 (h263 (native) -> rawvideo (native))' in out

def test_decode_h264():
    out = decode(codec='h264')
    assert 'Stream #0:0 -> #0:0 (h264 (native) -> rawvideo (native))' in out

def test_decode_h265():
    out = decode(codec='h265')
    assert 'Stream #0:0 -> #0:0 (hevc (native) -> rawvideo (native))' in out


def decode(codec: str):

    #encode first to generate correct video for testing
    encode(codec=codec)

    e = Decoder()

    remove_output(TEST_DECODED_VIDEO_PATH)
    command: list[str] = e.build_command((codec,TEST_ENCODED_VIDEO_PATH,TEST_DECODED_VIDEO_PATH))
    result: dict = e.run(command=command)

    assert result['return_code'] == 0
    return result['stderr']

    
