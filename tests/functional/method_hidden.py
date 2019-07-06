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
