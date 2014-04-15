"""Test Pylint's use of __all__.

* NonExistant is not defined in this module, and it is listed in
  __all__. An error is expected.

* This module imports path and republished it in __all__. No errors
  are expected.
"""
#  pylint: disable=R0903,R0201,W0612

__revision__ = 0

from os import path
from collections import deque

__all__ = [
    'Dummy',
    'NonExistant',
    'path',
    'func',
    'inner',
    'InnerKlass', deque.__name__]


class Dummy(object):
    """A class defined in this module."""
    pass

DUMMY = Dummy()

def function():
    """Function docstring
    """
    pass

function()

class Klass(object):
    """A klass which contains a function"""
    def func(self):
        """A klass method"""
        inner = None

    class InnerKlass(object):
        """A inner klass"""
        pass
