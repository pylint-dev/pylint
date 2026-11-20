# pylint: disable=missing-docstring,too-few-public-methods,disallowed-name,invalid-name,unused-argument
import abc


class SuperClass(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def prop(self):
        pass

    @abc.abstractmethod
    async def async_method(self):
        pass

    @abc.abstractmethod
    def method_a(self):
        pass

    @abc.abstractmethod
    def method_b(self):
        pass

class ValidDerived(SuperClass):
    @property
    def prop(self):
        return None

    async def async_method(self):
        return None

    def method_a(self):
        pass

    def method_b(self):
        pass

class InvalidDerived(SuperClass):
    def prop(self):  # [invalid-overridden-method]
        return None

    def async_method(self): # [invalid-overridden-method]
        return None

    @property
    def method_a(self): # [invalid-overridden-method]
        return None

    async def method_b(self): # [invalid-overridden-method]
        return None

class Property:

    @property
    def close(self):
        pass


class PropertySetter(Property):

    @property
    def close(self):
        pass

    @close.setter
    def close(self, attr):
        return attr

    @close.deleter
    def close(self):
        return None


class AbstractProperty:

    @property
    @abc.abstractmethod
    def prop(self):
        return


# https://github.com/pylint-dev/pylint/issues/4368
# Decrator functions with a nested property decorator should still be
# inferred as property.

def my_property(func):
    @property
    def _wrapper(self):
        pass
    return _wrapper

def not_a_property(func):
    def _wrapper(self):
        pass
    return _wrapper

def multiple_returns(func):
    def _wrapper(self):
        pass
    if foobar:  # pylint: disable=undefined-variable
        return False
    return _wrapper

class A:
    @property
    def foo(self):
        return True

    @property
    def bar(self):
        return True

    @property
    def bar2(self):
        return True

class B(A):
    @my_property
    def foo(self):
        return False

    @not_a_property
    def bar(self):  # [invalid-overridden-method]
        return False

    @multiple_returns
    def bar2(self):  # [invalid-overridden-method]
        return False


# https://github.com/pylint-dev/pylint/issues/8687
# A protocol property returning a Callable can be implemented by a method.
import collections.abc  # pylint: disable=wrong-import-position
from typing import (  # pylint: disable=wrong-import-position
    Callable, Optional, Protocol, Union, final
)


class CallableProto(Protocol):
    @property
    def fun(self) -> Callable[[int], None] | None: ...
    @property
    def fun_none_first(self) -> None | Callable[[int], None]: ...
    @property
    def fun_plain(self) -> Callable[[int], None]: ...
    @property
    def fun_abc(self) -> collections.abc.Callable[[int], None]: ...
    @property
    def fun_bare(self) -> Callable: ...
    @property
    def fun_optional(self) -> Optional[Callable[[int], None]]: ...
    @property
    def fun_union(self) -> Union[None, Callable[[int], None]]: ...
    @property
    def not_callable(self) -> int: ...
    @property
    def list_of_callables(self) -> list[Callable[[int], None]]: ...
    @property
    def unannotated(self): ...
    @property
    def fun_property(self) -> Callable[[int], None]: ...
    @property
    @final
    def fun_final(self) -> Callable[[int], None]: ...
    @property
    def fun_async(self) -> Callable[[int], None]: ...


class CallableImpl(CallableProto):
    def fun(self, i: int): ...
    def fun_none_first(self, i: int): ...
    def fun_plain(self, i: int): ...
    def fun_abc(self, i: int): ...
    def fun_bare(self, i: int): ...
    def fun_optional(self, i: int): ...
    def fun_union(self, i: int): ...
    def not_callable(self): ...  # [invalid-overridden-method]
    def list_of_callables(self, i: int): ...  # [arguments-differ, invalid-overridden-method]
    def unannotated(self, i: int): ...  # [arguments-differ, invalid-overridden-method]
    @property
    def fun_property(self) -> Callable[[int], None]: ...
    def fun_final(self, i: int): ...  # [overridden-final-method]
    async def fun_async(self, i: int): ...  # [invalid-overridden-method]


class CallableBase:
    @property
    def fun(self) -> Callable[[int], None]: ...


class CallableBaseImpl(CallableBase):
    def fun(self, i: int): ...  # [arguments-differ, invalid-overridden-method]
