"""Test valid __all__ format."""

# pylint: disable=import-error, unused-import, misplaced-module-dunder

from foo import bar

__all__ = list(globals().keys())
