"""Test linting.

This is only intended to test pylint support for python 3.8's
positional-only arguments (PEP 570).
"""


class Foobar:
    """Class for frobulating the Foobar."""

    @classmethod
    def buildme(cls, /, value):
        """Construct object using alternate method."""
        return cls(value).abc

    def runme(self, qrs, /, xyz=None):
        """Do something funcy."""
        if self.abc and qrs and xyz:
            print("found something else")

    abc = 42
