'Exeptions may be silently swallowed'
from __future__ import print_function
__revision__ = None
# pylint: disable=using-constant-test
def insidious_break_and_return():
    """I found you !"""
    for i in range(0, -5, -1):
        my_var = 0
        print(i)
        try:
            my_var += 1.0/i
            if i < -3:
                break # :D
            else:
                return my_var # :D
        finally:
            if i > -2:
                break # :(
            else:
                return my_var # :(
    return None

def break_and_return():
    """I found you !"""
    for i in range(0, -5, -1):
        my_var = 0
        if i:
            break # :D
        try:
            my_var += 1.0/i
        finally:
            for _ in range(2):
                if True:
                    break # :D
            else:
                def strange():
                    """why not ?"""
                    if True:
                        return my_var # :D
                strange()
        if i:
            break # :D
        else:
            return # :D
