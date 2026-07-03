# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import os

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
