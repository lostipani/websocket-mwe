import abc
from typing import Any, List


class NotImplementedError:
    pass


class Bus(object):
    """
    Bus classes have to feature the following methods:
        add
        size
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, data):
        self.data = data

    def __str__(self) -> str:
        return str(self.data)

    @staticmethod
    def factory(data):
        if isinstance(data, list):
            return BusList(data)
        else:
            raise NotImplementedError

    @abc.abstractmethod
    def add(self, value):
        pass

    @abc.abstractmethod
    def size(self):
        pass


class BusList(Bus):
    def __init__(self, data: List[Any]):
        super().__init__(data)

    def add(self, value: Any):
        self.data.append(value)

    def size(self) -> int:
        return len(self.data)
