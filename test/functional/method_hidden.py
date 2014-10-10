# pylint: disable=too-few-public-methods,print-statement
"""check method hidding ancestor attribute
"""

class Abcd(object):
    """dummy"""
    def __init__(self):
        self.abcd = 1

class Cdef(Abcd):
    """dummy"""
    def abcd(self): # [method-hidden]
        """test
        """
        print self
