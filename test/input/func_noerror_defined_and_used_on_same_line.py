#pylint: disable=C0111,C0321
"""pylint complains about 'index' being used before definition"""
from __future__ import with_statement

__revision__ = None

print [index
       for index in range(10)]

print((index
       for index in range(10)))

FILTER_FUNC = lambda x: not x

def func(xxx): return xxx

def func2(xxx): return xxx + func2(1)

import sys; print sys.exc_info( )

for i in range(10): print i

j = 4; LAMB = lambda x: x+j

FUNC4 = lambda a, b : a != b
FUNC3 = lambda (a, b) : a != b

# test http://www.logilab.org/ticket/6954:

with open('f') as f: print(f.read())

