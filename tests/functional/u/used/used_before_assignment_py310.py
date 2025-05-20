"""Tests for used-before-assignment with python 3.10's pattern matching"""

match ("example", "one"):
    case (x, y) if x == "example":
        print("x used to cause used-before-assignment!")
    case _:
        print("good thing it doesn't now!")


# pylint: disable = missing-function-docstring, redefined-outer-name, missing-class-docstring

# https://github.com/pylint-dev/pylint/issues/9668
from enum import Enum
from pylint.constants import PY311_PLUS
if PY311_PLUS:
    from typing import assert_never  # pylint: disable=no-name-in-module
else:
    from typing_extensions import assert_never

class Example(Enum):
    FOO = 1
    BAR = 2

def check_value_if_then_match_return(example: Example, should_check: bool) -> str | None:
    if should_check:
        result = None
    else:
        match example:
            case Example.FOO:
                result = "foo"
            case Example.BAR:
                result = "bar"
            case _:
                return None

    return result

def check_value_if_then_match_raise(example: Example, should_check: bool) -> str | None:
    if should_check:
        result = None
    else:
        match example:
            case Example.FOO:
                result = "foo"
            case Example.BAR:
                result = "bar"
            case _:
                raise ValueError("Not a valid enum")

    return result

def check_value_if_then_match_assert_never(example: Example, should_check: bool) -> str | None:
    if should_check:
        result = None
    else:
        match example:
            case Example.FOO:
                result = "foo"
            case Example.BAR:
                result = "bar"
            case _:
                assert_never(example)

    return result

def g(x):
    if x is None:
        y = 0
    else:
        match x:
            case int():
                y = x
            case _:
                raise TypeError(type(x))

    return y

def check_value_if_then_match_nested(
    example: Example, example_inner: Example, should_check: bool
) -> str | None:
    if should_check:
        result = None
    else:
        match example:
            case Example.FOO:
                match example_inner:
                    case Example.BAR:
                        result = "bar"
                    case _:
                        return None
            case _:
                return None

    return result

def check_value_if_then_match_non_exhaustive(example: Example, should_check: bool) -> str | None:
    if should_check:
        result = None
    else:
        match example:
            case Example.FOO:
                result = "foo"
            case Example.BAR:
                pass
            case _:
                return None

    return result  # [possibly-used-before-assignment]
