from .config import Settings
import json


class ConfigStore:

    _STATIC_CONFIG = {
        "encoder_type": {"000": "standard", "001": "scalable"},
        "loss": "PERCENT_TENTHS",
        "delay": "INTEGER",
        "jitter": "INTEGER"
    }

    def __init__(self, db_connection=None):
        with open(Settings.config_map_path, 'r') as f:
            self.config = json.loads(f.read())
    
    def get_config(self):
        return self.config
