"""Tests for missing-raises-doc and missing-raises-type-doc for Numpy style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def test_find_missing_numpy_raises(self):  # [missing-raises-doc]
    """This is a docstring.

    Raises
    ------
    NameError
        Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]


def test_find_all_numpy_raises(self):
    """This is a docstring.

    Raises
    ------
    RuntimeError
        Always
    NameError
        Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]
