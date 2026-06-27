# stores the result of a SINGLE network transmission- its status, output paths, logs, metrics and
# any errors returned from the simulation.


class NetworkResult:

    def __init__(
        self,
        status,
        transmitted_file_path,
        log_path,
        metrics,
        sequence_name,
        transmission_id,
        error=None
    ):

        # status of the network transmission
        self.status = status

        # path to transmitted output file
        self.transmitted_file_path = transmitted_file_path

        # path to any logs generated
        self.log_path = log_path

        # network metrics returned from the simulation
        self.metrics = metrics

        # sequence name being transmitted
        self.sequence_name = sequence_name

        self.transmission_id = transmission_id

        # error message if transmission fails
        self.error = error

    def invoke_network_simulation(self):

        # call group f's network simulation. Implementation will be added once
        # integration details/code received?

        pass

    def to_dict(self):

        # convert the object into dict for json serialisation and storage

        return {
            "status": self.status,
            "transmitted_file_path": self.transmitted_file_path,
            "log_path": self.log_path,
            "metrics": self.metrics,
            "error": self.error,
            "sequence_name": self.sequence_name,
            "transmission_id": self.transmission_id
        }