import os
from experiment_management.queue_setup.publisher import publish_to_queue


def main():
    os.environ.setdefault("QUEUE_NAME", "experiment_queue")
    os.environ.setdefault("QUEUE_CONTAINER", "localhost")
    os.environ.setdefault("RABBIT_PORT", "5672")

    test_payload = {
        "event": "publisher_test",
        "timestamp": "2026-05-29T00:00:00Z",
        "details": {
            "note": "This test prints the message and attempts RabbitMQ publish if pika is installed."
        },
    }

    print("Running publisher test with payload:")
    publish_to_queue(test_payload)


if __name__ == "__main__":
    main()
