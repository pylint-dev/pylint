# pylint: disable=missing-docstring, too-many-ancestors,too-few-public-methods
from typing import Generic, TypeVar

IN = TypeVar('IN', contravariant=True)
OUT = TypeVar('OUT', covariant=True)


class Service:
    pass


class ConsumingMixin(Generic[IN]):
    pass


class ProducingMixin(Generic[OUT]):
    pass


class StreamingMixin(Generic[IN, OUT], ConsumingMixin[IN], ProducingMixin[OUT]):
    pass


class Example(StreamingMixin[str, int], Service):
    pass


print(Example.__mro__)
