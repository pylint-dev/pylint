"""Regression test for https://github.com/PyCQA/pylint/issues/8109."""

# pylint: disable=missing-docstring, unsupported-binary-operation

from dataclasses import dataclass


@dataclass
class Number:
    amount: int | float
    round: int = 2

    def __str__(self) -> str:
        number_format = "{:,.%sf}" % self.round  # [consider-using-f-string]
        return number_format.format(self.amount).rstrip("0").rstrip(".")
