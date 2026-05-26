import json
import pika
from experiments_engine.config import Settings
from experiments_engine.runner import experiment

# RabbitMQ consumer class.
# this whole class listens for experiment messages and passes them into the encoding system


class MessageConsumer:

    def __init__(self, engine):

        # RabbitMQ connection object
        self.connection = None

        # RabbitMQ communication channel
        self.channel = None

        # used to start experiment processing
        self.engine = engine

    def connect(self):

        # Connect to RabbitMQ container.

        # because RabbitMQ runs inside Docker we can use the container name

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                Settings.queue_container
            )
        )

        # Create communication channel.
        #
        #  channel is used to:
        # - send messages
        # - receive messages
        # - acknowledge messages

        self.channel = self.connection.channel()

        # Declare queue.
        #
        # if queue already exists then RabbitMQ reuses it.

        self.channel.queue_declare(
            queue=Settings.experiment_queue,
            exclusive=True
        )

    def listen(self):

        # set up message consumption
        # auto_ack=False means messages are only acknowledged AFTER processing is completed successfully

        self.channel.basic_consume(
            queue=Settings.experiment_queue,
            on_message_callback=self.on_message,
            auto_ack=False
        )

        print("Waiting for messages")

        # starts listening for new experiment messages- continuous process

        self.channel.start_consuming()

    def on_message(self, ch, method, properties, body):

        #automatically runs whenever RabbitMQ sends a message

        try:

            # runner.py logic.

            experiment(body)

            # convert JSON message into python dictionary.

            data = json.loads(body)

            # get experiment id from incoming message.

            experiment_id = data["experiment_id"]

            # passes experiment into Engine workflow.

            self.engine.process(experiment_id)

            # only acknowledge message AFTER processing completes successfully

            self.acknowledge(method)

        except Exception:

            # rejecting the failed message

            self.reject(method)

    def acknowledge(self, method):

        # acknowledge successful processing- tells RabbitMQ the message can now be removed from the queue

        self.channel.basic_ack(
            delivery_tag=method.delivery_tag
        )

    def reject(self, method):

        # reject failed processing- tells RabbitMQ processing failed.

        self.channel.basic_nack(
            delivery_tag=method.delivery_tag
        )

    def disconnect(self):

        # close RabbitMQ connection cleanly

        if self.connection:
            self.connection.close()