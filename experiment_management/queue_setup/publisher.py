import json
import pika

def publish_to_queue(message):
    """
    Add RabbitMQ Publisher Logic here for now creating a print message
    to test functionality
    """
   # connection = pika.BlockingConnection(
   #     pika.ConnectionParameters(host="queue")
   # )

   # channel = connection.channel()

   # channel.queue_declare(queue="experiment_queue", durable=True)

   # channel.basic_publish(
   #     exchange="",
   #     routing_key="experiment_queue",
   #     body=json.dumps(message),
   #     properties=pika.BasicProperties(
   #         delivery_mode=2
   #     )
   # )
    # connection.close()
    print("EVENT:", message)