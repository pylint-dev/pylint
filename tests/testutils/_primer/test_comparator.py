# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import json
from pathlib import Path

import pytest
from pytest_remaster import (  # type: ignore[import-not-found]
    CaseData,
    GoldenMaster,
    discover_test_cases,
    json_normalizer,
)

from pylint.testutils._primer.comparator import Comparator

CASES_PATH = Path(__file__).parent / "cases"


def _comparator_to_json(comparator: Comparator) -> str:
    results = [
        {
            "package": package,
            "missing": len(missing["messages"]),
            "new": len(new["messages"]),
        }
        for package, missing, new in comparator
    ]
    return json.dumps(results, indent=2)


@pytest.mark.parametrize("case", discover_test_cases(CASES_PATH))
def test_comparator(case: CaseData, golden_master: GoldenMaster) -> None:
    """Test Comparator with each fixture directory."""
    comparator = Comparator(str(case.input / "main.json"), str(case.input / "pr.json"))
    golden_master.check(
        lambda: _comparator_to_json(comparator),
        case.input / "expected_comparator.json",
        normalizer=json_normalizer,
    )


def test_comparator_batched(golden_master: GoldenMaster) -> None:
    fixture = Path(__file__).parent / "batched_cases"
    comparator = Comparator(
        str(fixture / "main_BATCHIDX.json"),
        str(fixture / "pr_BATCHIDX.json"),
        batches=2,
    )
    golden_master.check(
        lambda: _comparator_to_json(comparator),
        fixture / "expected_comparator.json",
        normalizer=json_normalizer,
    )
