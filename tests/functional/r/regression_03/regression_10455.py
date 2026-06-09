# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/10455

Conditional expression + None-narrowing should not trigger E1136.

Fix landed before pylint 2.13 (oldest Python-3.12-compatible version).
"""

# pylint: disable=missing-docstring,fixme
from typing import Any


def use(structs1: dict, structs2: dict) -> Any:
    end_of_good_plan = (
        structs1["<key>"] if "<key>" in structs1 else None
    )
    end_of_bad_plan = (
        structs2["<key>"] if "<key>" in structs2 else None
    )

    if end_of_good_plan is not None and end_of_bad_plan is not None:
        return end_of_good_plan[0]
    return None
