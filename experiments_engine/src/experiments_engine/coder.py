# parent class for encoding and decoding. func shared by both encoder and decoder.


class Coder:

    def build_command(self, sequence, config):

        # child classes must provide own implementation

        raise NotImplementedError(
            "child class must implement build_command()"
        )

    def run(self, command):

        # run ffmpeg command

        pass

    def check_output(self, return_code, stderr):

        # child classes overrides if wanting to.

        pass