from encoding_result import EncodingResult

# main orchestration class. coordinates the encoding workflow.


class Engine:

    def __init__(
        self,
        store,
        encoder,
        output_store,
        decoder
    ):

        # collab classes

        self.store = store
        self.encoder = encoder
        self.output_store = output_store
        self.decoder = decoder

    def process(self, experiment_id):

        self.update_status(
            experiment_id,
            "PENDING"
        )

        experiment = self.store.get_experiment(
            experiment_id
        )

        config = self.store.get_config()

        valid = self.validate(
            experiment,
            config
        )

        if not valid:

            self.update_status(
                experiment_id,
                "FAILED"
            )

            return None

        self.update_status(
            experiment_id,
            "RUNNING"
        )

        decoded_sequence = self.decoder.decode(
            experiment["sequence_code"],
            config
        )

        command = self.encoder.build_command(
            decoded_sequence,
            config
        )

        result = self.encoder.run(command)

        success = self.encoder.check_output(
            result["return_code"],
            result["stderr"]
        )

        if success:

            encoding_result = EncodingResult(
                status="COMPLETED",
                video_path=None,
                log_path=None
            )

            self.output_store.save_status(
                experiment_id,
                encoding_result.status
            )

            self.update_status(
                experiment_id,
                "COMPLETED"
            )

            return encoding_result

        self.update_status(
            experiment_id,
            "FAILED"
        )

        return EncodingResult(
            status="FAILED",
            video_path=None,
            log_path=None,
            error=result["stderr"]
        )

    def validate(self, experiment, config):

        # Validates experiment/config

        return True #not passing here as need to determine if its valid or not

    def run_sequences(self, sequences):

        # Runs multiple sequences

        pass

    def build_result(self, sequence, status, error):

        # Builds result object/dictionary

        pass

    def report_status(self, experiment_id, results):

        # Reports experiment status

        pass


    def update_status(self, experiment_id, status):

        # Updates current job status

        pass