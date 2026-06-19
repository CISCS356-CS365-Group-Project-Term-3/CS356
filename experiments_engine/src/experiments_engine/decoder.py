from .coder import Coder

class Decoder(Coder):

    @classmethod
    def build_command(cls, sequence) -> list[str]:
        (_, input_file, output_file) = cls._get_codec(sequence=sequence)

        command = ['ffmpeg', 
                   # select input file
                   '-i', 
                   input_file, 
                   # select video stream to apply encoder (simple raw video so it is the only stream)
                   '-map', 
                   '0:v', 
                   # select encoder
                   '-c', 
                   'rawvideo', 
                   # select output format
                   '-f',
                   'yuv4mpegpipe',
                   # overwrite if already exists
                   '-y',
                   output_file]

        return command
