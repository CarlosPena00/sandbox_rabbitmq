#!/usr/bin/env python
import pika
from utils import bytes_to_json, json_to_bytes

def slow_fibonacci(n):
    if n in {0, 1}:
        return n
    return slow_fibonacci(n - 1) + slow_fibonacci(n - 2)


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='fibonacci')


def on_request(ch, method, props, body):
    input_val = bytes_to_json(body)
    n = input_val["x"]

    print(f" - fib({n})")
    resp = dict(
        response=slow_fibonacci(n))

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id),
                     body=json_to_bytes(resp))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='fibonacci', on_message_callback=on_request)

print(" Awaiting RPC requests")
channel.start_consuming()
