""" Tests for invalid-name checker. """
# pylint: disable=unused-import, no-absolute-import

AAA = 24
try:
    import collections
except ImportError:
    collections = None

aaa = 42 # [invalid-name]
try:
    import time
except ValueError:
    time = None # [invalid-name]

try:
    from sys import argv, executable as python
except ImportError:
    argv = 42
    python = 24

def test():
    """ Shouldn't emit an invalid-name here. """
    try:
        import re
    except ImportError:
        re = None
    return re
