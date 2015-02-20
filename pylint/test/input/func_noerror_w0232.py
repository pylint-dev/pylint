# pylint: disable=R0903,R0923
"""check interface and exception without __init__ doesn't print warnings
"""
__revision__ = ''

class Interface:
    """interface without docstring"""

class MyError(Exception):
    """exception without docstring"""
