# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import json
from pathlib import Path
from typing import cast

import pytest

from pylint.reporters.json_reporter import JSONMessage
from pylint.testutils._primer.comparator import (
    ChangedMessage,
    Comparator,
    _caret_hint,
    _is_symbol_rename,
    format_span,
    message_diff,
)

CASES_PATH = Path(__file__).parent / "cases"


def _msg(**overrides: object) -> JSONMessage:
    base: dict[str, object] = {
        "type": "warning",
        "module": "m",
        "obj": "",
        "line": 1,
        "column": 0,
        "endLine": 1,
        "endColumn": 5,
        "path": "m.py",
        "symbol": "s",
        "message": "msg",
        "messageId": "W0000",
        "confidence": "UNDEFINED",
        "absolutePath": "m.py",
    }
    base.update(overrides)
    return cast(JSONMessage, base)


@pytest.mark.parametrize(
    "directory",
    [pytest.param(p, id=p.name) for p in CASES_PATH.iterdir() if p.is_dir()],
)
def test_comparator(directory: Path) -> None:
    """Test Comparator with each fixture directory."""
    comparator = Comparator.from_json(directory / "main.json", directory / "pr.json")
    expected = json.loads((directory / "expected_comparator.json").read_text("utf-8"))
    results = list(comparator)
    assert len(results) == len(expected)
    for (package, missing, new, changed), exp in zip(results, expected):
        assert package == exp["package"]
        assert len(missing["messages"]) == exp["missing"]
        assert len(new["messages"]) == exp["new"]
        assert len(changed) == exp["changed"]


def test_format_span_without_end_position() -> None:
    """Messages missing endLine/endColumn fall back to a start-only span."""
    assert (
        format_span(_msg(line=42, column=7, endLine=None, endColumn=None)) == "`42:7`"
    )


def test_format_span_with_end_position() -> None:
    assert (
        format_span(_msg(line=42, column=7, endLine=43, endColumn=2)) == "`42:7`-`43:2`"
    )


def test_message_diff_merges_location_changes() -> None:
    """All location fields collapse into a single 'Moved from' sentence."""
    old = _msg()
    new = _msg(line=2, column=1, endLine=2, endColumn=6)
    assert message_diff(ChangedMessage(old=old, new=new)) == (
        "Moved from `1:0`-`1:5` to `2:1`-`2:6`."
    )


def test_caret_hint_returns_empty_when_mostly_changed() -> None:
    """When more than 60% of the text differs, carets are noise and are skipped."""
    assert _caret_hint("hello world", "goodbye universe") == ""


@pytest.mark.parametrize(
    ("old_symbol", "new_symbol", "expected"),
    [
        ("used-before-assignment", "possibly-used-before-assignment", True),
        ("abstract-method", "no-abstract-method", True),
        ("useless-suppression", "locally-disabled", False),
        ("too-complex", "too-many-locals", False),
        # Similar-looking but unrelated symbols must stay below the threshold.
        ("unused-variable", "unused-import", False),
        ("no-member", "no-name-in-module", False),
    ],
)
def test_is_symbol_rename(old_symbol: str, new_symbol: str, expected: bool) -> None:
    old = _msg(symbol=old_symbol)
    new = _msg(symbol=new_symbol)
    assert _is_symbol_rename(old, new) is expected


def test_message_diff_field_on_one_side_only() -> None:
    """A field present on only one side must not crash the diff rendering."""
    old = _msg()
    new = _msg(suggestion="use x instead")
    diff = message_diff(ChangedMessage(old=old, new=new))
    assert "suggestion: `None` → `use x instead`" in diff


def test_message_diff_multiline_value_diffs_line_by_line() -> None:
    """Multi-line messages (e.g. duplicate-code) diff per line, keeping context."""
    old = _msg(message="Similar lines in 2 files\n==a:[10:14]\nresult = []")
    new = _msg(message="Similar lines in 2 files\n==a:[10:15]\nresult = []")
    assert message_diff(ChangedMessage(old=old, new=new)) == (
        "```diff\n"
        "  Similar lines in 2 files\n"
        "- ==a:[10:14]\n"
        "+ ==a:[10:15]\n"
        "           ^\n"
        "  result = []\n"
        "```"
    )


def test_comparator_batched() -> None:
    fixture = Path(__file__).parent / "batched_cases"
    comparator = Comparator.from_json(
        fixture / "main_BATCHIDX.json",
        fixture / "pr_BATCHIDX.json",
        batches=2,
    )
    expected = json.loads((fixture / "expected_comparator.json").read_text("utf-8"))
    results = list(comparator)
    assert len(results) == len(expected)
    for (package, missing, new, changed), exp in zip(results, expected):
        assert package == exp["package"]
        assert len(missing["messages"]) == exp["missing"]
        assert len(new["messages"]) == exp["new"]
        assert len(changed) == exp["changed"]
