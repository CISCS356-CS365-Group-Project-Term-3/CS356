import subprocess
from experiments_engine.network import setup_namespaces
from experiments_engine.config import Settings as Config

# NOTE: The tests in this file are designed to be run in a Linux environment with the necessary permissions to manipulate network namespaces.
# NOTE: These tests need to be run using sudo in order to be given root privileges
# NOTE: EXAMPLE: sudo /home/<user>/CS356/.venv/bin/python3 -m pytest tests/test_setup_namespaces.py -q

Settings = Config.NetworkSimSettings

def test_setup_namespaces():
    setup_namespaces.setup_namespaces(Settings.namespace_1, Settings.namespace_2, Settings.veth_1, Settings.veth_2)

    # Get a list of all namespaces
    namespace_result = subprocess.check_output(["ip", "netns", "list"])
    print(f"Namespaces after setup: {namespace_result.decode('utf-8')}")

    # Assert that the namespace 1 and namespace 2 have been created and are present in the list of namespaces
    assert Settings.namespace_1 in namespace_result.decode('utf-8')
    assert Settings.namespace_2 in namespace_result.decode('utf-8')

    # Get the list of interfaces for namespace 1
    virtual_eth_1_result = subprocess.check_output(["sudo", "ip", "netns", "exec", Settings.namespace_1, "ip", "link"])

    # Assert that virtual ethernet connection 1 is present in the list of interfaces for namepspace 1
    assert Settings.veth_1 in virtual_eth_1_result.decode('utf-8')

    # Get the list of interfaces for namespace 2
    virtual_eth_2_result = subprocess.check_output(["sudo", "ip", "netns", "exec", Settings.namespace_2, "ip", "link"])

    # Assert that virtual ethernet connection 2 is present in the list of interfaces for namepspace 2
    assert Settings.veth_2 in virtual_eth_2_result.decode('utf-8')