# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/10455

A value built by a conditional expression and then narrowed with
``is not None`` should not trigger unsubscriptable-object.
"""

# pylint: disable=missing-docstring
from typing import Any


def use(structs1: dict[str, list[Any]], structs2: dict[str, list[Any]]) -> Any:
    end_of_good_plan = structs1["<key>"] if "<key>" in structs1 else None
    end_of_bad_plan = structs2["<key>"] if "<key>" in structs2 else None

    if end_of_good_plan is not None and end_of_bad_plan is not None:
        return end_of_good_plan[0]
    return None
