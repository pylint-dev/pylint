"""test string exception
"""

__revision__ = ''

def function1():
    """hehehe"""
    raise "String Exception"

def function2():
    """hehehe"""
    raise 'exception', 'message'
