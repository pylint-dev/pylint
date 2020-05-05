# pylint: disable=too-few-public-methods,print-statement, useless-object-inheritance,missing-docstring
"""check method hidding ancestor attribute
"""
from __future__ import print_function

class Abcd(object):
    """dummy"""
    def __init__(self):
        self.abcd = 1

class Cdef(Abcd):
    """dummy"""
    def abcd(self): # [method-hidden]
        """test
        """
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

    def one(self): # [method-hidden]
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
