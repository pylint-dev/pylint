# pylint: disable=missing-docstring,unused-variable,too-few-public-methods

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


def f1(x):
    """Check too many positional sub-patterns"""
    match x:
        case A(1): ...
        case A(1, 2): ...  # [too-many-positional-sub-patterns]
        case B(1, 2): ...
        case B(1, 2, 3): ...  # [too-many-positional-sub-patterns]

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
