"""Errors for invalid slice indices"""

__revision__ = 0

TESTLIST = [1, 2, 3]

def function1():
    """functions used as indices"""
    return TESTLIST[id:id:]

def function2():
    """strings used as indices"""
    return TESTLIST['0':'1':]

def function3():
    """class without __index__ used as index"""

    class NoIndexTest(object): # pylint: disable=too-few-public-methods
        """Class with no __index__ method"""
        pass

    return TESTLIST[NoIndexTest()::]

def function4():
    """integers used as indices"""
    return TESTLIST[0:0:0] # no error

def function5():
    """None used as indicies"""
    return TESTLIST[None:None:None]

def function6():
    """class with __index__ used as index"""
    class IndexTest(object): # pylint: disable=too-few-public-methods
        """Class with __index__ method"""
        def __index__(self): # pylint: disable=no-self-use
            """Allow objects of this class to be used as slice indices"""
            return 0

    return TESTLIST[IndexTest():None:None] # no error
