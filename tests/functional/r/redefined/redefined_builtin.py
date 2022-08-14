"""Tests for redefining builtins."""
# pylint: disable=unused-import, wrong-import-position, reimported, import-error
# pylint: disable=redefined-outer-name, import-outside-toplevel, wrong-import-order


def function():
    """Redefined local."""
    type = 1  # [redefined-builtin]
    print(type)


# pylint:disable=invalid-name
map = {}  # [redefined-builtin]
__doc__ = "reset the doc"


# Test redefining-builtins
from notos import open  # [redefined-builtin]

# Test default redefining-builtins-modules setting
from os import open

# Test non-default redefining-builtins-modules setting in function
def test():
    """Function importing a function"""
    from os import open
