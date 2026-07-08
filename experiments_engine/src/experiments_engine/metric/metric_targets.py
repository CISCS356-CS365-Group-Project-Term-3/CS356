class MetricTargets:
    def __init__(self, average, y, u, v):
        self.average: str = average
        self.y: str = y
        self.u: str = u
        self.v: str = v

    def get_tuple(self):
        return (self.average, self.y, self.u, self.v)
