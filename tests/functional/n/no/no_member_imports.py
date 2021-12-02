"""Tests for no-member on imported modules"""
# pylint: disable=import-outside-toplevel, pointless-statement


def test_no_member_in_getattr():
    """Make sure that a module attribute access is checked by pylint."""
    import collections

    collections.THIS_does_not_EXIST  # [no-member]
