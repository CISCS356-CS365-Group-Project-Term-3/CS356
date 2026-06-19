import json

import logging
import os
import subprocess
import re
import tempfile

from .metric import Ssim, Psnr
from .sequence_decoder import SequenceDecoder
from .config import Settings
from .coder import Decoder, Encoder
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
 
    def call_encoder(self, decoded_sequence, timeout=None):
        command = Encoder.build_command(decoded_sequence)
        logger.info(f'encoder command: {command}')
        result = Encoder.run(command, timeout=timeout)

        return self.transcoder_result(result, 'encoding')
    
    def call_decoder(self, decoded_sequence, timeout=None):
        command = Decoder.build_command(decoded_sequence)
        result = Decoder.run(command, timeout=timeout)

        return self.transcoder_result(result, 'decoding')
    
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
                temp_path
            )

            decoder_payload = (
                decoded.get("codec"),
                temp_path,
                output_path
            )

            logger.info(f"sequence starting for {experiment_id}")

            encoding_result = self.call_encoder(encoder_payload)
            logger.debug(encoding_result)

            logger.info("encoding complete")

            ## run network simulation here

            logger.info("simulation complete")

            decoding_result = self.call_decoder(decoder_payload)
            logger.debug(decoding_result)

            logger.info("decoding complete")

            metrics = self._calculate_metrics(input_path, output_path)

            logger.info("metrics complete")
            
            logger.info(
                f"Sequence '{sequence}' completed successfully."
            )

            result = metrics

            return (True, result)

        except Exception as e:
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
 
    def _parse_psnr(self, ffmpeg_output):
        # After "average" is where the result is in the output
        target = "average:"

        if target in ffmpeg_output:
            start_idx = ffmpeg_output.find(target) + len(target)
            value_str = ffmpeg_output[start_idx:].split()[0]
            # Handle the edge case if a perfect match returns 'inf'
            if value_str == "inf":
                return float("inf")
            return float(value_str)
        return None

    def _parse_ssim(self, ffmpeg_output):
        # After "All:" is where the result is in the output
        target = "All:"
        
        if target in ffmpeg_output:
            # Split the remaining text by spaces and grab the number
            start_idx = ffmpeg_output.find(target) + len(target)
            value_str = ffmpeg_output[start_idx:].split()[0]
            # Clean up trailing characters like '(inf)' if present
            if "(" in value_str:
                value_str = value_str.split("(")[0]
                
            return float(value_str)
        
        return None
 
    def send_result(self, experiment_id, result):

        self.output_store.store_experiment_result(result)
        
        logger.info(
            f"Results sent to output store for experiment "
            f"{experiment_id}: {self.status}"
        )
