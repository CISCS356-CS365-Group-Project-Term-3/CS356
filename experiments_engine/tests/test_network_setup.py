import pytest

from experiments_engine.network import setup_network


def test_setup_ip_to_ip_applies_packet_loss_as_percent(monkeypatch):
    commands = []

    monkeypatch.setattr(setup_network, "setup_namespaces", lambda *args: None)
    monkeypatch.setattr(setup_network, "run_except", commands.append)

    setup_network.setup_ip_to_ip(packet_loss=20.0)

    tc_commands = [command for command in commands if "tc" in command]

    assert tc_commands == [
        [
            "ip",
            "netns",
            "exec",
            setup_network.Settings.namespace_1,
            "tc",
            "qdisc",
            "add",
            "dev",
            setup_network.Settings.veth_1,
            "root",
            "netem",
            "loss",
            "20%",
        ]
    ]


def test_setup_ip_to_ip_combines_delay_jitter_and_loss(monkeypatch):
    commands = []

    monkeypatch.setattr(setup_network, "setup_namespaces", lambda *args: None)
    monkeypatch.setattr(setup_network, "run_except", commands.append)

    setup_network.setup_ip_to_ip(delay=50, jitter=10, packet_loss=2.5)

    tc_commands = [command for command in commands if "tc" in command]

    assert tc_commands == [
        [
            "ip",
            "netns",
            "exec",
            setup_network.Settings.namespace_1,
            "tc",
            "qdisc",
            "add",
            "dev",
            setup_network.Settings.veth_1,
            "root",
            "netem",
            "delay",
            "50ms",
            "10ms",
            "50%",
            "loss",
            "2.5%",
        ]
    ]


@pytest.mark.parametrize(
    ("segment", "expected_loss"),
    [
        ("000", 0.0),
        ("001", 0.1),
        ("010", 1.0),
        ("200", 20.0),
    ],
)
def test_sequence_decoder_decodes_packet_loss_as_tenths_of_percent(segment, expected_loss):
    from experiments_engine.sequence_decoder import SequenceDecoder

    config = {
        "raw_file": {"000": "input.y4m"},
        "encoder_type": {"000": "standard"},
        "codec": {"000": "h264"},
        "encoder_mode": {"000": "dummy"},
        "loss": "PERCENT_TENTHS",
        "delay": "INTEGER",
        "jitter": "INTEGER",
    }
    code = "000000000" + segment + "000000"

    actual_loss = SequenceDecoder.decode(code, config)["loss"]
    print(actual_loss)
    assert actual_loss == expected_loss
