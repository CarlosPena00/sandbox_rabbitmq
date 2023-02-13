import pika
import sys
import os

from utils import bytes_to_json


def slow_fibonacci(n):
    if n in {0, 1}:
        return n
    return slow_fibonacci(n - 1) + slow_fibonacci(n - 2)


def callback(ch, method, properties, body):
    _ = (ch, method, properties)
    body = bytes_to_json(body)
    print(f"Received: {body=}")
    response = slow_fibonacci(body["x"])
    print(f"{response=}")


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='fibonacci')
    channel.basic_consume(
        queue='fibonacci', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
