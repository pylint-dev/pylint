"""Errors for invalid sequence indices"""

__revision__ = 0

TESTLIST = [1, 2, 3]
TESTTUPLE = (1, 2, 3)
TESTSTR = '123'

def function1():
    """list index is a function"""
    return TESTLIST[id]

def function2():
    """list index is a str constant"""
    return TESTLIST['0']

def function3():
    """list index is None"""
    return TESTLIST[None]

def function4():
    """list index is a float expression"""
    return TESTLIST[float(0)]

def function5():
    """list index is an int constant"""
    return TESTLIST[0]  # no error

def function6():
    """list index is a integer expression"""
    return TESTLIST[int(0.0)] # no error

def function7():
    """list index is a slice"""
    return TESTLIST[slice(1, 2, 3)] # no error

def function8():
    """list index implements __index__"""
    class IndexType(object): # pylint: disable=too-few-public-methods
        """Class with __index__ method"""
        def __index__(self): # pylint: disable=no-self-use
            """Allow objects of this class to be used as slice indices"""
            return 0

    return TESTLIST[IndexType()] # no error

def function9():
    """list index implements __index__ in a superclass"""
    class IndexType(object): # pylint: disable=too-few-public-methods
        """Class with __index__ method"""
        def __index__(self): # pylint: disable=no-self-use
            """Allow objects of this class to be used as slice indices"""
            return 0

    class IndexSubType(IndexType): # pylint: disable=too-few-public-methods
        """Class with __index__ in parent"""
        pass

    return TESTLIST[IndexSubType()] # no error

def function10():
    """list index does not implement __index__"""
    class NonIndexType(object): # pylint: disable=too-few-public-methods
        """Class without __index__ method"""
        pass

    return TESTLIST[NonIndexType()]

# Repeat a handful of tests to ensure non-list types are caught
def function11():
    """Tuple index is None"""
    return TESTTUPLE[None]

def function12():
    """Tuple index is an int constant"""
    return TESTTUPLE[0]

def function13():
    """String index is None"""
    return TESTSTR[None]

def function14():
    """String index is an int constant"""
    return TESTSTR[0]
