# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/7381

Chaining more than two ``|`` operands should not trigger
unsupported-binary-operation, whether the operands are flags of a nested enum or
instances reached through a subscript.

Pylint now requires Python 3.10 or later, where the branch behind this false
positive returns early, so the snippet is clean on every pylint from 2.13 on.
"""

# pylint: disable=missing-docstring,too-few-public-methods
from enum import Flag


class MosaicFlags(Flag):
    NONE = 0
    SUPPLY_MUTABLE = 1
    TRANSFERABLE = 2
    RESTRICTABLE = 4
    REVOKABLE = 8


combined = MosaicFlags.SUPPLY_MUTABLE | MosaicFlags.RESTRICTABLE | MosaicFlags.REVOKABLE
print(combined)


class Module:
    class TestFlags(Flag):
        TEST_NONE = 0
        TEST_SUPPLY_MUTABLE = 1
        TEST_TRANSFERABLE = 2
        TEST_RESTRICTABLE = 4
        TEST_REVOKABLE = 8


class TestClass:
    @staticmethod
    def _assert_flags_parser(value, expected):
        pass

    def test_flags_parser_can_handle_multiple_string_flags(self):
        self._assert_flags_parser(
            "supply_mutable restrictable revokable",
            Module.TestFlags.TEST_SUPPLY_MUTABLE
            | Module.TestFlags.TEST_RESTRICTABLE
            | Module.TestFlags.TEST_REVOKABLE,
        )


class BinaryOperator:
    def __or__(self, whatever):
        return 42


operators = [BinaryOperator(), BinaryOperator()]


def or_through_subscript(idx: int = 0):
    print(operators[0] | operators[1])
    print(operators[idx] | operators[1])


or_through_subscript(0)
