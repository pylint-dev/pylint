# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import json
from pathlib import Path

import pytest

from pylint.testutils._primer.comparator import Comparator

FIXTURES_PATH = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize(
    "directory",
    [
        pytest.param(p, id=p.name)
        for p in FIXTURES_PATH.iterdir()
        if p.is_dir() and p.name != "batched"  # tested separately
    ],
)
def test_comparator(directory: Path) -> None:
    """Test Comparator with each fixture directory."""
    comparator = Comparator.from_json(
        str(directory / "main.json"), str(directory / "pr.json")
    )
    expected = json.loads((directory / "expected_comparator.json").read_text("utf-8"))
    results = list(comparator)
    assert len(results) == len(expected)
    for (package, missing, new, changed), exp in zip(results, expected):
        assert package == exp["package"]
        assert len(missing) == exp["missing"]
        assert len(new) == exp["new"]
        assert len(changed) == exp["changed"]


def test_comparator_batched() -> None:
    fixture = FIXTURES_PATH / "batched"
    comparator = Comparator.from_json(
        str(fixture / "main_BATCHIDX.json"),
        str(fixture / "pr_BATCHIDX.json"),
        batches=2,
    )
    expected = json.loads((fixture / "expected_comparator.json").read_text("utf-8"))
    results = list(comparator)
    assert len(results) == len(expected)
    for (package, missing, new, changed), exp in zip(results, expected):
        assert package == exp["package"]
        assert len(missing) == exp["missing"]
        assert len(new) == exp["new"]
        assert len(changed) == exp["changed"]
