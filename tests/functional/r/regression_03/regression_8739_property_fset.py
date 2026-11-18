"""Regression test for https://github.com/pylint-dev/pylint/issues/8739.

Reading ``fset`` of a property that has no setter crashed with an uncaught
``InferenceError``.
"""

# pylint: disable=too-few-public-methods,pointless-statement


class Config:
    """A read-only property."""

    @property
    def size(self):
        """No setter."""
        return 1


Config.size.fset
Config.size.fget
Config.size.fdel
