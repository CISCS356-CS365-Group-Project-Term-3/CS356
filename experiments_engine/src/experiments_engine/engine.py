import logging
import os

from .network import setup_ip_to_ip, namespace_command_prefix, encoder_endpoint, decoder_endpoint, teardown_network
from .metric import Ssim, Psnr
from .sequence_decoder import SequenceDecoder
from .config import Settings
from .coder import Decoder, Encoder, Transcoder
from .output_store import OutputStore
from .config_store import ConfigStore

# Main orchestration class

logger = logging.getLogger(__name__)

class Engine:

    def __init__(
        self,
        config_store,
        output_store,
    ):

        self.config_store: ConfigStore = config_store
        self.output_store: OutputStore = output_store

    def process(self, experiment):
        (success, id, result) = self.run(experiment)
        self.send_result(id, result)
        return success

    def run(self, experiment):
        self.status = "PENDING"

        experiment_id = ''

        try:

            config = self.config_store.get_config()

            if not self.validate_request(experiment, config):
                raise RuntimeError("invalid request")

            experiment_id = experiment['project']['experiment_id']

            self.status = "RUNNING"

            sequence = experiment.get("sequence") # don't need default, already validated
            (success, result) = self.run_sequence(sequence, config, experiment_id)

            experiment['success'] = success
            experiment['result'] = result


            return (success, experiment_id, experiment)

        except Exception as e:
            # prevents encoder crashes killing worker
            experiment['success'] = False
            experiment['result'] = {}
            experiment['result']['reason'] = f'experiment run failed: {str(e)}'

            return (False, experiment_id, experiment)


    def validate_request(self, experiment, config):
        if experiment is None:
            logger.error("Validation failed: experiment is None.")
            return False

        if config is None:
            logger.error("Validation failed: config is None.")
            return False

        sequence = experiment.get("sequence", {})
        if sequence == {}:
            logger.error("Validation failed: no sequence in experiment.")
            return False

        project = experiment.get("project", {})
        if project == {}:
            logger.error("Validation failed: no project info")
            return False

        id = project.get("experiment_id", '')
        if id == '':
            logger.error("Validation failed: no experiment_id")
            return False

        return True

    # deprecated now encoder & decoder are executed together via network using run_transcode
    def call_encoder(self, decoded_sequence, timeout=None):
        command = Encoder.build_command(decoded_sequence)
        logger.info(f'encoder command: {command}')
        result = Encoder.run(command, timeout=timeout)

        return self.transcoder_result(result, 'encoding')

    # deprecated now encoder & decoder are executed together via network using run_transcode
    def call_decoder(self, decoded_sequence, timeout=None):
        command = Decoder.build_command(decoded_sequence)
        result = Decoder.run(command, timeout=timeout)

        return self.transcoder_result(result, 'decoding')

    def run_transcode(self, encoder_sequence, decoder_sequence, timeout=None):
        encoder_command = namespace_command_prefix(Settings.NetworkSimSettings.namespace_1) + Encoder.build_command(encoder_sequence)
        decoder_command = namespace_command_prefix(Settings.NetworkSimSettings.namespace_2) + Decoder.build_command(decoder_sequence)

        results = Transcoder.run_piped(encoder_command, decoder_command, timeout)

        self.transcoder_result(results['sender'], 'encoding')
        self.transcoder_result(results['reciever'], 'decoding')

    def transcoder_result(self, result, type):
        success = result['return_code'] == 0

        if not success:
            raise RuntimeError(
                f"{type} failed with return code {result['return_code']}: "
                f"{result.get('stderr', 'unknown error')}"
            )

        return result

    def run_sequence(self, sequence, config, experiment_id):

        result = {}

        try:
            #code_segments = code.split("_")
            #layers = len(code_segments)
            #layer_results = []

            #for layer_code in code_segments:
            decoded = SequenceDecoder.decode(sequence, config)

            input_path =  os.path.join(Settings.input_directory, str(decoded.get("raw_file")))
            temp_path = os.path.join(Settings.temp_directory, "temp")
            output_path = os.path.join(Settings.output_directory, sequence)

            encoder_payload = (
                decoded.get("codec"),
                input_path,
                encoder_endpoint()
            )

            decoder_payload = (
                decoded.get("codec"),
                decoder_endpoint(),
                output_path
            )

            logger.info(f"sequence starting for {experiment_id}")

            # setup simulated network
            setup_ip_to_ip(
                delay=decoded.get("delay"),
                jitter=decoded.get("jitter"),
                packet_loss=decoded.get("loss")
            )

            logger.info("network setup")

            # run encode & decode across simulated network
            encoding_result = self.run_transcode(encoder_payload, decoder_payload)
            logger.debug(encoding_result)

            logger.info("experiment run complete")

            logger.info("network namespaces removed")

            metrics = self._calculate_metrics(input_path, output_path)

            logger.info("metrics extract complete")

            logger.info(
                f"Sequence '{sequence}' completed successfully."
            )

            result = metrics

            teardown_network()

            return (True, result)

        except Exception as e:
            teardown_network()

            msg = f"Experiment {experiment_id} error, sequence '{sequence}' failed: {str(e)}. "
            logger.error(
                msg
            )

            result['reason'] = msg

            return (False, result)




    ### might as well make this a seperate class that pulls frame by frame data for metrics

    def _calculate_metrics(self, reference_path, decoded_path):
        metrics = {}

        metrics["psnr"] = Psnr().calculate_metric(reference_path=reference_path, experiment_path=decoded_path)

        metrics["ssim"] = Ssim().calculate_metric(reference_path=reference_path, experiment_path=decoded_path)

        return metrics

    def send_result(self, experiment_id, result):

        self.output_store.store_experiment_result(result)

        logger.info(
            f"Results sent to output store for experiment "
            f"{experiment_id}: {self.status}"
        )
