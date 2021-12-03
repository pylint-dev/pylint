"""Tests for missing-raises-doc and missing-raises-type-doc for Numpy style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, try-except-raise, import-outside-toplevel


def test_find_missing_numpy_raises(self):  # [missing-raises-doc]
    """This is a Numpy docstring.

    Raises
    ------
    NameError
        Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]


def test_find_all_numpy_raises(self):
    """This is a Numpy docstring.

    Raises
    ------
    RuntimeError
        Always
    NameError
        Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]


def test_find_rethrown_numpy_raises(self):  # [missing-raises-doc]
    """This is a Numpy docstring.

    Raises
    ------
    NameError
        Sometimes
    """
    try:
        fake_func()
    except RuntimeError:
        raise

    raise NameError("hi")


def test_find_rethrown_numpy_multiple_raises(self):  # [missing-raises-doc]
    """This is a Numpy docstring.

    Raises
    ------
    NameError
        Sometimes
    """
    try:
        fake_func()
    except (RuntimeError, ValueError):
        raise

    raise NameError("hi")


def test_ignores_caught_numpy_raises(self):
    """This is a numpy docstring.

    Raises
    ------
    NameError
        Sometimes
    """
    try:
        raise RuntimeError("hi")
    except RuntimeError:
        pass

    raise NameError("hi")


def test_find_numpy_attr_raises_exact_exc(self):
    """This is a numpy docstring.

    Raises
    ------
    re.error
        Sometimes
    """
    import re

    raise re.error("hi")


def test_find_numpy_attr_raises_substr_exc(self):
    """This is a numpy docstring.

    Raises
    ------
    re.error
        Sometimes
    """
    from re import error

    raise error("hi")


def test_find_valid_missing_numpy_attr_raises(self):  # [missing-raises-doc]
    """This is a numpy docstring.

    Raises
    ------
    re.anothererror
        Sometimes
    """
    from re import error

    raise error("hi")


def test_find_invalid_missing_numpy_attr_raises(self):
    """This is a numpy docstring.
     pylint allows this to pass since the comparison between Raises and
    raise are based on the class name, not the qualified name.

    Raises
    ------
    bogusmodule.error
        Sometimes
    """
    from re import error

    raise error("hi")
