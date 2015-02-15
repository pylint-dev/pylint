"""check different signatures"""
from __future__ import print_function
__revision__ = 0
# pylint: disable=too-few-public-methods
class Abcd(object):
    '''dummy'''
    def __init__(self):
        self.aarg = False
    def abcd(self, aaa=1, bbbb=None):
        """hehehe"""
        print(self, aaa, bbbb)
    def args(self):
        """gaarrrggll"""
        self.aarg = True

class Cdef(Abcd):
    """dummy"""
    def __init__(self, aaa):
        Abcd.__init__(self)
        self.aaa = aaa

    def abcd(self, aaa, bbbb=None):
        """hehehe"""
        print(self, aaa, bbbb)
