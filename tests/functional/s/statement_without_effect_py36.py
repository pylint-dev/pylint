"""Test for statements without effects."""
# pylint: disable=too-few-public-methods


class ClassLevelAttributeTest:
    """ test attribute docstrings. """

    some_variable: int = 42
    """Data docstring"""

    some_other_variable: int = 42
    """Data docstring"""

    def func(self) -> None:
        """Some Empty Docstring"""

    # +1: [pointless-string-statement]
    """useless"""
