"""Tests for no-member on imported modules"""
# pylint: disable=import-outside-toplevel, pointless-statement


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
