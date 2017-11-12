"""Contains both normal error messages and Python3 porting error messages."""
# pylint: disable=too-few-public-methods

# error: import missing `from __future__ import absolute_import`
import sys

# error: Use raise ErrorClass(args) instead of raise ErrorClass, args.
raise Exception, 1

class Test(object):
    """dummy"""

    def __init__(self):
        # warning: Calling a dict.iter*() method
        {1: 2}.iteritems()
        return 42

# error: print statement used
print 'not in python3'
