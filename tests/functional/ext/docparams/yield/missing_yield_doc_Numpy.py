"""Tests for missing-yield-doc and missing-yield-type-doc for Numpy style docstrings"""
# pylint: disable=missing-function-docstring, unused-argument, function-redefined
# pylint: disable=invalid-name, undefined-variable


# Test redundant yields docstring variants
def my_func(self):
    """This is a docstring.

    Yields
    -------
        int
            One
        None
            Sometimes
    """
    if a_func():
        yield None
    yield 1


def my_func(self):  # [redundant-yields-doc]
    """This is a docstring.

    Yields
    -------
        int
            One
    """
    return 1
