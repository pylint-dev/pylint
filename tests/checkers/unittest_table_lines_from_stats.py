# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from pylint.checkers import table_lines_from_stats
from pylint.utils import LinterStats


def test_table_lines_from_stats_message_types_with_old_stats() -> None:
    """Test table_lines_from_stats formats integer message counts with diff_string."""
    new = LinterStats()
    old = LinterStats()
    new.convention, old.convention = 5, 2
    new.warning, old.warning = 3, 3
    new.error, old.error = 1, 4

    lines = table_lines_from_stats(new, old, "message_types")

    assert all(isinstance(cell, str) for cell in lines)
    assert lines == [
        "convention",
        "5",
        "2",
        "+3.00",
        "refactor",
        "0",
        "0",
        "=",
        "warning",
        "3",
        "3",
        "=",
        "error",
        "1",
        "4",
        "-3.00",
    ]


def test_table_lines_from_stats_message_types_without_old_stats() -> None:
    """Test table_lines_from_stats handles missing old stats for message types."""
    new = LinterStats()
    new.convention = 5

    lines = table_lines_from_stats(new, None, "message_types")

    assert all(isinstance(cell, str) for cell in lines)
    assert lines == [
        "convention",
        "5",
        "NC",
        "NC",
        "refactor",
        "0",
        "NC",
        "NC",
        "warning",
        "0",
        "NC",
        "NC",
        "error",
        "0",
        "NC",
        "NC",
    ]


def test_table_lines_from_stats_duplicated_lines_with_old_stats() -> None:
    """Test table_lines_from_stats formats integer and float duplicated lines with diff_string."""
    new = LinterStats()
    old = LinterStats()
    new.duplicated_lines["nb_duplicated_lines"] = 10
    new.duplicated_lines["percent_duplicated_lines"] = 2.5
    old.duplicated_lines["nb_duplicated_lines"] = 6
    old.duplicated_lines["percent_duplicated_lines"] = 1.5

    lines = table_lines_from_stats(new, old, "duplicated_lines")

    assert all(isinstance(cell, str) for cell in lines)
    assert lines == [
        "nb duplicated lines",
        "10",
        "6",
        "+4.00",
        "percent duplicated lines",
        "2.500",
        "1.500",
        "+1.00",
    ]


def test_table_lines_from_stats_duplicated_lines_without_old_stats() -> None:
    """Test table_lines_from_stats handles missing old stats for duplicated lines."""
    new = LinterStats()
    new.duplicated_lines["nb_duplicated_lines"] = 10
    new.duplicated_lines["percent_duplicated_lines"] = 2.5

    lines = table_lines_from_stats(new, None, "duplicated_lines")

    assert all(isinstance(cell, str) for cell in lines)
    assert lines == [
        "nb duplicated lines",
        "10",
        "NC",
        "NC",
        "percent duplicated lines",
        "2.500",
        "NC",
        "NC",
    ]
