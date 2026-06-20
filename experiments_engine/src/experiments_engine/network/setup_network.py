from .setup_namespaces import setup_namespaces
from .util import run_except
from typing import List

import logging
logger = logging.getLogger(__name__)

from ..config import Settings as Config
Settings = Config.NetworkSimSettings

# setup_ip_to_ip()
#
# Description:
#       Set up virtual network based on command line arguments
#
# Can Jitter % and correlation type can be added in future
#
def setup_ip_to_ip(delay: int|None=None, jitter: int|None=None, throttle_bw=None, packet_loss: float|None=None):
    # Handle command line inputs

    # Set up namespaces
    setup_namespaces(Settings.namespace_1, Settings.namespace_2, Settings.veth_1, Settings.veth_2)
    # logger.info("Created namespaces")

    # Set IP addresses of both namespace interfaces
    run_except(["sudo", "ip", "netns", "exec", Settings.namespace_1, "ip", "addr", "add", f"{Settings.ip_1}/24", "dev", Settings.veth_1])
    run_except(["sudo", "ip", "netns", "exec", Settings.namespace_2, "ip", "addr", "add", f"{Settings.ip_2}/24", "dev", Settings.veth_2])

    # Set both interfaces to up mode
    run_except(["sudo", "ip", "netns", "exec", Settings.namespace_1, "ip", "link", "set", Settings.veth_1, "up"])
    run_except(["sudo", "ip", "netns", "exec", Settings.namespace_2, "ip", "link", "set", Settings.veth_2, "up"])

    behavior_command = ""
    if delay  and jitter:
        run_except(["sudo", "ip", "netns", "exec", Settings.namespace_1, "tc", "qdisc", "add", "dev", Settings.veth_1, "root", "netem", "delay", f"{delay}ms", f"{jitter}ms", "50%"])
    elif delay:
        run_except(["sudo", "ip", "netns", "exec", Settings.namespace_1, "tc", "qdisc", "add", "dev", Settings.veth_1, "root", "netem", "delay", f"{delay}ms"])

    # throttle out of scope for MVP
       # behavior_command = "ip netns exec namespace1 tc qdisc add dev virtualeth1 root tbf latency 200ms burst 32kbit rate 100kbit"
    
    
    if packet_loss:
        run_except(["sudo", "ip", "netns", "exec", Settings.namespace_1, "tc", "qdisc", "add", "dev", Settings.veth_1, "root", "netem", "loss", f"{packet_loss}%"])

def namespace_command_prefix(namespace: str) -> List[str]:
    return ['sudo', 'ip', 'netns', 'exec', namespace]

def encoder_endpoint():
    return f"{Settings.protocol}://{Settings.ip_2}:{Settings.port}"

def decoder_endpoint():
    
    endpoint = ""
    if Settings.protocol == "udp":
        # udp has no end signal, so use a 2 second timeout to check for end of stream (max delay is 1 second)
        # definitely not the cleanest long  term solution
        return f"{Settings.protocol}://127.0.0.1:{Settings.port}?timeout=2000000"
    elif Settings == "rtsp":
        return f"{Settings.protocol}://{Settings.ip_1}:{Settings.port}"
