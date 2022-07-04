# pylint: disable=too-few-public-methods, missing-class-docstring
"""Functional tests for order-dependent-resolution and order-dependent-super-resolution."""
import typing
GrandparentT = typing.TypeVar('GrandparentT', 'Grandparent')

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


class Child1(Parent1, Parent2):  # [order-dependent-resolution]
    pass


class Child2(Parent1, Parent2):
    def __repr__(self):
        return "no warning, because reimplemented completely"


class Child3(Parent1, Parent2):
    def __repr__(self):
        print("warn, because calls super(), which is order-dependent")
        return super().__repr__()  # [order-dependent-super-resolution]


class Child4(Parent1, Parent2):
    def __repr__(self):
        def nested():
            return super().__repr__()
        return nested()


class Child5(Parent1, typing.Generic[GrandparentT]):
    pass


class ListySet(list, set):
    pass
