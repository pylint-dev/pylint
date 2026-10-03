"""Tests for super-init-not-called."""
# pylint: disable=too-few-public-methods, missing-class-docstring

import abc
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
# https://github.com/pylint-dev/pylint/issues/6027
class MyUnion(ctypes.Union):
    def __init__(self):
        pass


# Should not be called on abstract __init__ methods
# https://github.com/pylint-dev/pylint/issues/3975
class Base:
    def __init__(self, param: int, param_two: str) -> None:
        raise NotImplementedError()


class Derived(Base):
    def __init__(self, param: int, param_two: str) -> None:
        self.param = param + 1
        self.param_two = param_two[::-1]


class AbstractBase(abc.ABC):
    def __init__(self, param: int) -> None:
        self.param = param + 1

    def abstract_method(self) -> str:
        """This needs to be implemented."""
        raise NotImplementedError()


class DerivedFromAbstract(AbstractBase):
    def __init__(self, param: int) -> None:  # [super-init-not-called]
        print("Called")

    def abstract_method(self) -> str:
        return "Implemented"


class DerivedFrom(UnknownParent):  # [undefined-variable]
    def __init__(self) -> None:
        print("Called")


class DerivedFromUnknownGrandparent(DerivedFrom):
    def __init__(self) -> None:
        DerivedFrom.__init__(self)
