
from .message_consumer import MessageConsumer
import json
from .output_store import OutputStore
from .engine import Engine
from .config import Settings
from .config_store import ConfigStore
import os



def setup():
    ## setup logging
    import logging
    logging.basicConfig(level=Settings.log_level)
    
    ## create relevant file paths
    def create_dir(dir):
        if not os.path.exists(dir): 
            os.makedirs(dir)

    #input dir should already exist. If it doesn't we have problems
    create_dir(Settings.temp_directory)
    create_dir(Settings.output_directory)

def start():
    config_store = ConfigStore()
    output_store = OutputStore() # must add configged store connection
    engine = Engine(config_store=config_store , output_store=output_store) # create engine using the output store

    message_consumer = MessageConsumer(engine) # create message consumer that uses engine
    message_consumer.connect()
    message_consumer.listen()

def main():
    setup()
    start()

if __name__ == "__main__":
    main()

def test_only():
    config_store = ConfigStore()
    output_store = OutputStore() # must add configged store connection
    engine = Engine(config_store=config_store , output_store=output_store) # create engine using the output store

    engine.process(json.loads('''
{
  "project": {
    "experiment_id": "12345",
    "group_id": "12345",
    "user_id": "shivali_shah",
    "created_at": "2026-05-05T14:30:00Z"
  },
  "sequence": "001002000000000000"
}
                   '''))

