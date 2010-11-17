# pylint: disable=R0903,R0201
"""test Invalid name"""

__revision__ = 1

def Run():
    """method without any good name"""
    class B:
        """nested class should not be tested has a variable"""
        def __init__(self):
            pass
    bBb = 1
    return A, bBb

def run():
    """anothrer method without only good name"""
    class Aaa:
        """nested class should not be tested has a variable"""
        def __init__(self):
            pass
    bbb = 1
    return Aaa(bbb)

A = None

def HOHOHOHO():
    """yo"""
    HIHIHI = 1
    print HIHIHI

class xyz: 
    """yo"""
    def __init__(self):
        pass

    def Youplapoum(self):
        """bad method name"""


def no_nested_args(arg1, arg21, arg22):
    """a function which had nested arguments but no more"""
    print arg1, arg21, arg22


GOOD_CONST_NAME = ''
benpasceluila = 0

class Correct: 
    """yo"""
    def __init__(self):
        self.cava = 12
        self._Ca_va_Pas = None

V = [WHAT_Ever_inListComp for WHAT_Ever_inListComp in GOOD_CONST_NAME]
