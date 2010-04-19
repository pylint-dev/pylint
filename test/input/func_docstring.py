# pylint: disable=R0201

__revision__ = ''

def function1(value):
    # missing docstring
    print value

def function2(value):
    """docstring"""
    print value

def function3(value):
    """docstring"""
    print value

class AAAA:
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

    def __init__(self):
        pass
    
class DDDD(AAAA):
    """yeah !"""

    def __init__(self):
        AAAA.__init__(self)
 
