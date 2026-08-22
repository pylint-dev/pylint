# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression tests for https://github.com/pylint-dev/pylint/issues/8503.

``--fail-under`` changes pylint's exit code but, before this fix, gave no
visible indication on the terminal that the run failed because the score
was under the configured threshold. These tests check that a message is
printed in that case, and that nothing extra is printed when the score
meets the threshold.
"""

from __future__ import annotations

import warnings
from io import StringIO
from os.path import abspath, dirname, join

import pytest

from pylint.testutils._run import _add_rcfile_default_pylintrc
from pylint.testutils._run import _Run as Run
from pylint.testutils.utils import _patch_streams

HERE = abspath(dirname(__file__))
FAIL_UNDER_PLUS7_5 = join(HERE, "regrtest_data", "fail_under_plus7_5.py")


def _run_pylint_capture_output(args: list[str]) -> str:
    out = StringIO()
    args = _add_rcfile_default_pylintrc(list(args) + ["--persistent=no"])
    with _patch_streams(out):
        with pytest.raises(SystemExit):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                Run(args)
    return out.getvalue()


def test_fail_under_message_printed_when_score_below_threshold() -> None:
    output = _run_pylint_capture_output(
        ["--fail-under", "7.6", "--enable=all", FAIL_UNDER_PLUS7_5]
    )
    assert (
        "Score 7.50/10 was below the required --fail-under "
        "threshold of 7.60/10; exiting with a failure status." in output
    )


def test_fail_under_message_absent_when_score_meets_threshold() -> None:
    output = _run_pylint_capture_output(
        ["--fail-under", "7.5", "--enable=all", FAIL_UNDER_PLUS7_5]
    )
    assert "Your code has been rated at 7.50/10" in output
    assert "--fail-under threshold" not in output
