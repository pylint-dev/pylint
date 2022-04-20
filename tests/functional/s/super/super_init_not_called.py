"""Tests for super-init-not-called."""
# pylint: disable=too-few-public-methods, missing-class-docstring

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


# Tests for not calling the init of a parent that does not define one
# but inherits it.
class GrandParentWithInit:
    def __init__(self):
        print(self)


class ParentWithoutInit(GrandParentWithInit):
    pass


class ChildOne(ParentWithoutInit, GrandParentWithInit):
    """Since ParentWithoutInit calls GrandParentWithInit it doesn't need to be called."""

    def __init__(self):
        GrandParentWithInit.__init__(self)


class ChildTwo(ParentWithoutInit):
    def __init__(self):
        ParentWithoutInit.__init__(self)


class ChildThree(ParentWithoutInit):
    def __init__(self):  # [super-init-not-called]
        ...


# Regression test as reported in
# https://github.com/PyCQA/pylint/issues/6027
class MyUnion(ctypes.Union):
    def __init__(self):  # [super-init-not-called]
        pass
