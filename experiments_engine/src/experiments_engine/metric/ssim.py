from .metric import Metric
from .metric_targets import MetricTargets


class Ssim(Metric):

    def __init__(self):

        self.metric_name = 'ssim'

        self.sterr_targets = MetricTargets(
            'All:',
            'Y:',
            'U:',
            'V:'
        )

        self.file_targets = MetricTargets(
            'All:',
            'Y:',
            'U:',
            'V:'
        )

        self.file_prefix = 'n:'
        self.file_delimiter = ' '
