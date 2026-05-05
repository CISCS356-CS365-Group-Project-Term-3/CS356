import pika
from .runner import experiment
from .config import Settings

# Callback function to process messages
def callback(ch, method, properties, body):
        experiment(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

def consume(channel):
     # Declare the queue
        channel.queue_declare(queue=Settings.experiment_queue)

        # Set prefetch to 1 so worker only processes 1 experiment at a time
        channel.basic_qos(prefetch_count=1)

        print("Waiting for messages")
            
        # Start consuming messages
        channel.basic_consume(queue=Settings.experiment_queue, on_message_callback=callback, auto_ack=False)
        channel.start_consuming()

def main():

    while True:
        # Connect to RabbitMQ container
        connection = pika.BlockingConnection(pika.ConnectionParameters('queue'))
        channel = connection.channel()

        consume(channel)


