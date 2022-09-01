import json
import pika
import threading


def consumer_factory(func, bus):
    def inner(ch, method, properties, body):
        return func(bus, json.loads(body.decode('utf-8')))

    inner.__name__ = func.__name__
    return inner


class ConsumerRegistry:
    def __init__(self):
        self.consumers = list()

    def register(self, exchange, callback, **kwargs):
        host = kwargs.pop("host", "localhost")
        exchange_type = kwargs.pop("exchange_type", "direct")
        consumer = Consumer(host, callback, exchange, exchange_type)
        self.consumers.append(consumer)
        consumer.start()


class Consumer(threading.Thread):
    def __init__(self, host, consumer, exchange, exchange_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        conn = self.get_connection(host)
        self.channel = conn.channel()
        self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
        result = self.channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue

        self.channel.queue_bind(
            queue=queue_name, 
            exchange=exchange, 
            routing_key=consumer.__name__
        )
        self.channel.basic_consume(
            auto_ack=True,
            queue=queue_name, 
            on_message_callback=consumer, 
        )
    
    def get_connection(self, host):
        return pika.BlockingConnection(pika.ConnectionParameters(host=host))

    def run(self):
        self.channel.start_consuming()


registry = ConsumerRegistry()


def register(*args, **kwargs):
    registry.register(*args, **kwargs)


class ExternalMessage:
    def __init__(self, exchange, exchange_type, routing_key, body, host="localhost"):
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.routing_key = routing_key
        self.body = body
        self.host = host

def publish_message(msg: ExternalMessage):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=msg.host))
    channel = connection.channel()
    channel.exchange_declare(exchange=msg.exchange, exchange_type=msg.exchange_type)
    body = json.dumps(msg.body)
    channel.basic_publish(exchange=msg.exchange, routing_key=msg.routing_key, body=body)
    connection.close()