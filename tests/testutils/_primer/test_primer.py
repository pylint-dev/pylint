# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Test the primer commands. """
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from _pytest.capture import CaptureFixture

from pylint.constants import IS_PYPY
from pylint.testutils._primer.primer import Primer

HERE = Path(__file__).parent
TEST_DIR_ROOT = HERE.parent.parent
PRIMER_DIRECTORY = TEST_DIR_ROOT / ".pylint_primer_tests/"
PACKAGES_TO_PRIME_PATH = TEST_DIR_ROOT / "primer/packages_to_prime.json"
FIXTURES_PATH = HERE / "fixtures"

PRIMER_CURRENT_INTERPRETER = (3, 10)

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
    sys.version_info[:2] != PRIMER_CURRENT_INTERPRETER or IS_PYPY,
    reason=(
        "Primers are internal and will always be run for only one interpreter (currently"
        f" {PRIMER_CURRENT_INTERPRETER})"
    ),
)
class TestPrimer:
    @pytest.mark.parametrize(
        "directory",
        [
            pytest.param(p, id=str(p.relative_to(FIXTURES_PATH)))
            for p in FIXTURES_PATH.iterdir()
            if p.is_dir()
        ],
    )
    def test_compare(self, directory: Path) -> None:
        """Test for the standard case.

        Directory in 'fixtures/' with 'main.json', 'pr.json' and 'expected.txt'."""
        self.__assert_expected(directory)

    def test_truncated_compare(self) -> None:
        """Test for the truncation of comments that are too long."""
        max_comment_length = 525
        directory = FIXTURES_PATH / "message_changed"
        with patch(
            "pylint.testutils._primer.primer_compare_command.MAX_GITHUB_COMMENT_LENGTH",
            max_comment_length,
        ):
            content = self.__assert_expected(
                directory, expected_file=directory / "expected_truncated.txt"
            )
        assert len(content) < max_comment_length

    @staticmethod
    def __assert_expected(
        directory: Path,
        main: Path | None = None,
        pr: Path | None = None,
        expected_file: Path | None = None,
    ) -> str:
        if main is None:
            main = directory / "main.json"
        if pr is None:
            pr = directory / "pr.json"
        if expected_file is None:
            expected_file = directory / "expected.txt"
        new_argv = [*DEFAULT_ARGS, f"--base-file={main}", f"--new-file={pr}"]
        with patch("sys.argv", new_argv):
            Primer(PRIMER_DIRECTORY, PACKAGES_TO_PRIME_PATH).run()
        with open(PRIMER_DIRECTORY / "comment.txt", encoding="utf8") as f:
            content = f.read()
        with open(expected_file, encoding="utf8") as f:
            expected = f.read()
        # rstrip so the expected.txt can end with a newline
        assert content == expected.rstrip("\n")
        return content
