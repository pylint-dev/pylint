"""Tests for missing-raises-doc and missing-raises-type-doc"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, import-error

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
