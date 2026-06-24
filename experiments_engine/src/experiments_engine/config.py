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

    class NetworkSimSettings:
        namespace_1 =  os.getenv("NAMESPACE_1", "namespace_1")
        namespace_2 =  os.getenv("NAMESPACE_2", "namespace_2")

        ip_1 =  os.getenv("IP_1", "140.40.5.1")
        ip_2 =  os.getenv("IP_2", "140.40.5.2")

        port = os.getenv("NETWORK_SIM_PORT", "1234")
        protocol = os.getenv("NETWORK_SIM_PROTOCOL", "udp")

        veth_1 =  os.getenv("VIRTUAL_ETH_1", "virtual_eth_1")
        veth_2 =  os.getenv("VIRTUAL_ETH_2", "virtual_eth_2")