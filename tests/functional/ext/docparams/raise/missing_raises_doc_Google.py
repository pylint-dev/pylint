"""Tests for missing-raises-doc and missing-raises-type-doc for Google style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, import-outside-toplevel, import-error


def test_find_missing_google_raises(self):  # [missing-raises-doc]
    """This is a docstring.

    Raises:
        NameError: Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]


def test_find_google_attr_raises_exact_exc(self):
    """This is a google docstring.

    Raises:
        re.error: Sometimes
    """
    import re

    raise re.error("hi")


def test_find_google_attr_raises_substr_exc(self):
    """This is a google docstring.

    Raises:
        re.error: Sometimes
    """
    from re import error

    raise error("hi")


def test_find_valid_missing_google_attr_raises(self):  # [missing-raises-doc]
    """This is a google docstring.

    Raises:
        re.anothererror: Sometimes
    """
    from re import error

    raise error("hi")


def test_find_invalid_missing_google_attr_raises(self):
    """This is a google docstring.
    pylint allows this to pass since the comparison between Raises and
    raise are based on the class name, not the qualified name.

    Raises:
        bogusmodule.error: Sometimes
    """
    from re import error

    raise error("hi")


def test_google_raises_local_reference(self):
    """This is a google docstring.
    pylint allows this to pass since the comparison between Raises and
    raise are based on the class name, not the qualified name.

    Raises:
        .LocalException: Always
    """
    from neighbor_module import LocalException

    raise LocalException("hi")


def test_find_all_google_raises(self):
    """This is a docstring.

    Raises:
        RuntimeError: Always
        NameError: Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]
