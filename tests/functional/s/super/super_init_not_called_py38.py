"""Tests for super-init-not-called with Protocol."""
# pylint: disable=too-few-public-methods

from abc import abstractmethod
from typing import Protocol


class MyProtocol(Protocol):
    """A protocol."""

    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError


class ProtocolImplimentation(MyProtocol):
    """An implementation."""

    def __init__(self) -> None:
        ...
