"""https://github.com/pylint-dev/pylint/issues/3675"""


def noop(x):  # pylint: disable=invalid-name
    """Return value unchanged"""
    return x


def add(x, y):  # pylint: disable=invalid-name
    """Add two values"""
    return x + y


def main(param):
    """Should not emit too-many-function-args"""
    tmp = noop  # matched first
    if param == 0:
        tmp = add
    return tmp(1, 1.01)


# Negative case, see `_check_isinstance_args` in `./pylint/checkers/typecheck.py`
isinstance(1, int, int) # [too-many-function-args]
isinstance(1, 1, int) # [too-many-function-args, isinstance-second-argument-not-valid-type]

# Check if respecting Python's actual runtime MRO when using metaclasses
class Meta(type):
    """Metaclass with a __call__ method that takes more arguments than the class it creates."""
    def __call__(cls, a: int, b: int, c: int) -> "MyClass":
        """Calls the class __call__ with the first argument."""
        return super().__call__(a)


class MyClass(metaclass=Meta): # pylint: disable=too-few-public-methods
    """Class with a __init__ method that takes fewer arguments than the metaclass __call__."""
    def __init__(self, a: str) -> None:
        """Initializes the class."""
        self.a = a
        self.b = None


MyClass(1, 2, 3, 4) # [too-many-function-args]
MyClass(1, 2, 3)
