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
