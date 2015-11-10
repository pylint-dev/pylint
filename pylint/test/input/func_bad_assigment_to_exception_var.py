# pylint:disable=C0103, print-statement, no-absolute-import
"""ho ho ho"""
from __future__ import print_function
import sys
__revision__ = 'toto'

e = 1
e2 = 'yo'
e3 = None
try:
    raise e
except Exception as ex:
    print(ex)
    _, _, tb = sys.exc_info()



def func():
    """bla bla bla"""
    raise e3

def reraise():
    """reraise a catched exception instance"""
    try:
        raise Exception()
    except Exception as exc:
        print(exc)
        raise exc

raise e3
