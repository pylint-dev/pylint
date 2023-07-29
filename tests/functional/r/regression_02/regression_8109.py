"""Regression test for https://github.com/pylint-dev/pylint/issues/8109."""

# pylint: disable=missing-docstring, unsupported-binary-operation

from dataclasses import dataclass


@dataclass
class Number:
    amount: int | float
    round: int = 2

    def __str__(self):
        number_format = "{:,.%sf}" % self.round
        return number_format.format(self.amount).rstrip("0").rstrip(".")
