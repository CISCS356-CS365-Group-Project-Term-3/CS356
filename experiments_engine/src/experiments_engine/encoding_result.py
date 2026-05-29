# stores the result of an encoding job.  all outputs together in one object.


class EncodingResult:

    def __init__(
        self,
        status,
        video_path=None,
        log_path=None,
        config_path=None,
        sequence_name=None,
        metrics=None,
        error=None
    ):
        # Status of encoding job- may be PENDING, RUNNING, FAILED, COMPLETED
        self.status = status
        # path to encoded video file
        self.video_path = video_path
        # path to log file
        self.log_path = log_path
        # path to config file (optional)
        self.config_path = config_path
        # name of the sequence (optional)
        self.sequence_name = sequence_name
        # encoding metrics
        self.metrics = metrics
        # error message if job fails etc. optional.
        self.error = error