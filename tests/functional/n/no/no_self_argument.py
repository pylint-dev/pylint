"""Check for method without self as first argument"""
# pylint: disable=useless-object-inheritance
from __future__ import print_function

class NoSelfArgument(object):
    """dummy class"""

    def __init__(truc):  # [no-self-argument]
        """method without self"""
        print(1)

    def abdc(yoo):  # [no-self-argument]
        """another test"""
        print(yoo)

    def edf(self):
        """just another method"""
        print('yapudju in', self)
