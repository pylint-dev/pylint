"""Regression test for https://github.com/pylint-dev/pylint/issues/8331

After ``if not isinstance(...): raise``, the value is one of the checked
types, so a unary operator on it is valid.
"""

# pylint: disable=missing-docstring


def make(kind: str) -> int | float | complex | str | set | None:
    if kind == "int":
        return 1
    if kind == "float":
        return 1.0
    if kind == "complex":
        return 1.0j
    if kind == "str":
        return "a"
    if kind == "set":
        return set()
    return None


def negate(kind: str) -> int | float | complex:
    operand = make(kind)
    if not isinstance(operand, (int, float, complex)):
        raise ValueError("operand is not a number")
    return -operand
