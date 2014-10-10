"""Tests for redefining builtins."""

def function():
    """Redefined local."""
    type = 1  # [redefined-builtin]
    print type  # pylint: disable=print-statement

# pylint:disable=invalid-name
map = {}  # [redefined-builtin]
