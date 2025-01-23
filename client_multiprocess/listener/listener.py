import json
import pika
import time
from websockets.sync.client import connect

from commons.logger import logger
from commons.parser import get_URI, get_listener_period, get_broker_params
from commons.broker import Broker


def listener(URI: str, broker: Broker, period: float) -> None:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=broker.params.get("host"))
        )
        channel = connection.channel()
        with connect(URI) as websocket:
            for message in websocket:
                channel.queue_declare(queue=broker.params.get("queue"))
                channel.basic_publish(
                    exchange="",
                    routing_key=broker.params.get("routing_key"),
                    body=str(json.loads(message)["value"]),
                    properties=pika.BasicProperties(
                        delivery_mode=pika.DeliveryMode.Persistent
                    ),
                )
                # connection.close()
                # broker.add(str(json.loads(message)["value"]))
                time.sleep(period)
    except ConnectionRefusedError as error:
        logger.error(error)
        raise


def main(broker: Broker):
    listener(get_URI(), broker, get_listener_period())


if __name__ == "__main__":
    broker_params = get_broker_params()
    broker = Broker.factory(
        backend="rabbitmq",
        queue="test",
        host=broker_params.get("host"),
        routing_key="test",
    )
    main(broker)
