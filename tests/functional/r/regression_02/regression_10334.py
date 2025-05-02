"""Test for slice object used as a decorator."""
# pylint: disable=too-few-public-methods
s = slice(-2)
@s()  # [not-callable]
class A:
    """Class with a slice decorator."""
