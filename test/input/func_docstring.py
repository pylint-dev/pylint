# pylint: disable=R0201

__revision__ = ''

def function0():
    """"""

def function1(value):
    # missing docstring
    print value

def function2(value):
    """docstring"""
    print value

def function3(value):
    """docstring"""
    print value

class AAAA(object):
    # missing docstring

##     class BBBB:
##         # missing docstring
##         pass

##     class CCCC:
##         """yeah !"""
##         def method1(self):
##             pass

##         def method2(self):
##             """ yeah !"""
##             pass

    def method1(self):
        pass

    def method2(self):
        """ yeah !"""
        pass

    def method3(self):
        """"""
        pass

    def __init__(self):
        pass

class DDDD(AAAA):
    """yeah !"""

    def __init__(self):
        AAAA.__init__(self)

    def method2(self):
        """"""
        pass

    def method3(self):
        pass

    def method4(self):
        pass

# pylint: disable=missing-docstring
def function4():
    pass

# pylint: disable=empty-docstring
def function5():
    """"""
    pass
