import pytest
from coding_helpers import encode


def test_encode_h261():
    out = encode(codec='h261')
    assert 'Stream #0:0 -> #0:0 (rawvideo (native) -> h261 (native))' in out

def test_encode_h263():
    out = encode(codec='h263')
    assert 'Stream #0:0 -> #0:0 (rawvideo (native) -> h263 (native))' in out

def test_encode_h264():
    out = encode(codec='h264')
    assert 'Stream #0:0 -> #0:0 (rawvideo (native) -> h264 (libx264))' in out

def test_encode_h265():
    out = encode(codec='h265')
    assert 'Stream #0:0 -> #0:0 (rawvideo (native) -> hevc (libx265))' in out
