# pylint: disable=too-few-public-methods
"""
Simple test case for an annoying behavior in pylint.
"""


class Test:
    """Smallest test case for reported issue."""

    def __init__(self):
        self._thing = None

    @property
    def myattr(self):
        """Getter for myattr"""
        return self._thing

    @myattr.setter
    def myattr(self, value):
        """Setter for myattr."""
        self._thing = value

Test().myattr = 'grou'
