# pylint: disable=missing-docstring
from abc import ABCMeta, abstractmethod


class Cls(metaclass=ABCMeta):
    def __init__(self):
        pass

    @property
    @abstractmethod
    def values(self):
        pass

    @classmethod
    def some_method(cls):
        return cls.values.issubset({2, 3})


class Subcls(Cls):
    values = {1, 2, 3}
