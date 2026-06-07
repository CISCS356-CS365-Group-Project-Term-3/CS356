import subprocess

from abc import ABC, abstractmethod

class Coder(ABC):

    @classmethod
    @abstractmethod
    def build_command(cls, sequence) -> list[str]:
        pass

    @staticmethod
    def run(command) -> dict:
        process = subprocess.run(command, capture_output=True, text=True)

        return {
            "return_code": process.returncode,
            "stderr": process.stderr,
            "stdout": process.stdout
        }
    
    @staticmethod
    def _get_encoder(sequence) -> tuple[str, str, str]:
        # hardcoded method until config is available
        return sequence
