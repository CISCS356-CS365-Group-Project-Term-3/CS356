import json

# rabbitmq consumer class.


class MessageConsumer:

    def __init__(self, engine):

        # rabbitmq connection/channel
        self.connection = None
        self.channel = None

        # engine collaborator
        self.engine = engine

    def connect(self):

        # connects to rabbitmq

        pass

    def listen(self):

        #  listening for messages

        pass

    def on_message(self, message):

        # Handles received message

        data = json.loads(message)

        experiment_id = data["experiment_id"]

        self.engine.process(experiment_id)

        self.acknowledge(message)

    def acknowledge(self, message):

        # ack successful message

        pass

    def reject(self, message):

        # rejects failed message

        pass

    def disconnect(self):

        # Disconnects from rabbitmq

        pass