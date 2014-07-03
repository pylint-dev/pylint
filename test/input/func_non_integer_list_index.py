"""Errors for non-integer list indicies"""

__revision__ = 0

TESTLIST = [1, 2, 3]

def function1():
    """index is a function"""
    return TESTLIST[id]

def function2():
    """index is a str constant"""
    return TESTLIST['0']

def function3():
    """index is None"""
    return TESTLIST[None]

def function4():
    """index is a float expression"""
    return TESTLIST[float(0)]

def function5():
    """index is an int constant"""
    return TESTLIST[0]  # no error

def function6():
    """index is a integer expression"""
    return TESTLIST[int(0.0)] # no error
