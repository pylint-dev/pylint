"""test for eval usage"""

__revision__ = 0

eval('os.listdir(".")')
eval('os.listdir(".")', globals={})

eval('os.listdir(".")', globals=globals())

def func():
    """ eval in local scope"""
    eval('b = 1')

