# stores the result of an encoding job.  all outputs together in one object.


class EncodingResult:

    def __init__(
        self,
        status: int,
        video_path: str | None =None,
        log_path: str | None =None,
        metrics: str | None =None,
        error: str | None =None
    ):

        # Status of encoding job- may be PENDING, RUNNING, FAILED, COMPLETED
        self.status = status

        # path to encoded video file
        self.video_path = video_path

        # pth to log file
        self.log_path = log_path

        #  encoding metrics
        self.metrics = metrics

        #  error message if job fails etc. optional.
        self.error = error

    def to_dict(self):
        return vars(self)