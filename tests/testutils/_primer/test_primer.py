# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Test the primer commands."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from _pytest.capture import CaptureFixture

from pylint.constants import IS_PYPY
from pylint.testutils._primer.primer import Primer
from pylint.testutils._primer.primer_compare_command import CompareCommand

HERE = Path(__file__).parent
TEST_DIR_ROOT = HERE.parent.parent
PRIMER_DIRECTORY = TEST_DIR_ROOT / ".pylint_primer_tests/"
PACKAGES_TO_PRIME_PATH = TEST_DIR_ROOT / "primer/packages_to_prime.json"
CASES_PATH = HERE / "cases"

# If you change this, also change DEFAULT_PYTHON in
# ``.github/workflows/primer_comment.yaml``
PRIMER_CURRENT_INTERPRETER = (3, 13)

DEFAULT_ARGS = ["python tests/primer/__main__.py", "compare", "--commit=v2.14.2"]


@pytest.mark.parametrize("args", [[], ["wrong_command"]])
def test_primer_launch_bad_args(args: list[str], capsys: CaptureFixture) -> None:
    with pytest.raises(SystemExit):
        with patch("sys.argv", ["python tests/primer/__main__.py", *args]):
            Primer(PRIMER_DIRECTORY, PACKAGES_TO_PRIME_PATH).run()
    out, err = capsys.readouterr()
    assert not out
    assert "usage: Pylint Primer" in err


@pytest.mark.skipif(
    sys.platform != "linux"
    or sys.version_info[:2] != PRIMER_CURRENT_INTERPRETER
    or IS_PYPY,
    reason=(
        "Primers are internal and will always be run for only one interpreter (currently"
        f" {PRIMER_CURRENT_INTERPRETER}, on linux)"
    ),
)
class TestPrimer:
    @pytest.mark.parametrize(
        "directory",
        [
            pytest.param(p, id=str(p.relative_to(CASES_PATH)))
            for p in CASES_PATH.iterdir()
            if p.is_dir()
        ],
    )
    def test_compare(self, directory: Path) -> None:
        """Test for the standard case.

        Directory in 'cases/' with 'main.json', 'pr.json' and 'expected.txt'.
        """
        self.__assert_expected(directory)

    def test_compare_batched(self) -> None:
        fixture = HERE / "batched_cases"
        self.__assert_expected(
            fixture,
            fixture / "main_BATCHIDX.json",
            fixture / "pr_BATCHIDX.json",
            batches=2,
        )

    def test_truncated_compare(self) -> None:
        """Test for the truncation of comments that are too long."""
        max_comment_length = 525
        directory = CASES_PATH / "message_changed"
        with patch(
            "pylint.testutils._primer.primer_compare_command.MAX_GITHUB_COMMENT_LENGTH",
            max_comment_length,
        ):
            content = self.__assert_expected(
                directory, expected_file=directory / "expected_truncated.txt"
            )
        assert len(content) < max_comment_length

    def test_truncated_compare_stops_iterating_packages(self) -> None:
        """Once the comment exceeds MAX, further packages should be skipped."""
        max_comment_length = 500
        directory = CASES_PATH / "multi_package"
        with patch(
            "pylint.testutils._primer.primer_compare_command.MAX_GITHUB_COMMENT_LENGTH",
            max_comment_length,
        ):
            content = self.__assert_expected(
                directory,
                expected_file=directory / "expected_truncated_break.txt",
            )
        # Only the first package made it in; the second was skipped by the break.
        assert "astroid" in content
        assert "astropy" not in content
        assert len(content) < max_comment_length

    def test_truncated_compare_in_details(self) -> None:
        """Test for the truncation of comments that are too long inside details."""
        max_comment_length = 420
        directory = CASES_PATH / "message_changed"
        with patch(
            "pylint.testutils._primer.primer_compare_command.MAX_GITHUB_COMMENT_LENGTH",
            max_comment_length,
        ):
            content = self.__assert_expected(
                directory, expected_file=directory / "expected_truncated_in_details.txt"
            )
        assert len(content) < max_comment_length

    def test_truncate_falls_back_when_no_space(self) -> None:
        """When the pre-limit prefix has no space, cut at ``max_len - 10`` directly."""
        max_comment_length = 200
        config = argparse.Namespace(commit="v2.14.2")
        command = CompareCommand(PRIMER_DIRECTORY, {}, config)
        spaceless = "x" * 500
        with patch(
            "pylint.testutils._primer.primer_compare_command.MAX_GITHUB_COMMENT_LENGTH",
            max_comment_length,
        ):
            truncated = command._truncate_comment(spaceless)
        assert "..." in truncated
        assert len(truncated) < max_comment_length

    @staticmethod
    def __assert_expected(
        directory: Path,
        main: Path | None = None,
        pr: Path | None = None,
        expected_file: Path | None = None,
        batches: int = 0,
    ) -> str:
        if main is None:
            main = directory / "main.json"
        if pr is None:
            pr = directory / "pr.json"
        if expected_file is None:
            expected_file = directory / "expected.txt"
        new_argv = [*DEFAULT_ARGS, f"--base-file={main}", f"--new-file={pr}"]
        if batches:
            new_argv.append(f"--batches={batches}")
        with patch("sys.argv", new_argv):
            Primer(PRIMER_DIRECTORY, PACKAGES_TO_PRIME_PATH).run()
        with open(PRIMER_DIRECTORY / "comment.txt", encoding="utf8") as f:
            content = f.read()
        with open(expected_file, encoding="utf8") as f:
            expected = f.read()
        # rstrip so the expected.txt can end with a newline
        assert content == expected.rstrip("\n")
        return content
