"""
Lightweight RabbitMQ publisher with a print fallback for local testing.

Environment variables:
- `QUEUE_NAME` (default: "experiment_queue")
- `QUEUE_CONTAINER` (default: "localhost")
- `RABBIT_PORT` (default: 5672)

If `pika` is not installed or RabbitMQ is unavailable this will still
print the message so other parts of the app can be tested locally.
"""
import os
import json
import logging
import time

try:
    import pika
except Exception:
    pika = None

logging.basicConfig(level=logging.INFO)

QUEUE_NAME = os.getenv("QUEUE_NAME", "experiment_queue")
RABBIT_HOST = os.getenv("QUEUE_CONTAINER", "localhost")
RABBIT_PORT = int(os.getenv("RABBIT_PORT", 5672))

_connection = None
_channel = None


def _connect(retries: int = 3, delay: float = 2.0):
    """Attempt to establish a blocking connection to RabbitMQ."""
    global _connection, _channel

    if pika is None:
        logging.warning("pika not available; will fallback to printing events.")
        return

    if _connection and getattr(_connection, "is_open", False):
        return

    params = pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT, heartbeat=600)
    for attempt in range(1, retries + 1):

        try:
            _connection = pika.BlockingConnection(params)
            _channel = _connection.channel()
            _channel.queue_declare(queue=QUEUE_NAME, durable=True)
            logging.info("Connected to RabbitMQ %s:%s queue=%s", RABBIT_HOST, RABBIT_PORT, QUEUE_NAME)
            return
        except Exception:
            logging.exception("RabbitMQ connection attempt %d failed", attempt)
            _connection = None
            _channel = None
            if attempt < retries:
                time.sleep(delay)


def publish_to_queue(message: object):
    """Publish `message` (serializable) to RabbitMQ, or print if unavailable.

    This function always prints the message for test visibility.
    """

    print("EVENT:", message)



    if pika is None:
        return


    if _connection is None or not getattr(_connection, "is_open", False):
        _connect()


    if _channel is None:
        return

    try:
        body = json.dumps(message)
        _channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=body,
            properties=pika.BasicProperties(delivery_mode=2),
        )
        logging.info("Published message to queue %s", QUEUE_NAME)
    except Exception:
        logging.exception("Failed to publish message to RabbitMQ; event printed instead")



def publish_to_queue(message):
    print("EVENT:", message)