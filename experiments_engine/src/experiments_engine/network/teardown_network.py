from .util import run_except
from ..config import Settings

def teardown_network():
    # Tear down namespaces
    run_except(f"ip netns del {Settings.namespace_1}", shell=True)
    run_except(f"ip netns del {Settings.namespace_2}", shell=True)
