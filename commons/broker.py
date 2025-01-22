import abc
from typing import Any, List
import pika


class BrokerNotImplementedError:
    pass


class Broker(object):
    """
    Broker classes have to feature the following methods:
        add
        size
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, backend: Any, **kwargs):
        self.backend = backend

    def __str__(self) -> str:
        return str(self.backend)

    @staticmethod
    def factory(backend, **kwargs):
        if isinstance(backend, list):
            return BrokerList(backend)
        elif isinstance(backend, str) and backend.lower() == "rabbitmq":
            return BrokerRabbitMQ(**kwargs)
        else:
            raise BrokerNotImplementedError

    @abc.abstractmethod
    def add(self, value):
        pass

    @abc.abstractmethod
    def size(self):
        pass


class BrokerList(Broker):
    def __init__(self, backend: List[Any]):
        super().__init__(backend)

    def add(self, value: Any):
        self.backend.append(value)

    def size(self) -> int:
        return len(self.backend)


class BrokerRabbitMQ(Broker):
    def __init__(self, **kwargs):
        super().__init__("rabbitmq")
        self.params = kwargs
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.params.get("host"))
        )

    def add(self, value: Any):
        channel = self.connection.channel()
        channel.queue_declare(queue=self.params.get("queue"))
        channel.basic_publish(
            exchange="",
            routing_key=self.params.get("routing_key"),
            body=value,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            ),
        )
        self.connection.close()

    def size(self) -> int:
        pass
