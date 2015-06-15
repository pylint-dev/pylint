"""Test that we are emitting arguments-differ when the arguments are different."""
# pylint: disable=missing-docstring, too-few-public-methods

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

    def test(self, arg, **kwargs):
        pass

class VarargsChild(Varargs):

    def test(self, arg):
        pass


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
        super(Sub, self).__init__()

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

    def func(self, arg):
        super(StaticmethodChild2, self).func(arg)
