"""check use of * or **
"""

from operator import add
__revision__ = reduce(*(add, (1, 2, 3)))


def func(arg1, arg2):
    """magic function
    """
    return arg2, arg1

MYDICT = {'arg1':2, 'arg2': 4}
func(**MYDICT)

def coolfunc(*args, **kwargs):
    """magic function"""
    return func(*args, **kwargs)
