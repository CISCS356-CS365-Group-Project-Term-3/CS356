from .config import Settings
import requests
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
            config_string = f.read()

            if config_string != 'DYNAMIC':
                self.config = json.loads(config_string)
                return

        response = requests.get(f"{Settings.infra_api_url}/rest/mappings")
        response.raise_for_status()
        mappings = response.json()
        self.config = {**mappings, **self._STATIC_CONFIG}

    def get_config(self):
        return self.config
