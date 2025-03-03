"""https://github.com/pylint-dev/pylint/issues/3675"""


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


# Negative case, see `_check_isinstance_args` in `./pylint/checkers/typecheck.py`
isinstance(1, int, int) # [too-many-function-args]
isinstance(1, 1, int) # [too-many-function-args, isinstance-second-argument-not-valid-type]
