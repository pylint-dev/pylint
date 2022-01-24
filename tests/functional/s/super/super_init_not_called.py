"""Tests for super-init-not-called."""
# pylint: disable=too-few-public-methods

import ctypes


class Foo(ctypes.BigEndianStructure):
    """This class should not emit a super-init-not-called warning.

    It previously did, because ``next(node.infer())`` was used in that checker's logic
    and the first inferred node was an Uninferable object, leading to this false positive.
    """

    def __init__(self):
        ctypes.BigEndianStructure.__init__(self)


class UninferableChild(UninferableParent):  # [undefined-variable]
    """An implementation that test if we don't crash on uninferable parents."""

    def __init__(self):
        ...
