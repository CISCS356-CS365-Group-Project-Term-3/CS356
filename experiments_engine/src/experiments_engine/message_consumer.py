import json
import pika
from .config import Settings
from .runner import run
from .engine import Engine

# RabbitMQ consumer class.
# this whole class listens for experiment messages and passes them into the encoding system


class MessageConsumer:

    def __init__(self, engine):

        # RabbitMQ connection object
        self.connection: pika.BlockingConnection

        # used to start experiment processing
        self.engine: Engine = engine

    def connect(self):

        # Connect to RabbitMQ container.

        # because RabbitMQ runs inside Docker we can use the container name

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                Settings.queue_address
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
            # convert JSON message into python dictionary.


            experiment = json.loads(body)

            # passes experiment into Engine workflow.

            self.engine.process(experiment)

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