from .encoding_result import EncodingResult
from .coder import Coder

# builds and runs ffmpeg commands.


class Encoder(Coder):

    format_map: dict = {
        'h261': 'h261',
        'h263': 'h263',
        'h264': 'h264',
        'h265': 'hevc'
    }

    codec_map: dict = {
        'h261': 'h261',
        'h263': 'h263',
        'h264': 'libx264',
        'h265': 'libx265'
    }

    @classmethod
    def build_command(cls, sequence) -> list[str]:
        # builds ffmeg command from decoded sequence/config

        (encoder, input_file, output_file) = cls._get_encoder(sequence=sequence)

        codec: str = cls.format_map[encoder]
        format: str = cls.format_map[encoder]

        command = ['ffmpeg', 
                   # select input file
                   '-i', 
                   input_file, 
                   # select video stream to apply encoder (simple raw video so it is the only stream)
                   '-map', 
                   '0:v', 
                   # select encoder
                   '-c', 
                   codec, 
                   # select output format
                   '-f',
                   format,
                   output_file]

        return command
    
    def check_output(self, return_code: int, stderr: str) -> bool:
        return return_code == 0