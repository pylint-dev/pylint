"""test local variable used before assignment
"""
from __future__ import print_function
__revision__ = 0

def function():
    """dummy"""
    print(aaaa)
    aaaa = 1
