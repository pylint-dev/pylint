""" Tests for invalid-name checker. """
# pylint: disable=unused-import, wrong-import-position, import-outside-toplevel, missing-class-docstring
# pylint: disable=too-few-public-methods


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


def dummy_decorator(aaabc, bbbcd):
    """Some"""
    def real_decorator(fff):
        """pieces of"""
        def wrapper(*args, **kwargs):
            """docstring"""
            print(aaabc, bbbcd)
            fff(*args, **kwargs)
        return wrapper
    return real_decorator


@dummy_decorator(1, [
    0  # Fixing #119 should make this go away
# C0103 always points here - line 61  # [invalid-name]


])
def a_very_very_very_long_function_name_WithCamelCase_to_make_it_sad():  # Should be line 65
    """Docstring"""
    print('LOL')

a_very_very_very_long_function_name_WithCamelCase_to_make_it_sad()


class FooBar:
    def __init__(self, fooBar) -> None: # [invalid-name]
        self.foo_bar = fooBar
