"""check for method without self as first argument
"""
from __future__ import print_function
__revision__ = 0


class Abcd(object):
    """dummy class"""
    def __init__(self):
        pass

    def abcd(yoo):
        """another test"""

    abcd = classmethod(abcd)

    def edf(self):
        """justo ne more method"""
        print('yapudju in', self)
