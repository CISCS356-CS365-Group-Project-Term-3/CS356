from .util import run_except

def setup_namespaces(namespace1, namespace2, veth1, veth2):

    # Create both namespaces
    run_except(["ip", "netns", "add", namespace1])
    run_except(["ip", "netns", "add", namespace2])

    # Create virtual ethernet connection
    run_except(["ip", "link", "add", veth1, "type", "veth", "peer", "name", veth2])

    # Assign the ends of that virtual cable to a namespace
    run_except(["ip", "link", "set", veth1, "netns", namespace1])
    run_except(["ip", "link", "set", veth2, "netns", namespace2])
