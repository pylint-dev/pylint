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


# pylint: disable=missing-class-docstring,too-few-public-methods,arguments-differ
class BaseHandler:
    def log_error(self, format, *args):  # [redefined-builtin]
        """Define an interface with a built-in parameter name."""
        return format, args


class Handler(BaseHandler):
    def log_error(self, format, *args):
        """Keep the inherited parameter name in the override."""
        type = 1  # [redefined-builtin]
        return format, args, type


class DifferentArgument(BaseHandler):
    def log_error(self, type, *args):  # [redefined-builtin]
        """A different built-in name is not required by the interface."""
        return type, args


def standalone(format):  # [redefined-builtin]
    """A function with no inherited signature still warns."""
    return format
