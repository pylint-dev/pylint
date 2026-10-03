"""test no crash on __file__ global"""

def func():
    """override __file__"""
    global __file__  # [global-statement, redefined-builtin]
    __file__ = 'hop'
