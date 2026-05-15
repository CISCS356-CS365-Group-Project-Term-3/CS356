import os


# this class creates the settings object used in worker
# settings are read from environment variables e.g. the "QUEUE_NAME" envirnoment variable
# if the environment variable isn't set, a default value is given
class Settings:
    experiment_queue:str = os.getenv('QUEUE_NAME', 'experiment_queue')
    queue_container:str = os.getenv('QUEUE_CONTAINER', 'queue')