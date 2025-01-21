import abc
from typing import Any, List


class NotImplementedError:
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
    def factory(backend):
        if isinstance(backend, list):
            return BrokerList(backend)
        else:
            raise NotImplementedError

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
