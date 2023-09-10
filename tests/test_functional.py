# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Functional full-module tests for PyLint."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from _pytest.config import Config

from pylint import testutils
from pylint.constants import PY312_PLUS
from pylint.testutils import UPDATE_FILE, UPDATE_OPTION
from pylint.testutils.functional import (
    FunctionalTestFile,
    LintModuleOutputUpdate,
    get_functional_test_files_from_directory,
)
from pylint.utils import HAS_ISORT_5

FUNCTIONAL_DIR = Path(__file__).parent.resolve() / "functional"


# isort 5 has slightly different rules as isort 4. Testing both would be hard: test with isort 5 only.
TESTS = [
    t
    for t in get_functional_test_files_from_directory(FUNCTIONAL_DIR)
    if not (t.base == "wrong_import_order" and not HAS_ISORT_5)
]
TESTS_NAMES = [t.base for t in TESTS]
TEST_WITH_EXPECTED_DEPRECATION = [
    "anomalous_backslash_escape",
    "anomalous_unicode_escape",
    "excess_escapes",
    "future_unicode_literals",
]


@pytest.mark.parametrize("test_file", TESTS, ids=TESTS_NAMES)
def test_functional(test_file: FunctionalTestFile, pytestconfig: Config) -> None:
    __tracebackhide__ = True  # pylint: disable=unused-variable
    lint_test: LintModuleOutputUpdate | testutils.LintModuleTest
    if UPDATE_FILE.exists():
        lint_test = LintModuleOutputUpdate(test_file, pytestconfig)
    else:
        lint_test = testutils.LintModuleTest(test_file, pytestconfig)
    lint_test.setUp()

    if test_file.base in TEST_WITH_EXPECTED_DEPRECATION:
        exception_type = SyntaxWarning if PY312_PLUS else DeprecationWarning
        with pytest.warns(exception_type, match="invalid escape sequence"):
            lint_test.runTest()
    else:
        lint_test.runTest()


if __name__ == "__main__":
    if UPDATE_OPTION in sys.argv:
        UPDATE_FILE.touch()
        sys.argv.remove(UPDATE_OPTION)
    try:
        pytest.main(sys.argv)
    finally:
        if UPDATE_FILE.exists():
            UPDATE_FILE.unlink()
