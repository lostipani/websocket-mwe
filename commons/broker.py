import abc
from typing import Any, Callable, List
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

    def __init__(self, backend: Any):
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
        self.channel = self.connection.channel()

    def size(self) -> int:
        pass

    def add(self, value: Any):
        self.channel.queue_declare(queue=self.params.get("queue"))
        self.channel.basic_publish(
            exchange=self.params.get("exchange"),
            routing_key=self.params.get("routing_key"),
            body=value,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            ),
        )

    def get(self, callback: Callable) -> Any:
        self.channel.queue_declare(queue=self.params.get("queue"))
        self.channel.basic_consume(
            queue=self.params.get("queue"),
            on_message_callback=callback,
            auto_ack=True,
        )
        self.channel.start_consuming()
