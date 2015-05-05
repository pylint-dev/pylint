# pylint: disable=R0903
"""check interface and exception without __init__ doesn't print warnings
"""
__revision__ = ''

class MyError(Exception):
    """exception without docstring"""
