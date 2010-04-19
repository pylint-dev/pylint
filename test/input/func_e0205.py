# pylint: disable=R0903
"""check method hidding ancestor attribute
"""

__revision__ = ''

class Abcd:
    """dummy"""
    def __init__(self):
        self.abcd = 1

class Cdef(Abcd):
    """dummy"""
    def abcd(self):
        """test
        """
        print self
