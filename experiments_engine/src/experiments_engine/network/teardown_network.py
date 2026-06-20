from .util import run_except
from ..config import Settings as Config
Settings = Config.NetworkSimSettings

def teardown_network():
    # Tear down namespaces
    run_except(["sudo", "ip", "netns", "del", Settings.namespace_1])
    run_except(["sudo", "ip", "netns", "del", Settings.namespace_2])

#always attempt to teardown network at startup- useful for debugging, remove for deployment
try: 
    teardown_network()
except:
    pass