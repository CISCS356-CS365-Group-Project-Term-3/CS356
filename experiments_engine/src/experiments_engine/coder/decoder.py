from .coder import Transcoder

class Decoder(Transcoder):

    @classmethod
    def build_command(cls, sequence) -> list[str]:
        (_, endpoint, output_file) = cls._get_codec(sequence=sequence)

        command = ['ffmpeg',
                   # keep decoding lossy streams instead of aborting
                   # skip corrupted packets and don't bail out on decode errors
                   '-fflags',
                   '+discardcorrupt',
                   '-err_detect',
                   'ignore_err',
                   # select input
                   '-i', 
                   endpoint, 
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
