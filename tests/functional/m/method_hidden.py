# pylint: disable=too-few-public-methods,missing-docstring
# pylint: disable=unused-private-member
# pylint: disable=super-init-not-called
"""check method hiding ancestor attribute
"""
from functools import cached_property
import functools as ft
import something_else as functools  # pylint: disable=import-error


class Abcd:
    """dummy"""

    def __init__(self):
        self.abcd = 1


class Cdef(Abcd):
    """dummy"""

    def abcd(self):  # [method-hidden]
        """test"""
        print(self)


class AbcdMixin:
    def abcd(self):
        pass


class Dabc(AbcdMixin, Abcd):
    def abcd(self):
        pass


class CustomProperty:
    """dummy"""

    def __init__(self, _):
        pass

    def __get__(self, obj, __):
        if not obj:
            return self
        return 5

    def __set__(self, _, __):
        pass


class Ddef:
    """dummy"""

    def __init__(self):
        self.five = "five"

    @CustomProperty
    def five(self):
        """Always 5."""
        return self


def my_decorator(*args, **kwargs):
    return CustomProperty(*args, **kwargs)


class Foo:
    def __init__(self):
        self._bar = 42
        self._baz = 84

    @my_decorator
    def method(self):  # E0202
        return self._baz

    @method.setter
    def method(self, value):
        self._baz = value

    def do_something_with_baz(self, value):
        self.method = value


class One:
    def __init__(self, one=None):
        if one is not None:
            self.one = one

    def one(self):  # [method-hidden]
        pass


class Two(One):
    def one(self):
        pass


try:
    import unknown as js
except ImportError:
    import json as js


class JsonEncoder(js.JSONEncoder):
    # pylint: disable=useless-super-delegation,super-with-arguments
    def default(self, o):
        return super(JsonEncoder, self).default(o)


class Parent:
    def __init__(self):
        self._protected = None
        self._protected_two = None


class Child(Parent):
    def _protected(self):  # [method-hidden]
        pass


class CachedChild(Parent):
    @ft.cached_property
    def _protected(self):
        pass

    @functools.cached_property
    def _protected_two(self):
        pass


class CachedChildFromImport(Parent):
    @cached_property
    def _protected(self):
        pass


class ParentTwo:
    def __init__(self):
        self.__private = None


class ChildTwo(ParentTwo):
    def __private(self):
        pass


class ChildHidingAncestorAttribute(Parent):
    @functools().cached_property
    def _protected(self):
        pass


class BuiltinNameAncestor:
    def __init__(self):
        self.help = None
        self.format = None


class BuiltinNameChild(BuiltinNameAncestor):
    def help(self):  # [method-hidden]
        pass

    def format(self):  # [method-hidden]
        pass


class BuiltinNameSameClass:
    """``object`` is an implicit ancestor, so no base class is needed."""

    def __init__(self):
        self.license = 1

    def license(self):  # [method-hidden]
        return self.license


def color():
    """A module level function unrelated to the class below."""


class ModuleFunctionNameAncestor:
    def __init__(self):
        self.color = None


class ModuleFunctionNameChild(ModuleFunctionNameAncestor):
    def color(self):  # [method-hidden]
        pass


class InitAssignsAttribute:
    def __init__(self, func):
        self.func = func


class OverridesInitWithoutCallingSuper(InitAssignsAttribute):
    """`__init__` never runs `InitAssignsAttribute.__init__`, so `func` is
    never actually hidden."""

    def __init__(self):
        pass

    def func(self, arg):
        print(arg)


class OverridesInitCallingSuper(InitAssignsAttribute):
    def __init__(self):
        super().__init__(None)

    def func(self, arg):  # [method-hidden]
        print(arg)


class OverridesInitCallingAncestorExplicitly(InitAssignsAttribute):
    """Calls the ancestor's `__init__` by name rather than via `super()`, so the
    assignment does run and the method really is hidden."""

    def __init__(self):
        InitAssignsAttribute.__init__(self, None)

    def func(self, arg):  # [method-hidden]
        print(arg)


class OverridesInitCallingSomethingElse(InitAssignsAttribute):
    """`__init__` calls something that is not an `__init__`, so the ancestor's
    assignment still never runs and the method is not hidden."""

    def __init__(self):
        print("not an init call")

    def func(self, arg):
        print(arg)
