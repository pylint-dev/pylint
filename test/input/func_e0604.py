"""Test for invalid objects in a module's __all__ variable.

"""
#  pylint: disable=R0903,R0201,W0612

__revision__ = 0

def some_function():
    """Just a function."""
    pass


__all__ = [some_function]
