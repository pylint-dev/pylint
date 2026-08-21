# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import itertools
import os
from io import StringIO
from pathlib import Path

import pytest

from pylint.reporters.text import TextReporter
from pylint.testutils._run import _Run as Run

PARENT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
REGR_DATA = os.path.join(PARENT_DIR, "regrtest_data")


@pytest.mark.timeout(8)
def test_process_tokens() -> None:
    with pytest.raises(SystemExit) as cm:
        Run(
            [os.path.join(REGR_DATA, "very_long_line.py"), "--disable=C"],
            reporter=TextReporter(),
        )
    assert cm.value.code == 0


@pytest.mark.timeout(60)
def test_issue_5724() -> None:
    """Regression test for parsing of pylint disable pragma's."""
    with pytest.raises(SystemExit) as cm:
        Run(
            [
                os.path.join(REGR_DATA, "issue_5724.py"),
                "--enable=missing-final-newline",
                "--disable=C",
            ],
            reporter=TextReporter(),
        )
    assert cm.value.code == 0


@pytest.mark.timeout(30)
def test_long_comparison_chain_does_not_crash(tmp_path: Path) -> None:
    """A machine-generated ``and`` chain must not exhaust the recursion limit.

    ``chained-comparison`` walks the operands as a graph, and both the cycle
    search and the path search are recursive.
    """
    names = [f"x{index}" for index in range(1201)]
    chain = " and ".join(
        f"{left} > {right}" for left, right in itertools.pairwise(names)
    )
    source = tmp_path / "long_comparison_chain.py"
    source.write_text(
        f'"""A condition no human would write."""\n\n\n'
        f"def check({', '.join(names)}):\n"
        f"    return {chain}\n",
        encoding="utf-8",
    )

    output = StringIO()
    with pytest.raises(SystemExit):
        Run(
            [
                str(source),
                "--disable=all",
                "--enable=chained-comparison,chained-comparison-all-equal,"
                "impossible-comparison,astroid-error,fatal",
            ],
            reporter=TextReporter(output),
        )
    assert "Fatal error" not in output.getvalue()
