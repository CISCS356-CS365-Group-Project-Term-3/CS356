import os


class Settings:
    experiment_queue:str = os.getenv('QUEUE_NAME', 'experiment_queue')