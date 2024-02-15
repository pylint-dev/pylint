"""Tests that variables assigned as constants with boolean values are checked."""

# pylint: disable=invalid-name,missing-function-docstring
a: bool = True  # [invalid-boolean-variable-name]

# +1: [invalid-boolean-variable-name]
b, c = True, False  # [invalid-boolean-variable-name]

d: bool  # [invalid-boolean-variable-name]
e: bool  # [invalid-boolean-variable-name]

can_fly = False

is_flying: bool = False

flew = True  # [invalid-boolean-variable-name]


def hello() -> str:
    return "Hello, World!"


my_str = hello()

another_str: str
another_str = "Hello, World!"
