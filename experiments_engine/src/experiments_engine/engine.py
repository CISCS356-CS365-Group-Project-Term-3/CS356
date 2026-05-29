import logging
import os
import subprocess
import tempfile
import re
 
from .encoding_result import EncodingResult
 
# Main orchestration class
 
logger = logging.getLogger(__name__)
 
# Valid codecs
VALID_CODEC_PAIRS = {
    "AVC": "standard",
    "HEVC": "standard",
    "FVC": "standard",
    #"SVC": "scalable",
    #"SHVC": "scalable",
}
 
 
class Engine:
 
    def __init__(
        self,
        store,
        encoder,
        output_store,
        decoder
    ):
  
        self.store = store
        self.encoder = encoder
        self.output_store = output_store
        self.decoder = decoder
 
    def process(self, experiment_id):
        self.status = "PENDING"
 
        try:
            experiment = self.fetch_experiment(experiment_id)
            config = self.store.get_config()
 
            if not self.validate_request(experiment, config):
                self.status = "FAILED"
                self.send_results(experiment_id, [EncodingResult(
                    status="FAILED",
                    error="Validation failed"
                )])
                return None
 
            self.status = "RUNNING"
 
            sequences = experiment.get("sequences", [])
            results = self.run_sequences(sequences, config, experiment_id)
 
            all_failed = all(r.status == "FAILED" for r in results)
            all_completed = all(r.status == "COMPLETED" for r in results)
 
            if all_failed:
                self.status = "FAILED"
            elif all_completed:
                self.status = "COMPLETED"
            else:
                self.status = "PARTIAL"
 
            self.send_results(experiment_id, results)
            return results
 
        except Exception as e:
            # prevents encoder crashes killing worker
            logger.critical(
                f"Unhandled error processing experiment {experiment_id}: {e}"
            )
            self.status = "FAILED"
            self.send_results(experiment_id, [EncodingResult(
                status="FAILED",
                error=f"Unhandled error: {str(e)}"
            )])
            return None
 
    def fetch_experiment(self, experiment_id):
        experiment = self.store.get_experiment(experiment_id)
 
        if experiment is None:
            logger.error(f"Experiment {experiment_id} not found in store.")
 
        return experiment
 
    def generate_script(self, sequences, config):
        commands = []
 
        for sequence in sequences:
            if sequence.get("pre_encoded", False):
                continue
 
            code = sequence["code"]
            decoded_layers = self.decoder.decode(code, config)
 
            # handle single and multi-layer safely
            if isinstance(decoded_layers, dict):
                decoded_layers = [decoded_layers]
 
            for layer in decoded_layers:
                command = self.encoder.build_command(layer, config)
                commands.append(" ".join(command))
 
        # create a bash script
        script_lines = ["#!/bin/bash", ""]
        script_lines.append("# Auto-generated encoding script")
        script_lines.append(f"# Sequences: {len(commands)}")
        script_lines.append("")
 
        for i, cmd in enumerate(commands):
            script_lines.append(f"# Sequence {i}")
            script_lines.append(cmd)
            script_lines.append("")
 
        return "\n".join(script_lines)
  
    def validate_request(self, experiment, config):
        if experiment is None:
            logger.error("Validation failed: experiment is None.")
            return False
 
        if config is None:
            logger.error("Validation failed: config is None.")
            return False
 
        sequences = experiment.get("sequences", [])
        if len(sequences) == 0:
            logger.error("Validation failed: no sequences in experiment.")
            return False
 
        project = experiment.get("project", {})
        codec = project.get("codec")
        encoder_type = project.get("encoder_type")
 
        # Validate codec/encoder_type pairing
        if codec and encoder_type:
            expected_type = VALID_CODEC_PAIRS.get(codec)
            if expected_type and expected_type != encoder_type:
                logger.error(
                    f"Validation failed: codec '{codec}' requires "
                    f"encoder_type '{expected_type}', got '{encoder_type}'."
                )
                return False
 
        if encoder_type == "scalable" and "scalability" not in project:
            logger.error(
                "Validation failed: scalable encoder requires 'scalability' field."
            )
            return False
 
        for seq in sequences:
            is_pre_encoded = seq.get("pre_encoded", False)
 
            if is_pre_encoded:
                if "pre_encoded_id" not in seq:
                    logger.error(
                        "Validation failed: pre_encoded sequence missing pre_encoded_id."
                    )
                    return False
            else:
                if "code" not in seq or not seq["code"]:
                    logger.error("Validation failed: sequence missing code.")
                    return False
 
                code = seq["code"]
                code_segments = code.split("_")
                layers = len(code_segments)
 
                for segment in code_segments:
                    if len(segment) != 30:
                        logger.error(
                            f"Validation failed: code segment '{segment}' "
                            f"is {len(segment)} chars, expected 30."
                        )
                        return False
 
            if encoder_type == "standard" and len(seq.get("code", "").split("_")) > 1:
                logger.error(
                    "Validation failed: standard encoder cannot have multi-layer sequences."
                )
                return False
 
        return True
 
    def call_encoder(self, decoded_sequence, config, timeout=None):
        command = self.encoder.build_command(decoded_sequence, config)
        result = self.encoder.run(command, timeout=timeout)
 
        success = self.encoder.check_output(
            result["return_code"],
            result["stderr"]
        )
 
        if not success:
            raise RuntimeError(
                f"Encoding failed with return code {result['return_code']}: "
                f"{result.get('stderr', 'unknown error')}"
            )
 
        return result
 
    def run_sequences(self, sequences, config, experiment_id):
        results = []
 
        for sequence in sequences:
            sequence_name = sequence.get("name", "unknown")
 
            if sequence.get("pre_encoded", False):
                logger.info(
                    f"Sequence '{sequence_name}' is pre-encoded. Skipping."
                )
                results.append(EncodingResult(
                    status="COMPLETED",
                    video_path=None,
                    log_path=None,
                    metrics={},
                    error=None,
                ))
                continue
 
            code = sequence["code"]
 
            try:
                code_segments = code.split("_")
                layers = len(code_segments)
                layer_results = []
 
                for layer_code in code_segments:
                    decoded = self.decoder.decode(layer_code, config)

                    encoder_payload = (
                        decoded.get("codec_library", "libx264"), 
                        decoded.get("raw_file"), 
                        "output.mp4"
                    )

                    result = self.call_encoder(encoder_payload, config)

                    result["output_path"] = "output.mp4" 
                    result["log_path"] = None
                    result["config_path"] = None
                    
                    layer_results.append(result)
 
                final_result = layer_results[-1]
                source_path = decoded.get("raw_file")

                encoding_result = self.build_result(
                    sequence, final_result, source_path
                )
                results.append(encoding_result)
 
                self.output_store.save_log(
                    experiment_id,
                    sequence_name,
                    f"COMPLETED: {layers} layer(s) encoded successfully."
                )
                logger.info(
                    f"Sequence '{sequence_name}' completed successfully."
                )
 
            except Exception as e:
                logger.error(
                    f"Sequence '{sequence_name}' failed: {str(e)}. "
                    f"Skipping to next."
                )
 
                encoding_result = EncodingResult(
                    status="FAILED",
                    video_path=None,
                    log_path=None,
                    metrics={},
                    error=str(e),
                )
                results.append(encoding_result)
 
                self.output_store.save_log(
                    experiment_id,
                    sequence_name,
                    f"FAILED: {str(e)}"
                )
                continue
 
        return results
 
    def build_result(self, sequence, encoder_output, source_path):
        sequence_name = sequence.get("name", "unknown")
        encoded_path = encoder_output.get("output_path")
        log_path = encoder_output.get("log_path")
        config_path = encoder_output.get("config_path")
 
        metrics = {}
 
        if encoded_path and source_path:
            # decode to raw pixels to calculate metrics
            decoded_path = self.call_decoder(encoded_path, sequence, encoder_output)
            metrics = self._calculate_metrics(source_path, decoded_path)
 
        result = EncodingResult(
            status="COMPLETED",
            video_path=encoded_path,
            log_path=log_path,
            metrics=metrics,
            error=None,
        )
 
        return result
 
    # Call decoder for encoded bitstream/video
    def call_decoder(self, encoded_path, sequence=None, encoder_output=None, timeout=120):
        if not self.decoder:
            return encoded_path
 
        decode_video_method = getattr(self.decoder, "decode_video", None)
        if callable(decode_video_method):
            decoded_output = decode_video_method(
                encoded_path,
                sequence=sequence,
                encoder_output=encoder_output,
                timeout=timeout,
            )
 
            if isinstance(decoded_output, dict):
                decoded_path = decoded_output.get("output_path")
                if decoded_path:
                    return decoded_path
            elif isinstance(decoded_output, str):
                return decoded_output
 
            raise RuntimeError("Decoder did not return a usable decoded output path.")
 
        return encoded_path
 
    def _calculate_metrics(self, reference_path, decoded_path):
        metrics = {}
 
        # store logs locally to prevent memory leaks in ffmpeg
        psnr_fd, psnr_stats_path = tempfile.mkstemp(prefix="psnr_", suffix=".log")
        ssim_fd, ssim_stats_path = tempfile.mkstemp(prefix="ssim_", suffix=".log")
        os.close(psnr_fd)
        os.close(ssim_fd)
 
        # Calculate PSNR 
        psnr_cmd = [
            "ffmpeg", "-i", decoded_path, "-i", reference_path,
            "-lavfi", f"psnr=stats_file={psnr_stats_path}",
            "-f", "null", "-"
        ]
 
        try:
            psnr_result = subprocess.run(
                psnr_cmd, capture_output=True, text=True, timeout=120
            )
            if psnr_result.returncode == 0:
                combined_output = (psnr_result.stdout or "") + (psnr_result.stderr or "")
                psnr_value = self._parse_psnr(combined_output)
                if psnr_value is not None:
                    metrics["psnr"] = psnr_value
            else:
                logger.warning(
                    f"PSNR command failed with code {psnr_result.returncode}: {psnr_result.stderr}"
                )
        except (subprocess.TimeoutExpired, OSError) as e:
            logger.warning(f"PSNR calculation failed: {e}")
 
        # Calculate SSIM
        ssim_cmd = [
            "ffmpeg", "-i", decoded_path, "-i", reference_path,
            "-lavfi", f"ssim=stats_file={ssim_stats_path}",
            "-f", "null", "-"
        ]
 
        try:
            ssim_result = subprocess.run(
                ssim_cmd, capture_output=True, text=True, timeout=120
            )
            if ssim_result.returncode == 0:
                combined_output = (ssim_result.stdout or "") + (ssim_result.stderr or "")
                ssim_value = self._parse_ssim(combined_output)
                if ssim_value is not None:
                    metrics["ssim"] = ssim_value
            else:
                logger.warning(
                    f"SSIM command failed with code {ssim_result.returncode}: {ssim_result.stderr}"
                )
        except (subprocess.TimeoutExpired, OSError) as e:
            logger.warning(f"SSIM calculation failed: {e}")
        finally:
            for stats_path in (psnr_stats_path, ssim_stats_path):
                try:
                    if os.path.exists(stats_path):
                        os.remove(stats_path)
                except OSError:
                    logger.warning(f"Failed to remove temporary stats file: {stats_path}")
 
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
 
    def send_results(self, experiment_id, results):
        if isinstance(results, EncodingResult):
            results = [results]
 
        for r in results:
            if r.status == "COMPLETED":
                if r.video_path:
                    self.output_store.save_video(r.video_path)
 
                if r.metrics:
                    self.output_store.save_metrics(
                        experiment_id, r.metrics
                    )
 
                if r.config_path:
                    self.output_store.save_configs(
                        experiment_id, {"config_path": r.config_path}
                    )
 
        self.output_store.save_status(experiment_id, {
            "status": self.status,
            "results": [vars(r) for r in results],
        })
 
        logger.info(
            f"Results sent to output store for experiment "
            f"{experiment_id}: {self.status}"
        )
 
    def get_status(self):
        return self.status