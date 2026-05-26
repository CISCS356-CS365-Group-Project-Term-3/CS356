from unittest.mock import patch
from experiments_engine.message_consumer import MessageConsumer


# test engine class
class TestEngine:

    def __init__(self):

        self.called = False

    def process(self, experiment_id):

        self.called = True


# test channel class
class TestChannel:

    def __init__(self):

        self.acknowledged = False

    def basic_ack(self, delivery_tag):

        self.acknowledged = True


# test method class
class TestMethod:

    def __init__(self):

        self.delivery_tag = "123"


def test_init():

    engine = TestEngine()

    consumer = MessageConsumer(engine)

    # check engine stored correctly
    assert consumer.engine == engine


def test_acknowledge():

    engine = TestEngine()

    consumer = MessageConsumer(engine)

    # replace channel with test channel
    consumer.channel = TestChannel()

    method = TestMethod()

    consumer.acknowledge(method)

    # check acknowledge happened
    assert consumer.channel.acknowledged is True



@patch('experiments_engine.message_consumer.experiment')
def test_on_message(mock_experiment):

    engine = TestEngine()

    consumer = MessageConsumer(engine)

    consumer.channel = TestChannel()

    method = TestMethod()

    # example json message
    message = '{"experiment_id":"EXP001"}'

    consumer.on_message(
        None,
        method,
        None,
        message
    )

    # check engine.process() was called
    assert engine.called is True