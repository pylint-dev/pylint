""" Tests for invalid-name checker. """
# pylint: disable=unused-import, no-absolute-import, wrong-import-position,import-outside-toplevel

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

def a(): # [invalid-name]
    """yo"""


def _generate_cmdline_tests():
    TestCase = collections.namedtuple('TestCase', 'cmd, valid')
    valid = ['leave-mode', 'hint all']
    # Valid command only -> valid
    for item in valid:
        yield TestCase(''.join(item), True)


# We should emit for the loop variable.
for i in range(10):
    Foocapfor = 2  # [invalid-name]
