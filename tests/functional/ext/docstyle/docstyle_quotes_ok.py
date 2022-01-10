"""Checks of ok-ish docstrings."""
# pylint: disable=undefined-variable


def function2():
    """Test Ok"""


class FFFF:
    """This is ok."""

    @check_messages("bad-open-mode", "redundant-unittest-assert", "deprecated-module")
    def method5(self):
        """Test OK 1 with decorators"""

    def method6(self):
        r"""Test OK 2 with raw string"""

    def method7(self):
        u"""Test OK 3 with unicode string"""
