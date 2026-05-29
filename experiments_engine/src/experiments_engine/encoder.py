import subprocess

from .encoding_result import EncodingResult

# builds and runs ffmpeg commands.


class Encoder:

    format_map: dict = {
        'h261': 'h261',
        'h263': 'h263',
        'libx264': 'h264',
        'libx265': 'hevc'
    }

    def build_command(self, sequence, config) -> list[str]:
        # builds ffmeg command from decoded sequence/config

        (encoder, input_file, output_file) = self._get_encoder(sequence=sequence)

        format: str = self.format_map[encoder]

        command = ['ffmpeg', 
                   # select input file
                   '-i', 
                   input_file, 
                   # select video stream to apply encoder (simple raw video so it is the only stream)
                   '-map', 
                   '0:v', 
                   # select encoder
                   '-c', 
                   encoder, 
                   # select output format
                   '-f',
                   format,

                   output_file]

        return command

    def run(self, command) -> dict:
        process = subprocess.run(command, capture_output=True, text=True)

        return {
            "return_code": process.returncode,
            "stderr": process.stderr,
            "stdout": process.stdout
        }

    def check_output(self, return_code: int, stderr: str) -> bool:
        return return_code == 0

    @classmethod
    def _get_encoder(cls, sequence) -> tuple[str, str, str]:
        # hardcoded method until config is available
        return sequence