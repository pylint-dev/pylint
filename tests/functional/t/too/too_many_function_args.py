"""https://github.com/PyCQA/pylint/issues/3675"""


def noop(x):  # pylint: disable=invalid-name
    """Return value unchanged"""
    return x


def add(x, y):  # pylint: disable=invalid-name
    """Add two values"""
    return x + y


def main(param):
    """Should not emit too-many-function-args"""
    tmp = noop  # matched first
    if param == 0:
        tmp = add
    return tmp(1, 1.01)
