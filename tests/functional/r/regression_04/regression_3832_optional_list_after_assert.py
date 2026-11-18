"""Regression test for https://github.com/pylint-dev/pylint/issues/3832

An Optional list that starts as None, is reassigned in a loop and checked
with ``assert ... is not None`` supports item assignment. Fixed in astroid
by pylint-dev/astroid#3387.
"""

# pylint: disable=missing-docstring

from typing import Iterable, List, Optional


def merge_rows(rows: Iterable[List[str]]) -> None:
    """Append rows whose first cell is empty to the previous row."""
    previous: Optional[List[str]] = None
    for row in rows:
        if row[0]:
            if previous is not None:
                print(previous)
            previous = row
        else:
            assert previous is not None
            for index, cell in enumerate(row):
                if index:
                    previous[index] += " " + cell
    if previous is not None:
        print(previous)
