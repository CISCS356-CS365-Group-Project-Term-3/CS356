# Handles saving videos, logs,metrics, and experiment outputs.


class OutputStore:

    def __init__(self, store_connection):

        # storage connection
        self.store_connection = store_connection

    def save_file(self, file_path, destination):

        # saves encoded output file

        pass

    def save_log(self, experiment_id, sequence_name, log_data):

        # saves encoding logs

        pass

    def save_status(self, experiment_id, results):

        # saves experiment status

        pass


    def save_video(self, video_path):

        # saves encoded video

        pass

    def save_metrics(self, metrics):

        # saves encoding metrics/statistics

        pass

    def save_configs(self, config):

        # saves configuration information

        pass

    def organise_output_directory(self, experiment_id):

        # org experiment output folders

        pass