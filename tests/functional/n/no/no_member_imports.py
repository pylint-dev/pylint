"""Tests for no-member on imported modules"""
# pylint: disable=import-outside-toplevel, pointless-statement, missing-function-docstring


def test_no_member_in_getattr():
    """Make sure that a module attribute access is checked by pylint."""
    import math

    math.THIS_does_not_EXIST  # [no-member]


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
    import importlib

    importlib.metadata.THIS_does_not_EXIST


def test_ignored_classes_no_recursive_pattern() -> None:
    import sys

    sys.THIS_does_not_EXIST  # [no-member]


def test_ignored_classes_qualified_name() -> None:
    """Test that ignored-classes supports qualified name for ignoring."""

    import optparse

    optparse.Values.THIS_does_not_EXIST


def test_ignored_classes_only_name() -> None:
    """Test that ignored_classes works with the name only."""
    import optparse

    optparse.Option.THIS_does_not_EXIST
