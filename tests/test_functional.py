# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

"""Functional full-module tests for PyLint."""
import sys
from pathlib import Path
from typing import Union

import pytest
from _pytest.config import Config
from _pytest.recwarn import WarningsRecorder

from pylint import testutils
from pylint.testutils import UPDATE_FILE, UPDATE_OPTION
from pylint.testutils.functional import (
    FunctionalTestFile,
    LintModuleOutputUpdate,
    get_functional_test_files_from_directory,
)
from pylint.utils import HAS_ISORT_5

# TODOs
#  - implement exhaustivity tests


FUNCTIONAL_DIR = Path(__file__).parent.resolve() / "functional"


# isort 5 has slightly different rules as isort 4. Testing both would be hard: test with isort 5 only.
TESTS = [
    t
    for t in get_functional_test_files_from_directory(FUNCTIONAL_DIR)
    if not (t.base == "wrong_import_order" and not HAS_ISORT_5)
]
TESTS_NAMES = [t.base for t in TESTS]
TEST_WITH_EXPECTED_DEPRECATION = [
    "future_unicode_literals",
    "anomalous_unicode_escape_py3",
]


@pytest.mark.parametrize("test_file", TESTS, ids=TESTS_NAMES)
def test_functional(
    test_file: FunctionalTestFile, recwarn: WarningsRecorder, pytestconfig: Config
) -> None:
    __tracebackhide__ = True  # pylint: disable=unused-variable
    if UPDATE_FILE.exists():
        lint_test: Union[
            LintModuleOutputUpdate, testutils.LintModuleTest
        ] = LintModuleOutputUpdate(test_file, pytestconfig)
    else:
        lint_test = testutils.LintModuleTest(test_file, pytestconfig)
    lint_test.setUp()
    lint_test.runTest()
    warning = None
    try:
        # Catch <unknown>:x: DeprecationWarning: invalid escape sequence,
        # so, it's not shown during tests
        warning = recwarn.pop()
    except AssertionError:
        pass
    if warning is not None:
        if (
            test_file.base in TEST_WITH_EXPECTED_DEPRECATION
            and sys.version_info.minor > 5
        ):
            assert issubclass(warning.category, DeprecationWarning)
            assert "invalid escape sequence" in str(warning.message)


if __name__ == "__main__":
    if UPDATE_OPTION in sys.argv:
        UPDATE_FILE.touch()
        sys.argv.remove(UPDATE_OPTION)
    try:
        pytest.main(sys.argv)
    finally:
        if UPDATE_FILE.exists():
            UPDATE_FILE.unlink()
