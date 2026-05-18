# pylint: disable=missing-docstring, too-few-public-methods
from abc import ABCMeta, abstractmethod


class Cls:
    @property
    def a(self, arg):  # [property-with-parameters]
        return arg

    @property
    def b(self, arg, /):  # [property-with-parameters]
        return arg

    @property
    def c(self, *, arg):  # [property-with-parameters]
        return arg

    @property
    def d(self, *args):  # [property-with-parameters]
        return args

    @property
    def e(self, **kwargs):  # [property-with-parameters]
        return kwargs


class MyClassBase(metaclass=ABCMeta):
    """MyClassBase."""

    @property
    @abstractmethod
    def example(self):
        """Getter."""

    @example.setter
    @abstractmethod
    def example(self, value):
        """Setter."""
