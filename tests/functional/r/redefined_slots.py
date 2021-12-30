"""Checks that a subclass does not redefine a slot which has been defined in a parent class."""

# pylint: disable=too-few-public-methods


class Base:
    """Class defining the `a`, `b` & `c` slots"""
    __slots__ = ("a", "b", "c")


class Subclass1(Base):
    """Redefining the `a` slot & adding the `d` & `e` slots"""
    __slots__ = ("a", "d", "e")  # [redefined-slots-in-subclass]


class Subclass2(Base):
    """Adding the `f`, `g` & `h` slots"""
    __slots__ = ("f", "g", "h")


class Base2:
    """Class defining the `i`, `j` & `k` slots"""
    __slots__ = ("i", "j", "k")


class Subclass3(Base, Base2):
    """Adding the `l`, `m`, `n` slots
       Redefining the `a`, `b`, & `c` slot already defined in `Base`
       Redefining the `i`, `j`, `k` slot already defined in `Base2`
    """
    __slots__ = ("a", "b", "c", "i", "j", "k", "l", "m", "n")  # [redefined-slots-in-subclass]
