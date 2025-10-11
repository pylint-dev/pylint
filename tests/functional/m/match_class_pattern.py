# pylint: disable=missing-docstring,unused-variable,too-few-public-methods
# pylint: disable=match-class-positional-attributes

from typing import NamedTuple

# -- Check __match_args__ definitions --
class A:
    __match_args__ = ("x",)

class B(A):
    __match_args__ = ("x", "y")

class C:
    __match_args__ = ["x", "y"]  # [invalid-match-args-definition]

class D:
    __match_args__ = ("x", 1)  # [invalid-match-args-definition]

class E:
    def f(self):
        __match_args__ = ["x"]


class Result(NamedTuple):
    # inherits from tuple -> match self
    x: int
    y: int


def f1(x):
    """Check too many positional sub-patterns"""
    match x:
        case A(1): ...
        case A(1, 2): ...  # [too-many-positional-sub-patterns]
        case B(1, 2): ...
        case B(1, 2, 3): ...  # [too-many-positional-sub-patterns]
        case int(1): ...
        case int(1, 2): ...  # [too-many-positional-sub-patterns]
        case tuple(1): ...
        case tuple(1, 2): ...  # [too-many-positional-sub-patterns]
        case tuple((1, 2)): ...
        case Result(1, 2): ...

def f2(x):
    """Check multiple sub-patterns for attribute"""
    match x:
        case A(1, x=1): ...  # [multiple-class-sub-patterns]
        case A(1, y=1): ...
        case A(x=1, x=2, x=3): ...  # [multiple-class-sub-patterns]

        # with invalid __match_args__ we can't detect duplicates with positional patterns
        case D(1, x=1): ...

        # If class name is undefined, we can't get __match_args__
        case NotDefined(1, x=1): ...  # [undefined-variable]

def f3(x):
    """Check class pattern with name binding to self."""
    match x:
        case int(y): ... # [match-class-bind-self]
        case int() as y: ...
        case int(2 as y): ...
        case str(y): ...   # [match-class-bind-self]
        case str() as y: ...
        case str("Hello" as y): ...
        case tuple(y, 2): ...  # pylint: disable=too-many-positional-sub-patterns
        case tuple((y, 2)): ...

def f4(x):
    """Check for positional attributes if keywords could be used."""
    # pylint: enable=match-class-positional-attributes
    match x:
        case int(2): ...
        case bool(True): ...
        case A(1): ...  # [match-class-positional-attributes]
        case A(x=1): ...
        case B(1, 2): ...  # [match-class-positional-attributes]
        case B(x=1, y=2): ...
        case Result(1, 2): ...
        case Result(x=1, y=2): ...
