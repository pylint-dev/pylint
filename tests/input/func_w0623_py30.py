"""Test for W0623, overwriting names in exception handlers."""
# pylint: disable=unnecessary-pass

__revision__ = ''

class MyError(Exception):
    """Special exception class."""
    pass


def some_function():
    """A function."""

    try:
        {}["a"]
    except KeyError as some_function: # W0623
        pass
