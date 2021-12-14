"""Tests for missing-raises-doc for exception class inheritance."""
# pylint: disable=missing-class-docstring

class CustomError(NameError):
    pass


class CustomChildError(CustomError):
    pass


def test_find_missing_raise_for_parent():  # [missing-raises-doc]
    """This is a docstring.

    Raises:
        CustomError: Never
    """
    raise NameError("hi")


def test_no_missing_raise_for_child_builtin():
    """This is a docstring.

    Raises:
        Exception: Never
    """
    raise ValueError("hi")


def test_no_missing_raise_for_child_custom():
    """This is a docstring.

    Raises:
        NameError: Never
    """
    raise CustomError("hi")


def test_no_missing_raise_for_child_custom_nested():
    """This is a docstring.

    Raises:
        NameError: Never
    """
    raise CustomChildError("hi")
