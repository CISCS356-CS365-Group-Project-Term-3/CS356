from .config import Settings
import json


class ConfigStore:
    def __init__(self, db_connection=None):
        with open(Settings.config_map_path, 'r') as f:
            self.config = json.loads(f.read())
    
    def get_config(self):
        return self.config
