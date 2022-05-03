# pylint: disable=missing-docstring,invalid-name,line-too-long,too-few-public-methods,use-list-literal,use-dict-literal, typevar-name-incorrect-variance
import typing
import collections
from typing import Generic, TypeVar


# tests/functional/a/assigning_non_slot.py
TYPE = TypeVar('TYPE')

class Cls(Generic[TYPE]):
    """ Simple class with slots """
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value


# tests/functional/d/dangerous_default_value_py30.py
def function4(value=set()): # [dangerous-default-value]
    """set is mutable and dangerous."""
    return value

def function5(value=frozenset()):
    """frozenset is immutable and safe."""
    return value

def function7(value=dict()): # [dangerous-default-value]
    """dict is mutable and dangerous."""
    return value

def function8(value=list()):  # [dangerous-default-value]
    """list is mutable and dangerous."""
    return value

def function17(value=collections.deque()):  # [dangerous-default-value]
    """mutable, dangerous"""
    return value

def function18(value=collections.ChainMap()):  # [dangerous-default-value]
    """mutable, dangerous"""
    return value

def function19(value=collections.Counter()):  # [dangerous-default-value]
    """mutable, dangerous"""
    return value

def function20(value=collections.OrderedDict()):  # [dangerous-default-value]
    """mutable, dangerous"""
    return value

def function21(value=collections.defaultdict()):  # [dangerous-default-value]
    """mutable, dangerous"""
    return value


# tests/functional/p/protocol_classes.py  (min py38)
T2 = typing.TypeVar("T2")

class HasherGeneric(typing.Protocol[T2]):
    """A hashing algorithm, e.g. :func:`hashlib.sha256`."""
    def update(self, blob: bytes):
        ...
    def digest(self) -> bytes:
        ...


# tests/functional/r/regression/regression_2443_duplicate_bases.py
IN = TypeVar('IN', contravariant=True)
OUT = TypeVar('OUT', covariant=True)

class ConsumingMixin(Generic[IN]):
    pass

class ProducingMixin(Generic[OUT]):
    pass

class StreamingMixin(Generic[IN, OUT], ConsumingMixin[IN], ProducingMixin[OUT]):
    pass
