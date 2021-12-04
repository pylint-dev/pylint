"""Tests for missing-return-doc and missing-return-type-doc"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def ignores_no_docstring(self):
    return False


def ignores_unknown_style(self):
    """This is a docstring."""
    return False
