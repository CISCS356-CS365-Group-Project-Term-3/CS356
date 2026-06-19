import tempfile
import logging
import subprocess 

import numpy as np

from abc import ABC, abstractmethod

from .metric_targets import MetricTargets

logger = logging.getLogger(__name__)

# I think this will break for PSNR values greater than 100 or lower than 10
class Metric(ABC):

    def __init__(self):
        self.sterr_targets: MetricTargets
        self.file_targets: MetricTargets
        self.metric_name: str

        self.file_prefix: str # used to slice the relevant part of each line in a stats file
        self.file_delimiter: str

    def calculate_metric(self, reference_path: str, experiment_path: str):
              
        with tempfile.NamedTemporaryFile(mode="w+b", delete=False) as ffmpeg_output:
            command = [
                "ffmpeg", 
                "-i", 
                experiment_path, 
                "-i", 
                reference_path,
                "-lavfi", f"{self.metric_name}=stats_file={ffmpeg_output.name}",
                "-f", "null", "-"
            ]
            
            try:
                
                # run the command
                result = subprocess.run(
                    command, capture_output=True, text=True, timeout=120
                )

                # get the average values from the stderr output easy
                average = {}    
                (average['combined'],average['y'], average['u'],average['v']) = self._parse_float_outputs(result.stderr, self.sterr_targets)


                #### Getting the raw values
                #### trying to make this as quick as possible

                # get the frame count so we know how big to make our arrays
                frame_count = int(self._parse_output(result.stderr, 'frame=  '))

                # init numpy arrays for each raw datatype we want
                r_a: dict[str, np.typing.NDArray[np.float32]] = {}
                (r_a['combined'], r_a['y'], r_a['u'], r_a['v']) = (np.empty(frame_count, dtype=np.float32) for _ in range(4))

                ## build a map of the indices of the values we want (faster than scanning every single line)
                # get first line
                first_line = str(ffmpeg_output.readline())
                # get rid of 'n:13' style index
                first_line = self._slice_relevant(first_line)
                # build index map
                index_map = (self._find_index(first_line, target) for target in self.file_targets.get_tuple())

                counter = 0

                values_indexes = list(zip(r_a.values(), index_map)) # zip values and indexes for looping

                ffmpeg_output.seek(0) # seek to start of file
                for line_bytes in ffmpeg_output: # each line in the temp file
                    line = str(line_bytes)
                    line = self._slice_relevant(line) # always discard initial 'n:13' style index or index map values get messed up
                    for v,i in values_indexes:
                        v[counter] = float(line[i[0]:i[1]]) 
                        val = float(line[i[0]:i[1]])

                    counter += 1

                # convert each numpy array to a list which dumps to JSON cleanly
                raw = {}
                for k in r_a:
                    raw[k] = r_a[k].tolist()
                


            except (subprocess.TimeoutExpired, OSError) as e:
                logger.warning(f"{self.metric_name} metric calculation failed: {e}")
                return None
            
            result = {}
            result['average'] = average
            result['raw'] = raw

            return result

    def _parse_float_outputs(self, output, targets: MetricTargets):
        for t in targets.get_tuple():
            yield float(self._parse_output(output, t))
        

    def _parse_output(self, ffmpeg_output, target):
      
        if target in ffmpeg_output:
            # Split the remaining text by spaces and grab the number
            start_idx = ffmpeg_output.find(target) + len(target)
            value_str = ffmpeg_output[start_idx:].split()[0]
            # Clean up trailing characters like '(inf)' if present
            if "(" in value_str:
                value_str = value_str.split("(")[0]
                
            return value_str
        
        return ""
    
    # find the string index of a value given the prefix
    def _find_index(self, string, prefix):
        start = string.find(prefix) + len(prefix)
        end = string[start:].find(self.file_delimiter) + start
        val = string.find(prefix)
        l = len(prefix)
        return (start, end)
    
    # create a slice of the relevant section of the line
    def _slice_relevant(self, line):
        start_target = line.find(self.file_prefix)
        start = line.find(self.file_delimiter, start_target) + 1
        return line[start:]
