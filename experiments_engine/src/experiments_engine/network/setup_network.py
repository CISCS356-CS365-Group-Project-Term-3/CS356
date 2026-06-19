from .setup_namespaces import setup_namespaces
from .util import run_except

import logging
logger = logging.getLogger(__name__)

from ..config import Settings

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
    logger.info("Created namespaces")

    # Set IP addresses of both namespace interfaces
    ip_string1 = f'ip netns exec {Settings.namespace_1} ip addr add {Settings.ip_1}/32 dev {Settings.veth_1}'
    ip_string2 = f'ip netns exec {Settings.namespace_2} ip addr add {Settings.ip_2}/34 dev {Settings.veth_2}'
    run_except(ip_string1, shell=True)
    run_except(ip_string2, shell=True)

    # Set both interfaces to up mode
    run_except(f"ip netns exec {Settings.namespace_1} ip link set {Settings.veth_1} up", shell=True)
    run_except(f"ip netns exec {Settings.namespace_2} ip link set {Settings.veth_2} up", shell=True)

    behavior_command = ""
    if delay  and jitter:
        run_except(f'ip netns exec {Settings.namespace_1} tc qdisc add dev {Settings.veth_1} root netem delay {delay}ms {jitter}ms 50%')
    elif delay:
        run_except(f'ip netns exec {Settings.namespace_1} tc qdisc add dev {Settings.veth_1} root netem delay {delay}ms')

    # throttle out of scope for MVP
       # behavior_command = "ip netns exec namespace1 tc qdisc add dev virtualeth1 root tbf latency 200ms burst 32kbit rate 100kbit"
    
    
    if packet_loss:
        run_except(f'ip netns exec {Settings.namespace_1} tc qdisc add dev {Settings.veth_1} root netem loss {packet_loss}%')