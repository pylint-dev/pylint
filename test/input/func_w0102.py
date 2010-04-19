# pylint: disable=R0201
"""docstring"""
__revision__ = ''

class AAAA:
    """docstring"""
    def __init__(self):
        pass
    def method1(self):
        """docstring"""
        
    def method2(self):
        """docstring"""
        
    def method2(self):
        """docstring"""

class AAAA:
    """docstring"""
    def __init__(self):
        pass
    def yeah(self):
        """hehehe"""
    def yoo(self):
        """yoo""" 
def func1():
    """docstring"""
    
def func2():
    """docstring"""
    
def func2():
    """docstring"""
    __revision__ = 1    
    return __revision__ 

if __revision__:
    def exclusive_func():
        "docstring"
else:
    def exclusive_func():
        "docstring"

try:
    def exclusive_func2():
        "docstring"
except TypeError:
    def exclusive_func2():
        "docstring"
else:
    def exclusive_func2():
        "this one redefine the one defined line 42"


def with_inner_function_1():
    """docstring"""
    def callback():
        """callback docstring"""
        pass
    return callback

def with_inner_function_2():
    """docstring"""
    def callback():
        """does not redefine callback returned by with_inner_function_1"""
        pass
    return callback
