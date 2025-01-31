import abc
from queue import Queue
from typing import Any, Callable, List
import pika


class BrokerNotImplementedError:
    pass


Value = Any


class Broker(object):
    """
    Abstract methods to be implemented:
        add
        get
        is_empty

    This base class is equipped with a factory method to instantiate the
    proper derived class depending on the chosen backend.

    Args
        backend: an instance of the Value container
    Raises
        BrokerNotImplementedError
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
        if isinstance(backend, Queue):
            return BrokerQueue(backend)
        elif isinstance(backend, str) and backend.lower() == "rabbitmq":
            return BrokerRabbitMQ(**kwargs)
        else:
            raise BrokerNotImplementedError

    @abc.abstractmethod
    def add(self, value: Value, **kwargs):
        pass

    @abc.abstractmethod
    def get(self, **kwargs) -> Value:
        pass

    @abc.abstractmethod
    def is_empty(self) -> bool:
        pass


class BrokerList(Broker):

    def __init__(self, backend: List[Value]):
        super().__init__(backend)

    def add(self, value: Value, **kwargs):
        del kwargs
        self.backend.append(value)

    def get(self, **kwargs) -> Value:
        del kwargs
        return self.backend[-1]

    def is_empty(self) -> bool:
        return len(self.backend) == 0


class BrokerQueue(Broker):

    def __init__(self, backend: Queue):
        super().__init__(backend)

    def add(self, value: Value, **kwargs):
        del kwargs
        self.backend.put(value)

    def get(self, **kwargs) -> Value:
        del kwargs
        return self.backend.get()

    def is_empty(self) -> bool:
        return self.backend.empty()


class BrokerRabbitMQ(Broker):

    def __init__(self, **kwargs):
        super().__init__("rabbitmq")
        self.params = kwargs
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.params.get("host"))
        )
        self.channel = self.connection.channel()

    def add(self, value: Value, **kwargs):
        del kwargs
        self.channel.queue_declare(queue=self.params.get("queue"))
        self.channel.basic_publish(
            exchange=self.params.get("exchange"),
            routing_key=self.params.get("routing_key"),
            body=value,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            ),
        )

    def get(self, **kwargs) -> Value:
        callback: Callable = kwargs["callback"]
        self.channel.queue_declare(queue=self.params.get("queue"))
        self.channel.basic_consume(
            queue=self.params.get("queue"),
            on_message_callback=callback,
            auto_ack=True,
        )
        self.channel.start_consuming()

    def is_empty(self) -> bool:
        queue = self.channel.queue_declare(
            queue=self.params.get("queue"), passive=True
        )
        return queue.method.message_count == 0
