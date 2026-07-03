import subprocess
from src.experiments_engine.network import setup_network
from src.experiments_engine.config import Settings as Config

# NOTE: The tests in this file are designed to be run in a Linux environment with the necessary permissions to manipulate network namespaces.
# NOTE: These tests need to be run using sudo in order to be given root privileges
# NOTE: EXAMPLE: sudo /home/<user>/CS356/.venv/bin/python3 -m pytest tests/test_setup_network.py -q

Settings = Config.NetworkSimSettings

# ***** UTILITY FUNCTIONS FOR CONFIRMING NETWORK BEHAVIORS *****
def confirm_jitter(ping_result: str, delay_amount: int, jitter_amount: int) -> bool:
    times = []
    result_lines = ping_result.splitlines()

    # Retrieve the time values from each ping line and store them in a list
    for line in result_lines:
        if "time=" in line:
            current_time = line.split("time=")[1].split(" ")[0]
            times.append(float(current_time))
            
    # Removes the first time value as it often is an outlier and does not represent the jitter behavior accurately  
    times.pop(0)

    # Check that each time value lies within the bounds of the jitter range.
    for time in times:
        if time >= delay_amount - jitter_amount and time <= delay_amount + jitter_amount:
            continue
        else:
            raise AssertionError(f"Time {time} is outwith the bounds of {delay_amount}ms delay with {jitter_amount}ms of jitter")
    
    # Check that there is at least one instance of variation in the delay time to confirm the presence of jitter behavior
    for i, time in enumerate(times):
        if i > 1:
            if time != times[i-1]:
                return True
    raise AssertionError("No variation in delay times detected, no jitter behavior has been emulated")

def confirm_packet_loss(ping_result: str, packet_loss_amount: int) -> bool:
    packets = []
    result_lines = ping_result.splitlines()

    # Retrieve the time values from each ping line and store them in a list
    for line in result_lines:
        if "icmp_seq=" in line:
            current_packet = line.split("icmp_seq=")[1].split(" ")[0]
            packets.append(int(current_packet))

    number_of_sent_packets = max(packets)
    number_of_received_packets = len(packets)
    loss_percentage = (number_of_sent_packets - number_of_received_packets) / number_of_sent_packets * 100

    if loss_percentage < packet_loss_amount/2:
        raise AssertionError(f"Packet loss percentage: {loss_percentage:.2f}% is significantly lower than the specified loss percentage: {packet_loss_amount}%")
    if number_of_sent_packets == number_of_received_packets:
        raise AssertionError(f"All packets were received, no packet loss detected")
    else:
        return True

# ***** TESTS FOR SETUP_IP_TO_IP FUNCTION *****
def test_setup_ip_to_ip_with_delay():
    # Set up the network with a delay of 100ms
    setup_network.setup_ip_to_ip(delay=100)

    # Ping from namespace 1 to the ip address fo namespace 2
    ping = subprocess.check_output(["sudo", "ip", "netns", "exec", Settings.namespace_1, "ping", "-c", "5", Settings.ip_2])

    # Get the output of the ping command
    ping_result = ping.decode('utf-8')

    # Clean up the namespaces before the next test
    subprocess.run(f"sudo ip netns del {Settings.namespace_1}", shell=True)
    subprocess.run(f"sudo ip netns del {Settings.namespace_2}", shell=True)

    assert f"PING {Settings.ip_2}" in ping_result
    assert f"time=100 ms" in ping_result

def test_setup_ip_to_ip_with_jitter():
    # Set up the network with a delay of 100ms
    delay_amount = 100
    jitter_amount = 30
    setup_network.setup_ip_to_ip(delay=delay_amount, jitter=jitter_amount)

    # Ping from namespace 1 to the ip address fo namespace 2
    ping = subprocess.check_output(["sudo", "ip", "netns", "exec", Settings.namespace_1, "ping", "-c", "5", Settings.ip_2])

    # Get the output of the ping command
    ping_result = ping.decode('utf-8')

    # Clean up the namespaces before the next test
    subprocess.run(f"sudo ip netns del {Settings.namespace_1}", shell=True)
    subprocess.run(f"sudo ip netns del {Settings.namespace_2}", shell=True)

    assert f"PING {Settings.ip_2}" in ping_result
    assert confirm_jitter(ping_result, delay_amount, jitter_amount) == True

def test_setup_ip_to_ip_with_packet_loss():
    # Set up the network with a delay of 100ms
    packet_loss_amount = 30
    setup_network.setup_ip_to_ip(packet_loss=packet_loss_amount)

    # Ping from namespace 1 to the ip address fo namespace 2
    ping = subprocess.check_output(["sudo", "ip", "netns", "exec", Settings.namespace_1, "ping", "-c", "20", Settings.ip_2])

    # Get the output of the ping command
    ping_result = ping.decode('utf-8')

    print(f"Ping result: {ping_result}")
    subprocess.run(f"sudo ip netns del {Settings.namespace_1}", shell=True)
    subprocess.run(f"sudo ip netns del {Settings.namespace_2}", shell=True)

    assert f"PING {Settings.ip_2}" in ping_result
    assert confirm_packet_loss(ping_result, packet_loss_amount) == True