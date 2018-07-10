# pylint: disable=too-few-public-methods,print-statement, useless-object-inheritance
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
