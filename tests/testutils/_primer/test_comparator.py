# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import json
from pathlib import Path

import pytest

from pylint.testutils._primer.comparator import Comparator

CASES_PATH = Path(__file__).parent / "cases"


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
    for (package, missing, new), exp in zip(results, expected):
        assert package == exp["package"]
        assert len(missing["messages"]) == exp["missing"]
        assert len(new["messages"]) == exp["new"]


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
    for (package, missing, new), exp in zip(results, expected):
        assert package == exp["package"]
        assert len(missing["messages"]) == exp["missing"]
        assert len(new["messages"]) == exp["new"]
