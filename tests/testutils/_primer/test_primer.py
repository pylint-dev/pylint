# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Test the primer commands. """
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from pylint.constants import IS_PYPY
from pylint.testutils._primer.primer import Primer

HERE = Path(__file__).parent
TEST_DIR_ROOT = HERE.parent.parent
PRIMER_DIRECTORY = TEST_DIR_ROOT / ".pylint_primer_tests/"
PACKAGES_TO_PRIME_PATH = TEST_DIR_ROOT / "primer/packages_to_prime.json"
FIXTURES_PATH = HERE / "fixtures"

PRIMER_CURRENT_INTERPRETER = (3, 10)


@pytest.mark.skipif(
    sys.platform in {"win32", "darwin"},
    reason="Primers are internal will never be run on costly github action (mac or windows)",
)
@pytest.mark.skipif(
    sys.version_info[:2] != PRIMER_CURRENT_INTERPRETER or IS_PYPY,
    reason=f"Primers are internal will always be run for only one interpreter (currently {PRIMER_CURRENT_INTERPRETER})",
)
@pytest.mark.parametrize(
    "directory",
    [
        pytest.param(p, id=str(p.relative_to(FIXTURES_PATH)))
        for p in FIXTURES_PATH.iterdir()
        if p.is_dir()
    ],
)
def test_compare(directory: Path) -> None:
    main = directory / "main.json"
    pr = directory / "pr.json"
    expected_file = directory / "expected.txt"
    new_argv = [
        "python tests/primer/__main__.py",
        "compare",
        "--commit=v2.14.2",
        f"--base-file={main}",
        f"--new-file={pr}",
    ]
    with patch("sys.argv", new_argv):
        Primer(PRIMER_DIRECTORY, PACKAGES_TO_PRIME_PATH).run()
    with open(PRIMER_DIRECTORY / "comment.txt", encoding="utf8") as f:
        content = f.read()
    with open(expected_file, encoding="utf8") as f:
        expected = f.read()
    # rstrip so the expected.txt can end with a newline
    assert content == expected.rstrip("\n")
