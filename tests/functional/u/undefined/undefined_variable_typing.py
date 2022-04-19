"""Tests for undefined-variable related to typing"""
# pylint: disable=invalid-name, import-error

# Ensure attribute lookups in type comments are accounted for.
# Reported in https://github.com/PyCQA/pylint/issues/4603

from typing import TYPE_CHECKING, Any, Dict

import foo
from foo import Bar, Boo

a = ...  # type: foo.Bar
b = ...  # type: foo.Bar[Boo]
c = ...  # type: Bar.Boo


if TYPE_CHECKING:
    __additional_builtin__: Dict[str, Any]
    repr: Any


def run():
    """https://github.com/PyCQA/pylint/issues/6388"""
    print(repr)
    return __additional_builtin__["test"]
