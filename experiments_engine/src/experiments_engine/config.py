import os


# this class creates the settings object used in worker
# settings are read from environment variables e.g. the "QUEUE_NAME" envirnoment variable
# if the environment variable isn't set, a default value is given
class Settings:

    config_map_path:str = os.getenv('CONFIG_MAP_PATH', './config_map.json')

    experiment_queue:str = os.getenv('QUEUE_NAME', 'experiment_queue')
    queue_address:str = os.getenv('QUEUE_CONTAINER', 'localhost')

    output_mongo_uri:str = os.getenv('OUTPUT_MONGO_URI','mongodb://admin:admin@localhost:27017/')
    output_mongo_db_name = os.getenv("OUTPUT_MONGO_DB_NAME", "experiment_storage")

    # expected migration do postgres- commented for now
    #config_mongo_uri:str = os.getenv('CONFIG_MONGO_URI','mongodb://admin:admin@localhost:27017/')
    #config_mongo_db_name = os.getenv("CONFIG_MONGO_DB_NAME", "experiment_storage")

    input_directory = os.getenv("INPUT_DIR", "./experiments_engine/tests/test_data/input")
    temp_directory = os.getenv("TEMP_DIR", "./experiments_engine/tests/test_data/temp")
    output_directory = os.getenv("OUTPUT_DIR", "./experiments_engine/tests/test_data/output")

    log_level = os.getenv("LOG_LEVEL", "INFO")