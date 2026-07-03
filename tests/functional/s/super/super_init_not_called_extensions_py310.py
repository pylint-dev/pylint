"""Tests for super-init-not-called."""
# pylint: disable=too-few-public-methods

from typing_extensions import Protocol as ExtensionProtocol


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
