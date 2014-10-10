"""Check possible undefined loopvar
"""
from __future__ import print_function
__revision__ = 0

def do_stuff(some_random_list):
    """This is not right."""
    for var in some_random_list:
        pass
    print(var)


def do_else(some_random_list):
    """This is not right."""
    for var in some_random_list:
        if var == 42:
            break
    else:
        var = 84
    print(var)
