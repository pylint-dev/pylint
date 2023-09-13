# pylint: disable=too-few-public-methods,missing-docstring,invalid-name
"""test detection of method which could be a function"""
from abc import ABC, abstractmethod
from typing import Protocol, overload


class Toto:
    """bla bal abl"""

    def __init__(self):
        self.aaa = 2

    def regular_method(self):
        """this method is a real method since it access to self"""
        self.function_method()

    def function_method(self):  # [no-self-use]
        """this method isn' a real method since it doesn't need self"""
        print('hello')

    async def async_regular_method(self):
        """this async method is a real method since it accesses self"""
        await self.async_function_method()

    async def async_function_method(self):  # [no-self-use]
        """this async method isn't a real method since it doesn't need self"""
        print('hello')

class Base:
    """an abstract class"""

    def __init__(self):
        self.aaa = 2

    def check(self, arg):
        """an abstract method, could not be a function"""
        raise NotImplementedError


class Sub(Base):
    """a concrete class"""

    def check(self, arg):
        """a concrete method, could not be a function since it need
        polymorphism benefits
        """
        return arg == 0

class Super:
    """same as before without abstract"""
    attr = 1
    def method(self):
        """regular"""
        print(self.attr)

class Sub1(Super):
    """override method with need for self"""
    def method(self):
        """no i can not be a function"""
        print(42)

    def __len__(self):
        """no i can not be a function"""
        return 42

    def __cmp__(self, other):
        """no i can not be a function"""
        print(42)

    def __copy__(self):
        return 24

    def __getstate__(self):
        return 42


class Prop:

    @property
    def count(self):
        """Don't emit no-self-use for properties.

        They can't be functions and they can be part of an
        API specification.
        """
        return 42


class A:
    def __init__(self):
        self.store = {}

    def get(self, key, default=None):
        return self.store.get(key, default)

class B(A):
    def get_memo(self, obj):
        return super().get(obj)


class C:
    def a(self, /):  # [no-self-use]
        ...

    # Disable with old error code
    # pylint: disable=use-symbolic-message-instead
    def b(self, /):  # pylint: disable=R0201
        ...


def func_a(self):  # pylint: disable=unused-argument
    pass


class Foo1(ABC):
    """Don't emit no-self-use for abstract methods."""

    @abstractmethod
    def a(self):
        pass

    def b(self):
        raise NotImplementedError

    def c(self):
        pass  # pass counts as abstract


class Foo2(Protocol):
    """Don't emit no-self-use for methods in Protocol classes."""

    def a(self):
        ...

class Foo3:
    """Don't emit no-self-use for overload methods."""

    @overload
    def a(self, var): ...

    @overload
    def a(self, var): ...

    def a(self, var):
        pass


class Foo4:
    """Other false positive cases."""

    @staticmethod
    def a(self):  # pylint: disable=unused-argument,bad-staticmethod-argument
        ...

    @staticmethod
    def b():
        ...

    @classmethod
    def c(self):  # pylint: disable=bad-classmethod-argument
        ...

    def d():  # pylint: disable=no-method-argument
        ...
