# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from typing import Literal

import pytest

from pylint.checkers import table_lines_from_stats
from pylint.utils import LinterStats


def _message_types_stats(convention: int, warning: int, error: int) -> LinterStats:
    stats = LinterStats()
    stats.convention, stats.warning, stats.error = convention, warning, error
    return stats


def _duplicated_lines_stats(number: int, percent: float) -> LinterStats:
    stats = LinterStats()
    stats.duplicated_lines["nb_duplicated_lines"] = number
    stats.duplicated_lines["percent_duplicated_lines"] = percent
    return stats


@pytest.mark.parametrize(
    "new,old,stat_type,expected",
    [
        pytest.param(
            _message_types_stats(5, 3, 1),
            _message_types_stats(2, 3, 4),
            "message_types",
            [
                ("convention", "5", "2", "+3.00"),
                ("refactor", "0", "0", "="),
                ("warning", "3", "3", "="),
                ("error", "1", "4", "-3.00"),
            ],
            id="message_types_with_old_stats",
        ),
        pytest.param(
            _message_types_stats(5, 0, 0),
            None,
            "message_types",
            [
                ("convention", "5", "NC", "NC"),
                ("refactor", "0", "NC", "NC"),
                ("warning", "0", "NC", "NC"),
                ("error", "0", "NC", "NC"),
            ],
            id="message_types_without_old_stats",
        ),
        pytest.param(
            _duplicated_lines_stats(10, 2.5),
            _duplicated_lines_stats(6, 1.5),
            "duplicated_lines",
            [
                ("nb duplicated lines", "10", "6", "+4.00"),
                ("percent duplicated lines", "2.500", "1.500", "+1.00"),
            ],
            id="duplicated_lines_with_old_stats",
        ),
        pytest.param(
            _duplicated_lines_stats(10, 2.5),
            None,
            "duplicated_lines",
            [
                ("nb duplicated lines", "10", "NC", "NC"),
                ("percent duplicated lines", "2.500", "NC", "NC"),
            ],
            id="duplicated_lines_without_old_stats",
        ),
    ],
)
def test_table_lines_from_stats(
    new: LinterStats,
    old: LinterStats | None,
    stat_type: Literal["duplicated_lines", "message_types"],
    expected: list[tuple[str, str, str, str]],
) -> None:
    """The difference column holds the change since the previous run, as a string."""
    assert table_lines_from_stats(new, old, stat_type) == [
        cell for row in expected for cell in row
    ]
