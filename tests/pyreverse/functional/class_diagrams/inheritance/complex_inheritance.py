from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar


@dataclass
class AbstractParent(ABC):
    """parent class"""


@dataclass
class Child(AbstractParent):
    """child class"""


GenericType = TypeVar("GenericType")


class GenericParent(Generic[GenericType]):
    """parent class"""


class ConcreteChild(GenericParent[int]):
    """child class"""
