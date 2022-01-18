"""Tests for super-init-not-called."""
# pylint: disable=too-few-public-methods

import ctypes
from abc import abstractmethod
from typing import Protocol

from typing_extensions import Protocol as ExtensionProtocol


# This should not emit a super-init-not-called warning. It previously did this, because
# ``next(node.infer())`` was used in that checker's logic and the first inferred node
# was an Uninferable object, leading to this false positive.
class Foo(ctypes.BigEndianStructure):
    """A class"""

    def __init__(self):
        ctypes.BigEndianStructure.__init__(self)


class MyProtocol(Protocol):
    """A protocol."""

    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError


class ProtocolImplimentation(MyProtocol):
    """An implementation."""

    def __init__(self) -> None:
        ...


class TestProto(ExtensionProtocol):
    """A protocol without __init__ using Protocol from typing_extensions."""


class TestParent(TestProto):
    """An implementation."""

    def __init__(self):
        ...


class TestChild(TestParent):
    """An implementation which should could the init of TestParent."""

    def __init__(self):  # [super-init-not-called]
        ...
