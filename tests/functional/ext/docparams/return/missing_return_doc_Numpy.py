"""Tests for missing-return-doc and missing-return-type-doc for Numpy style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def my_func(self):
    """This is a docstring.

    Returns
    -------
    bool
        Always False
    """
    return False


def my_func(self):
    """This is a docstring.

    Returns
    -------
    :obj:`list` of :obj:`str`
        List of strings
    """
    return ["hi", "bye"]
