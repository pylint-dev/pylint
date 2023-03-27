"""Test valid __all__ format."""

# pylint: disable=import-error, unused-import

from foo import bar

__all__ = tuple(globals().keys())
