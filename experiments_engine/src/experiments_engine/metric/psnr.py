from .metric import Metric
from .metric_targets import MetricTargets


class Psnr(Metric):

    def __init__(self):

        self.metric_name = 'psnr'

        self.sterr_targets = MetricTargets(
            'average:',
            'y:',
            'u:',
            'v:'
        )

        self.file_targets = MetricTargets(
            'psnr_avg:',
            'psnr_y:',
            'psnr_u:',
            'psnr_v:',
        )

        self.file_prefix = 'mse_v:'
        self.file_delimiter = ' '
