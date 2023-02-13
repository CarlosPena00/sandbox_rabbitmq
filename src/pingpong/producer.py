import pika
import uuid
from utils import json_to_bytes

import pika
import uuid


class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='fibonacci',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json_to_bytes(n))
        self.connection.process_data_events(time_limit=None)
        return self.response


fibonacci_rpc = FibonacciRpcClient()


while True:
    x = input("Calc the fibonacci of (input in):")
    if not x.isnumeric():
        break

    to_send = dict(x=int(x))
    response = fibonacci_rpc.call(to_send)
    print(f"\tGot {response}")
