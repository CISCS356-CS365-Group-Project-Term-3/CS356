import pytest
import json
import os

from experiments_engine.metric import Ssim, Psnr

DIRECTORY_NAME = os.path.dirname(__file__)
TEST_RAW_VIDEO_PATH: str = os.path.join(DIRECTORY_NAME, 'test_data/akiyo_qcif.y4m')
TEST_DECODED_VIDEO_PATH: str = os.path.join(DIRECTORY_NAME, 'test_data/decoded_akiyo_qcif')

def test_ssim():
    ssim = Ssim()
    results = ssim.calculate_metric(reference_path=TEST_RAW_VIDEO_PATH, experiment_path=TEST_DECODED_VIDEO_PATH)
    assert(results is not None)
    print(json.dumps(results))

def test_psnr():
    psnr = Psnr()
    results = psnr.calculate_metric(reference_path=TEST_RAW_VIDEO_PATH, experiment_path=TEST_DECODED_VIDEO_PATH)
    assert(results is not None)
    print(json.dumps(results))

test_psnr()