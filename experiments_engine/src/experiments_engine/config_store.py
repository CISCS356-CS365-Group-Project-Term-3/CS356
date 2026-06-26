from .config import Settings
import requests


class ConfigStore:

    _STATIC_CONFIG = {
        "encoder_type": {"000": "standard", "001": "scalable"},
        "loss": "DECIMAL",
        "delay": "INTEGER",
        "jitter": "INTEGER"
    }

    def __init__(self, db_connection=None):
        response = requests.get(f"{Settings.infra_api_url}/rest/mappings")
        response.raise_for_status()
        mappings = response.json()
        self.config = {**mappings, **self._STATIC_CONFIG}

    def get_config(self):
        return self.config
