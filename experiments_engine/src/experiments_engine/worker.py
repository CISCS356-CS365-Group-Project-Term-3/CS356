import pika
from .runner import experiment
from .config import Settings

# Callback function to process messages
def callback(ch, method, properties, body):
        experiment(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

def setup_consume(channel):
        channel.basic_consume(queue=Settings.experiment_queue, on_message_callback=callback, auto_ack=False)

def consume(channel):
        # Start consuming messages
        print("Waiting for messages")
        channel.start_consuming()

def main():
        # Connect to RabbitMQ container
        connection = pika.BlockingConnection(pika.ConnectionParameters(Settings.queue_container))
        channel = connection.channel()

        channel.queue_declare(queue=Settings.experiment_queue, exclusive=True)

        setup_consume(channel)
        while True:
                consume(channel)
