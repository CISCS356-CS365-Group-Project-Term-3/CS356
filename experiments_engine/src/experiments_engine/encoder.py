import subprocess

# builds and runs ffmpeg commands.


class Encoder:

    def build_command(self, sequence, config) -> list[str]:
        # builds ffmeg command from decoded sequence/config

        (encoder, input_file, output_file) = self._get_encoder(sequence=sequence)

        command = ['ffmpeg', '-i', input_file, '-map', '0:v', '-c', encoder, output_file]

        return command

    def run(self, command):

        # Runs the ffmpeg command

        subprocess.run(command)

        pass

    def check_output(self, return_code, stderr):

        # Checks encoding output and determines success/failure

        pass

    @classmethod
    def _get_encoder(cls, sequence) -> tuple[str, str, str]:
        # hardcoded method until config is available
        return sequence