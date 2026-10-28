# pylint: disable=missing-docstring

from collections.abc import Callable
from decimal import Decimal
from fractions import Fraction  # [unused-import]
from typing import Optional, TypeAlias

def unused_variable_should_not_be_emitted():
    """unused-variable shouldn't be emitted for Example."""
    Example: TypeAlias = int
    result: set["Example"] = set()
    return result

# The value of an explicit TypeAlias is a type expression, so a string in it is
# a forward reference. unused-import shouldn't be emitted for Callable or Decimal.
Handler: TypeAlias = "Callable[[int], int]"
MaybeDecimal: TypeAlias = Optional["Decimal"]

# Without the TypeAlias annotation this is only a string.
NOT_A_TYPE = "Fraction"
