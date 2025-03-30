""" Tests for invalid-name checker. """
# pylint: disable=unused-import, wrong-import-position, import-outside-toplevel, missing-class-docstring,missing-function-docstring
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

bbb: int = 42  # [invalid-name]

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

def a():
    """We no longer fail 1-character names by default."""


def A():  # [invalid-name]
    """But we do check casing."""


def _generate_cmdline_tests():
    TestCase = collections.namedtuple('TestCase', 'cmd, valid')
    valid = ['leave-mode', 'hint all']
    # Valid command only -> valid
    for item in valid:
        yield TestCase(''.join(item), True)


# We should emit for the loop variable using the variable pattern.
for i in range(10):
    Foocapfor = 2  # [invalid-name]
    foonocapsfor = 3


# Reassignments outside loops
my_var = 0
my_var = 1


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


@dummy_decorator(1, [0])
def a_very_very_very_long_function_name_WithCamelCase_to_make_it_sad():  # [invalid-name]
    """Docstring"""
    print('LOL')

a_very_very_very_long_function_name_WithCamelCase_to_make_it_sad()


class FooBar:
    def __init__(self, fooBar) -> None:  # [invalid-name]
        self.foo_bar = fooBar
        self.foo_bar2 = None

    def func1(
        self,
        fooBar,  # [invalid-name]
    ):
        self.foo_bar = fooBar

    # Test disable invalid-name
    def test_disable1(self, fooBar):  # pylint: disable=invalid-name
        self.foo_bar = fooBar

    def test_disable2(
        self,
        fooBar,  # pylint: disable=invalid-name
    ):
        self.foo_bar = fooBar

    def test_disable3(self, fooBar):  # pylint: disable=invalid-name
        self.foo_bar = fooBar

    def test_disable_mixed(
        self,
        fooBar,  # pylint: disable=invalid-name
        fooBar2,  # [invalid-name]
    ):
        """Invalid-name will still be raised for other arguments."""
        self.foo_bar = fooBar
        self.foo_bar2 = fooBar2

    def tearDown(self): ...  # pylint: disable=invalid-name


class FooBarSubclass(FooBar):
    tearDown = FooBar.tearDown
    tearDownNotInAncestor = None  # [invalid-name]
