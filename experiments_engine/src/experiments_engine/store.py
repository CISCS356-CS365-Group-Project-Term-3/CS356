# This class handles retrieving experiment data,configuration data, and lookup information.

#commented code are EXAMPLES

class Store:

    def __init__(self, db_connection):
        # Database connection
        self.db_connection = db_connection

    def get_experiment(self, experiment_id):
        # Retrieves experiment information
        # from the database

        pass

        # return {
        #     "experiment_id": experiment_id,
        #     "sequence_code": "ABC123"
        # }

    def get_config(self):
        # Retrieves system configuration
        # information


        pass

    def lookup_spatial(self, spatial_id):
        # Retrieves spatial settings
        # such as resolution
        # return {
        #     "width": 1920,
        #     "height": 1080
        # }

        pass

    def lookup_codec(self, codec_id):
        # Retrieves codec information
        # return {
        #     "codec": "h264"
        # }
        pass

    def lookup_source_file(self, file_id):
        # Retrieves source video path/file info
        # return {
        #     "path": "video.mp4"
        # }
        pass
