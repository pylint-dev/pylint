"""Tests for super-init-not-called."""
# pylint: disable=too-few-public-methods

import ctypes

from typing_extensions import Protocol as ExtensionProtocol


class Foo(ctypes.BigEndianStructure):
    """This class should not emit a super-init-not-called warning.

    It previously did, because ``next(node.infer())`` was used in that checker's logic
    and the first inferred node was an Uninferable object, leading to this false positive.
    """

    def __init__(self):
        ctypes.BigEndianStructure.__init__(self)


class TestProto(ExtensionProtocol):
    """A protocol without __init__ using Protocol from typing_extensions."""


class TestParent(TestProto):
    """An implementation."""

    def __init__(self):
        ...


class TestChild(TestParent):
    """An implementation which should call the init of TestParent."""

    def __init__(self):  # [super-init-not-called]
        ...


class UninferableChild(UninferableParent):  # [undefined-variable]
    """An implementation that test if we don't crash on uninferable parents."""

    def __init__(self):
        ...
