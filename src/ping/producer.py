import pika
from utils import json_to_bytes

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='fibonacci')

while True:
    x = input("Calc the fibonacci of (input in):")
    if not x.isnumeric():
        break

    to_send = dict(x=int(x))
    body = json_to_bytes(to_send)

    channel.basic_publish(exchange='',
                        routing_key='fibonacci',
                        body=body)
    print(f"Send: {x}")


connection.close()