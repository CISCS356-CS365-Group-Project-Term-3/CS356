import pytest

from experiments_engine.message_consumer import MessageConsumer


class FakeEngine:
    def __init__(self, should_fail=False):
        self.experiments = []
        self.should_fail = should_fail

    def process(self, experiment):
        if self.should_fail:
            raise RuntimeError("failed")
        self.experiments.append(experiment)


class FakeChannel:
    def __init__(self):
        self.acknowledged = False
        self.rejected = False
        self.delivery_tag = None

    def basic_ack(self, delivery_tag):
        self.acknowledged = True
        self.delivery_tag = delivery_tag

    def basic_nack(self, delivery_tag):
        self.rejected = True
        self.delivery_tag = delivery_tag


class FakeMethod:
    delivery_tag = "123"


def test_init_stores_engine():
    engine = FakeEngine()

    consumer = MessageConsumer(engine)

    assert consumer.engine == engine
    assert consumer.connection is None
    assert consumer.channel is None


def test_acknowledge_acks_message():
    consumer = MessageConsumer(FakeEngine())
    consumer.channel = FakeChannel()

    consumer.acknowledge(FakeMethod())

    assert consumer.channel.acknowledged is True
    assert consumer.channel.delivery_tag == "123"


def test_acknowledge_requires_channel():
    consumer = MessageConsumer(FakeEngine())

    with pytest.raises(RuntimeError, match="not connected"):
        consumer.acknowledge(FakeMethod())


def test_on_message_processes_json_and_acknowledges():
    engine = FakeEngine()
    consumer = MessageConsumer(engine)
    consumer.channel = FakeChannel()

    consumer.on_message(None, FakeMethod(), None, b'{"experiment_id":"EXP001"}')

    assert engine.experiments == [{"experiment_id": "EXP001"}]
    assert consumer.channel.acknowledged is True


def test_on_message_rejects_when_processing_fails():
    consumer = MessageConsumer(FakeEngine(should_fail=True))
    consumer.channel = FakeChannel()

    consumer.on_message(None, FakeMethod(), None, b'{"experiment_id":"EXP001"}')

    assert consumer.channel.rejected is True
    assert consumer.channel.delivery_tag == "123"
