"""Tests for no-member on imported modules"""
# pylint: disable=import-outside-toplevel, pointless-statement, missing-function-docstring


def test_no_member_in_getattr():
    """Make sure that a module attribute access is checked by pylint."""
    import collections

    collections.THIS_does_not_EXIST  # [no-member]


def test_no_member_in_getattr_ignored() -> None:
    """Make sure that a module attribute access check is omitted with a
    module that is configured to be ignored.
    """
    import argparse

    argparse.THIS_does_not_EXIST


def test_ignored_modules_invalid_pattern() -> None:
    import xml

    xml.etree.THIS_does_not_EXIST  # [no-member]


def test_ignored_modules_root_one_applies_as_well() -> None:
    """Check that when a root module is completely ignored, submodules are skipped."""
    import argparse

    argparse.submodule.THIS_does_not_EXIST


def test_ignored_modules_patterns() -> None:
    import collections

    collections.abc.THIS_does_not_EXIST
