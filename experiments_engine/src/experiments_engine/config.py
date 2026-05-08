import os


class Settings:
    experiment_queue:str = os.getenv('QUEUE_NAME', 'experiment_queue')
    queue_container:str = os.getenv('QUEUE_CONTAINER', 'queue')