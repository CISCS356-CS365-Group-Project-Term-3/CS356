import pika


# Settings are used throughout the code for the name of the queue and the name of the queue container
from .config import Settings

# Callback function to process messages
# The callback function is called when a message is consumed from the queue
def callback(ch, method, properties, body):

        # run the experiment on the body of the message
        #experiment(body)

        # only acknowledge the message AFTER we have finished running the experiment
        ch.basic_ack(delivery_tag=method.delivery_tag)

def setup_consume(channel):

        # This step sets up what happens when a message is "consumed" from the queue
        #
        # The name of the queue is required (we have declared it/created it, but RabbitMQ doesn't know it is the only queue)
        #
        # the callback function is the function that is called when a message is consumed
        #
        # auto_ack=False says that we don't want to automatically tell the queue we have read the message
        # this is important, as we don't want to acknowledge the next experiment before we are done processing the current one
        #
        #                                (name of the queue)     (function that is called)  (don't acknowledge)
        channel.basic_consume(queue=Settings.experiment_queue, on_message_callback=callback, auto_ack=False)

def consume(channel):
        # Start consuming messages
        print("Waiting for messages")
        channel.start_consuming()

def main():
        # Connect to RabbitMQ container

        # This step sets up a conection to the queue
        # Typically, the address of the queue would be an IP address, but since this will run in a container, we can use the name of the container
        #                                                               (address of the queue)
        connection = pika.BlockingConnection(pika.ConnectionParameters(Settings.queue_container))

        # A channel is like your session with RabbitMQ
        channel = connection.channel()

        # This step "declares" a queue with RabbitMQ
        # "declaring" a queue checks if it exists, and creates it if it doesn't exist
        # in our system, the expectation is that it won't exist, and we are creating it
        #
        # our system only has 1 queue so we simply just use the name of our queue
        # exclusive=True tells RabbitMQ that we are the only connection that can read from the queue (expermint management pushes, we read)
        # this isn't the most important thing ever
        #                             (name of the queue)      (exclusivity)
        channel.queue_declare(queue=Settings.experiment_queue, exclusive=True)

        setup_consume(channel)

        while True:
                consume(channel)
