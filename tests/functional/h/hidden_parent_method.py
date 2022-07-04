# pylint: disable=too-few-public-methods, missing-class-docstring
"""Functional tests for hidden-parent-method."""
import typing

GrandparentT = typing.TypeVar("GrandparentT", "Grandparent")


class Grandparent:
    def __init__(self):
        pass

    def __repr__(self):
        return "I'm a grandparent"

    def __eq__(self, other):
        return NotImplemented


class Parent1(Grandparent):
    def __repr__(self):
        return "I'm parent 1"


class Parent2(Grandparent):
    def __repr__(self):
        return "I'm parent 2"


class Child1(Parent1, Parent2):  # [hidden-parent-method]
    pass


class Child2(Parent1, Parent2):
    def __repr__(self):
        return "no warning, because reimplemented completely"


class Child3(Parent1, Parent2):
    def __repr__(self):
        print("could warn, but not now--would need to determine if all paths delegate to super()")
        return super().__repr__()


class Child4(Parent1, Parent2):
    def __repr__(self):
        def nested():
            return super().__repr__()

        return nested()


class Child5(Parent1, typing.Generic[GrandparentT]):
    pass


class ListySet(list, set):
    pass


class HasClose:
    def close(self):
        """Example demonstrating better inheritance pattern"""


class Child6(HasClose):
    def close(self):
        print("Child6")
        super().close()


class Child7(HasClose):
    def close(self):
        print("Child7")
        super().close()


class Grandchild1(Child6, Child7):
    def close(self):
        """All paths delegate to super -- no warning"""
        print("Grandchild")
        super().close()


class Granchild2(Child6, Child7):
    """Same test, but without reimplementation -- no warning"""
