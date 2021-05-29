"""Test that we are emitting arguments-differ when the arguments are different."""
# pylint: disable=missing-docstring, too-few-public-methods, unused-argument,useless-super-delegation, useless-object-inheritance, unused-private-member

class Parent(object):

    def test(self):
        pass


class Child(Parent):

    def test(self, arg):  # [arguments-differ]
        pass


class ParentDefaults(object):

    def test(self, arg=None, barg=None):
        pass

class ChildDefaults(ParentDefaults):

    def test(self, arg=None):  # [arguments-differ]
        pass


class Classmethod(object):

    @classmethod
    def func(cls, data):
        return data

    @classmethod
    def func1(cls):
        return cls


class ClassmethodChild(Classmethod):

    @staticmethod
    def func():  # [arguments-differ]
        pass

    @classmethod
    def func1(cls):
        return cls()


class Builtins(dict):
    """Ignore for builtins, for which we don't know the number of required args."""

    @classmethod
    def fromkeys(cls, arg, arg1):
        pass


class Varargs(object):

    def has_kwargs(self, arg, **kwargs):
        pass

    def no_kwargs(self, args):
        pass


class VarargsChild(Varargs):

    def has_kwargs(self, arg):  # [arguments-differ]
        "Not okay to lose capabilities. Also, type has changed."

    def no_kwargs(self, arg, **kwargs):  # [arguments-renamed]
        "Addition of kwargs does not violate LSP, but first argument's name has changed."


class Super(object):
    def __init__(self):
        pass

    def __private(self):
        pass

    def __private2_(self):
        pass

    def ___private3(self):
        pass

    def method(self, param):
        raise NotImplementedError


class Sub(Super):

    # pylint: disable=unused-argument
    def __init__(self, arg):
        super().__init__()

    def __private(self, arg):
        pass

    def __private2_(self, arg):
        pass

    def ___private3(self, arg):
        pass

    def method(self, param='abc'):
        pass


class Staticmethod(object):

    @staticmethod
    def func(data):
        return data


class StaticmethodChild(Staticmethod):

    @classmethod
    def func(cls, data):
        return data


class Property(object):

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


class StaticmethodChild2(Staticmethod):

    def func(self, data):
        super().func(data)


class SuperClass(object):

    @staticmethod
    def impl(arg1, arg2, **kwargs):
        return arg1 + arg2


class MyClass(SuperClass):

    def impl(self, *args, **kwargs):
        """
        Acceptable use of vararg in subclass because it does not violate LSP.
        """
        super().impl(*args, **kwargs)


class FirstHasArgs(object):

    def test(self, *args):
        pass


class SecondChangesArgs(FirstHasArgs):

    def test(self, first, second, *args):  # [arguments-differ]
        pass


class Positional(object):

    def test(self, first, second):
        pass


class PositionalChild(Positional):

    def test(self, *args):
        """
        Acceptable use of vararg in subclass because it does not violate LSP.
        """
        super().test(args[0], args[1])

class Mixed(object):

    def mixed(self, first, second, *, third, fourth):
        pass


class MixedChild1(Mixed):

    def mixed(self, first, *args, **kwargs):
        """
        Acceptable use of vararg in subclass because it does not violate LSP.
        """
        super().mixed(first, *args, **kwargs)


class MixedChild2(Mixed):

    def mixed(self, first, *args, third, **kwargs):
        """
        Acceptable use of vararg in subclass because it does not violate LSP.
        """
        super().mixed(first, *args, third, **kwargs)


class HasSpecialMethod(object):

    def __getitem__(self, key):
        return key


class OverridesSpecialMethod(HasSpecialMethod):

    def __getitem__(self, cheie):
        # no error here, method overrides special method
        return cheie + 1


class ParentClass(object):

    def meth(self, arg, arg1):
        raise NotImplementedError


class ChildClass(ParentClass):

    def meth(self, _arg, dummy):
        # no error here, "dummy" and "_" are being ignored if
        # spotted in a variable name (declared in dummy_parameter_regex)
        pass


# https://github.com/PyCQA/pylint/issues/4443
# Some valid overwrites with type annotations

import typing  # pylint: disable=wrong-import-position
from typing import Dict  # pylint: disable=wrong-import-position

class ParentT1:
    def func(self, user_input: Dict[str, int]) -> None:
        pass

class ChildT1(ParentT1):
    def func(self, user_input: Dict[str, int]) -> None:
        pass

class ParentT2:
    async def func(self, user_input: typing.List) -> None:
        pass

class ChildT2(ParentT2):
    async def func(self, user_input: typing.List) -> None:
        pass

class FooT1:
    pass

class ParentT3:
    def func(self, user_input: FooT1) -> None:
        pass

class ChildT3(ParentT3):
    def func(self, user_input: FooT1) -> None:
        pass

# Keyword and positional overriddes
class AbstractFoo:

    def kwonly_1(self, first, *, second, third):
        "Normal positional with two positional only params."

    def kwonly_2(self, *, first, second):
        "Two positional only parameter."

    def kwonly_3(self, *, first, second):
        "Two positional only params."

    def kwonly_4(self, *, first, second=None):
        "One positional only and another with a default."

    def kwonly_5(self, *, first, **kwargs):
        "Keyword only and keyword variadics."

    def kwonly_6(self, first, second, *, third):
        "Two positional and one keyword"


class Foo(AbstractFoo):

    def kwonly_1(self, first, *, second):  # [arguments-differ]
        "One positional and only one positional only param."

    def kwonly_2(self, *, first):  # [arguments-differ]
        "Only one positional parameter instead of two positional only parameters."

    def kwonly_3(self, first, second):  # [arguments-differ]
        "Two positional params."

    def kwonly_4(self, first, second):  # [arguments-differ]
        "Two positional params."

    def kwonly_5(self, *, first):  # [arguments-differ]
        "Keyword only, but no variadics."

    def kwonly_6(self, *args, **kwargs):  # valid override
        "Positional and keyword variadics to pass through parent params"


class Foo2(AbstractFoo):

    def kwonly_6(self, first, *args, **kwargs):  # valid override
        "One positional with the rest variadics to pass through parent params"
