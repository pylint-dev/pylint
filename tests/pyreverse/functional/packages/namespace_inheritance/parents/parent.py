from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar


@dataclass
class AbstractParent(ABC):
    """Parent class."""


GenericType = TypeVar("GenericType")


class GenericParent(Generic[GenericType]):
    """Parent class."""
