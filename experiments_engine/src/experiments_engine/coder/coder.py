import subprocess

from abc import ABC, abstractmethod

class Transcoder(ABC):

    @classmethod
    @abstractmethod
    def build_command(cls, sequence) -> list[str]:
        pass

     # deprecated now encoder & decoder are executed together via network using run_transcode
    @staticmethod
    def run(command, timeout=None) -> dict:
        process = subprocess.run(command, capture_output=True, text=True)

        return {
            "return_code": process.returncode,
            "stderr": process.stderr,
            "stdout": process.stdout
        }
    
    @staticmethod
    # used to run a reciever command, followed by a sender command
    # the reciever command waits for the send command to complete
    # used as an ffmpeg command with UDP as input must be running and listening before the corresponding sender command tries to send encoded packets via UDP
    def run_piped(sender_command, reciever_command, timeout=None) -> dict:

        reciever = subprocess.Popen(reciever_command)
        sender = subprocess.Popen(sender_command)
        sender.wait()
        reciever.wait()

        return {
            "sender": {
                "return_code": sender.returncode,
                "stderr": sender.stderr,
                "stdout": sender.stdout
            },
            "reciever": {
                "return_code": reciever.returncode,
                "stderr": reciever.stderr,
                "stdout": reciever.stdout
            }
        }
    
    @staticmethod
    def _get_codec(sequence) -> tuple[str, str, str]:
        # hardcoded method until config is available
        return sequence
