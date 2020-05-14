# pylint: disable=missing-docstring, too-few-public-methods
from abc import ABCMeta, abstractproperty


class Cls:
    @property
    def attribute(self, param, param1): # [property-with-parameters]
        return param + param1


class MyClassBase(metaclass=ABCMeta):
    """MyClassBase."""

    @abstractproperty
    def example(self):
        """Getter."""

    @abstractproperty
    @example.setter
    def example(self, value):
        """Setter."""
