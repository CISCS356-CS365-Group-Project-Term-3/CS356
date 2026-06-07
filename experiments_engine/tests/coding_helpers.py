import os
from experiments_engine.encoder import Encoder

DIRECTORY_NAME = os.path.dirname(__file__)
TEST_ENCODED_VIDEO_PATH: str = os.path.join(DIRECTORY_NAME, 'test_data/encoded_akiyo_qcif')
TEST_RAW_VIDEO_PATH: str = os.path.join(DIRECTORY_NAME, 'test_data/akiyo_qcif.y4m')


def encode(codec: str):
    e = Encoder()

    remove_output(TEST_ENCODED_VIDEO_PATH)
    command: list[str] = e.build_command((codec,TEST_RAW_VIDEO_PATH,TEST_ENCODED_VIDEO_PATH))
    result: dict = e.run(command=command)

    assert result['return_code'] == 0
    return result['stderr']

    

def remove_output(path):
    if os.path.exists(path):
        os.remove(path)
