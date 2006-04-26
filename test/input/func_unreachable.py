"""docstring"""

__revision__ = ''

def func1():
    """docstring"""
    return 1
    print 'unreachable'

def func2():
    """docstring"""
    while 1:
        break
        print 'unreachable'

def func3():
    """docstring"""
    for i in (1, 2, 3):
        print i
        continue
        print 'unreachable'
    
