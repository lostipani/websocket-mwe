import time

from commons.logger import logger
from commons.parser import get_broker_params, get_consumer_period
from commons.broker import Broker


def consumer(broker: Broker, period: float) -> None:

    def callback_fun(channel, method, properties, body):
        """
        RabbitMQ dependent callback function to deal with incoming message
        """
        del channel, method, properties
        logger.info(body.decode("utf-8"))
        time.sleep(period)

    broker.get(callback=callback_fun)


def main(broker: Broker) -> None:
    consumer(broker, get_consumer_period())


if __name__ == "__main__":
    broker_params = get_broker_params()
    broker = Broker.factory(
        backend="rabbitmq",
        queue="test",
        host=broker_params.get("host"),
        routing_key="test",
        exchange="",
    )
    main(broker)
