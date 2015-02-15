"""test min methods"""
from __future__ import print_function
__revision__ = None

class Aaaa(object):
    """yo"""
    def __init__(self):
        pass
    def meth1(self):
        """hehehe"""
        print(self)
    def _dontcount(self):
        """not public"""
        print(self)


# Don't emit for these cases.
class Klass(object):
    """docstring"""

    def meth1(self):
        """first"""

    def meth2(self):
        """second"""


class EnoughPublicMethods(Klass):
    """We shouldn't emit too-few-public-methods for this."""

