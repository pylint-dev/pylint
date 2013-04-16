"""Test that non-inferable __all__ variables do not make Pylint crash.

"""
#  pylint: disable=R0903,R0201,W0612

__revision__ = 0

__all__ = [SomeUndefinedName]
