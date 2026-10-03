"""Tests for undefined-variable related to typing"""
# pylint: disable=invalid-name, import-error

# Ensure attribute lookups in type comments are accounted for.
# Reported in https://github.com/pylint-dev/pylint/issues/4603

from typing import TYPE_CHECKING, Any, Dict

import foo
from foo import Bar, Boo

a = ...  # type: foo.Bar
b = ...  # type: foo.Bar[Boo]
c = ...  # type: Bar.Boo


if TYPE_CHECKING:
    __additional_builtin__: Dict[str, Any]
    # For why this would emit redefined-builtin: https://github.com/pylint-dev/pylint/pull/3643
    # pylint: disable-next=redefined-builtin
    repr: Any


def run():
    """https://github.com/pylint-dev/pylint/issues/6388"""
    print(repr)
    return __additional_builtin__["test"]
