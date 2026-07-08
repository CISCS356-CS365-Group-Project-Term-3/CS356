import subprocess
from ..config import Settings
import logging
logger = logging.getLogger(__name__)

def run_except(command: list[str], shell=False):
    result = subprocess.run(command, shell=shell, capture_output=True, text=True)
    if result.returncode != 0:
        message = f'Network command {command} exited with error code {result.returncode} \nstderr: {result.stderr} \nstdout: {result.stdout} '
        if Settings.environment == 'prod':
            logger.info(message)
        else:
            raise RuntimeError(message)
