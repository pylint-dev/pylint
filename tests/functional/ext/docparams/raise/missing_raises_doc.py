"""Tests for missing-raises-doc and missing-raises-type-doc"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, import-error, unused-variable

from unknown import Unknown


def test_ignores_no_docstring(self):
    raise RuntimeError("hi")


def test_ignores_unknown_style(self):
    """This is a docstring."""
    raise RuntimeError("hi")


def test_ignores_raise_uninferable(self):
    """This is a docstring.

    :raises NameError: Never
    """
    raise Unknown("hi")
    raise NameError("hi")  # [unreachable]


def test_ignores_returns_from_inner_functions(self):  # [missing-raises-doc]
    """This is a docstring.
    We do NOT expect a warning about the OSError in inner_func!

    :raises NameError: Never
    """

    def ex_func(val):
        def inner_func(value):
            return OSError(value)

        return RuntimeError(val)

    raise ex_func("hi")
    raise NameError("hi")  # [unreachable]


def test_ignores_returns_use_only_names():
    """This is a docstring

    :raises NameError: Never
    """

    def inner_func():
        return 42

    raise inner_func()  # [raising-bad-type]
