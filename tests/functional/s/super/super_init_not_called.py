"""This should not emit a super-init-not-called warning. It previously did this, because
``next(node.infer())`` was used in that checker's logic and the first inferred node
was an Uninferable object, leading to this false positive."""
# pylint: disable=too-few-public-methods, missing-class-docstring

import ctypes


class Foo(ctypes.BigEndianStructure):
    """A class"""

    def __init__(self):
        ctypes.BigEndianStructure.__init__(self)


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
