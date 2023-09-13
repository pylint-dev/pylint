# pylint: disable=missing-docstring

from typing import TypeAlias

def unused_variable_should_not_be_emitted():
    """unused-variable shouldn't be emitted for Example."""
    Example: TypeAlias = int
    result: set["Example"] = set()
    return result
