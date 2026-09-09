# pylint: disable=missing-docstring, invalid-name, too-few-public-methods

from dataclasses import dataclass
from typing import Protocol


def some_func():
    pass


def decorate(func):
    """Decorate *fn* to return ``self`` to enable chained method calls."""
    def wrapper(self, *args, **kw):
        func(self, *args, **kw)
        return 42
    return wrapper


class Class:

    def some_method(self):
        pass

    @decorate
    def some_other_decorated_method(self):
        pass

    def some_other_method(self):
        value = self.some_method()  # [assignment-from-no-return]
        other_value = self.some_other_decorated_method()
        return value + other_value


VALUE = some_func() # [assignment-from-no-return]
FUNCTIONS = [some_func]
VALUE_FROM_SUBSCRIPT = FUNCTIONS[0]()  # [assignment-from-no-return]


class Parent:
    """Parent class"""

    def compute(self):
        """This isn't supported by all child classes"""

        raise ValueError('Not supported for this object')

    def test(self):
        """Test"""

        result = self.compute()
        return result


class Child(Parent):
    """Child class"""

    def compute(self):
        """This is supported for this child class"""

        return 42


# Regression test for https://github.com/pylint-dev/pylint/issues/4220
class A:
    """Parent class"""
    def f(self):
        """This returns something"""
        return 42


class B(A):
    """Child class"""
    def __init__(self):
        self.a = A()
        result = self.a.f()  # no error here
        print(result)

    def f(self):
        """This doesn't return anything"""


res = B().a.f()  # no error here


# Regression test for https://github.com/pylint-dev/pylint/issues/11114
# A function whose body ends in an unconditional raise never returns normally,
# even when other statements precede the raise (e.g. pathlib.Path.readlink()
# on platforms without symlink support).
class Unsupported:
    """Class with a method that always raises"""

    def readlink(self):
        """Always raises, so assigning its result is not an error"""
        message = f"{type(self).__name__}.readlink() is unsupported"
        raise OSError(message)


link = Unsupported().readlink()  # no error here


# A trailing raise does not make the function no-return if an earlier branch
# can still return: here the bare return yields None, which is still reported.
def early_return_then_raise(value):
    """Returns on one branch, otherwise raises"""
    if value:
        return
    raise ValueError(value)


maybe = early_return_then_raise(None)  # [assignment-from-none]


# Methods of a Protocol and functions whose body is only ``...`` are stubs
# declaring what to implement, not functions returning nothing.
# Regression test for https://github.com/pylint-dev/pylint/issues/9080
class Blah(Protocol):
    """A protocol"""

    def do_thing(self) -> str:
        """Declares the method without implementing it"""
        ...


class Overridable:
    """A base class whose method is meant to be overridden"""

    def do_thing(self): ...

    def really_returns_nothing(self):
        """A body that does something and returns None"""
        print(self)


@dataclass
class BlahUser:
    """Holds a protocol implementation and a base class instance"""

    blah: Blah
    overridable: Overridable

    def do_thing_with_blah(self):
        """No message for the stubs, one for the real method"""
        value = self.blah.do_thing()
        other = self.overridable.do_thing()
        nothing = self.overridable.really_returns_nothing()  # [assignment-from-no-return]
        return value, other, nothing
