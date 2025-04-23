"""Test for slice object used as a decorator."""
s = slice(-2)
@s()  # [not-callable]
class A:
    """Class with a slice decorator."""
