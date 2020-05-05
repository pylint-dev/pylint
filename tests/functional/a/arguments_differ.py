"""Test that we are emitting arguments-differ when the arguments are different."""
# pylint: disable=missing-docstring, too-few-public-methods, unused-argument,useless-super-delegation, useless-object-inheritance

class Parent(object):

    def test(self):
        pass


class Child(Parent):

    def test(self, arg): # [arguments-differ]
        pass


class ParentDefaults(object):

    def test(self, arg=None, barg=None):
        pass

class ChildDefaults(ParentDefaults):

    def test(self, arg=None): # [arguments-differ]
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
    def func(): # [arguments-differ]
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

    def has_kwargs(self, arg): # [arguments-differ]
        "Not okay to lose capabilities."

    def no_kwargs(self, arg, **kwargs): # [arguments-differ]
        "Not okay to add extra capabilities."


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

    def test(self, first, second, *args): # [arguments-differ]
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
        return cheie + 1


class ParentClass(object):

    def meth(self, arg, arg1):
        raise NotImplementedError


class ChildClass(ParentClass):

    def meth(self, _arg, dummy):
        pass
