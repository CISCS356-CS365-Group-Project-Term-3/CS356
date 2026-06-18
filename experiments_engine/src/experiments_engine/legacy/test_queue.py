""" import queue
import threading
import time

import pika
import pytest
from docker.errors import DockerException
from testcontainers.rabbitmq import RabbitMqContainer

from experiments_engine import worker


def test_consume_acks_message_and_prints_it(capsys):
    queue_name = f"test-queue-1"
    message_text = f"integration-message-1"
    original_queue_name = worker.Settings.experiment_queue

    try:
        rabbitmq = RabbitMqContainer("rabbitmq:3.13-alpine")
    except DockerException as exc:
        pytest.skip(f"Docker is unavailable for testcontainers: {exc}")

    worker.Settings.experiment_queue = queue_name

    try:
        with rabbitmq:

            connection_params = rabbitmq.get_connection_params()
            publisher_connection = pika.BlockingConnection(connection_params)
            publisher_channel = publisher_connection.channel()
            publisher_channel.queue_declare(queue=queue_name)

            consumer_connection = pika.BlockingConnection(connection_params)
            consumer_channel = consumer_connection.channel()
            consumer_result: queue.Queue[BaseException | None] = queue.Queue()

            def run_consumer() -> None:
                try:
                    worker.setup_consume(consumer_channel)
                    worker.consume(consumer_channel)
                    consumer_result.put(None)
                except BaseException as exc:  # pragma: no cover - surfaced below
                    consumer_result.put(exc)
                finally:
                    if consumer_connection.is_open:
                        consumer_connection.close()

            consumer_thread = threading.Thread(target=run_consumer, daemon=True)
            consumer_thread.start()

            try:
                output = ""
                ready_deadline = time.monotonic() + 20
                while time.monotonic() < ready_deadline:
                    output += capsys.readouterr().out
                    if "Waiting for messages" in output:
                        break
                    time.sleep(0.1)
                assert "Waiting for messages" in output

                publisher_channel.basic_publish(
                    exchange="",
                    routing_key=queue_name,
                    body=message_text.encode(),
                )

                message_deadline = time.monotonic() + 20
                while time.monotonic() < message_deadline:
                    output += capsys.readouterr().out
                    if message_text in output:
                        break
                    time.sleep(0.1)
                assert message_text in output

                consumer_connection.add_callback_threadsafe(consumer_channel.stop_consuming)
                consumer_thread.join(timeout=10)
                assert not consumer_thread.is_alive()

                consumer_error = consumer_result.get(timeout=1)
                if consumer_error is not None:
                    raise consumer_error

                verify_connection = pika.BlockingConnection(connection_params)
                verify_channel = verify_connection.channel()
                method_frame, _, body = verify_channel.basic_get(queue=queue_name, auto_ack=True)
                assert method_frame is None, (
                    "Expected the worker to ack the message before shutdown, "
                    f"but the message was requeued with body={body!r}."
                )
                verify_connection.close()
            finally:
                if consumer_thread.is_alive():
                    consumer_connection.add_callback_threadsafe(consumer_channel.stop_consuming)
                    consumer_thread.join(timeout=10)
                if publisher_connection.is_open:
                    publisher_connection.close()
    finally:
        worker.Settings.experiment_queue = original_queue_name
 """