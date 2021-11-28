# Copyright (c) 2014-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 Michal Nowikowski <godfryd@gmail.com>
# Copyright (c) 2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Lucas Cimon <lucas.cimon@gmail.com>
# Copyright (c) 2018 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Mr. Senko <atodorov@mrsenko.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Damien Baty <damien.baty@polyconseil.fr>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2020 bernie gray <bfgray3@users.noreply.github.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Functional full-module tests for PyLint."""
import csv
import os
import sys
from typing import Union

import pytest
from _pytest.config import Config
from _pytest.recwarn import WarningsRecorder

from pylint import testutils
from pylint.testutils import UPDATE_FILE, UPDATE_OPTION
from pylint.testutils.functional_test_file import FunctionalTestFile
from pylint.utils import HAS_ISORT_5

# TODOs
#  - implement exhaustivity tests

# 'Wet finger' number of files that are reasonable to display by an IDE
# 'Wet finger' as in 'in my settings there are precisely this many'.
REASONABLY_DISPLAYABLE_VERTICALLY = 48


class LintModuleOutputUpdate(testutils.LintModuleTest):
    """If message files should be updated instead of checked."""

    class TestDialect(csv.excel):
        delimiter = ":"
        lineterminator = "\n"

    csv.register_dialect("test", TestDialect)

    def _check_output_text(self, _, expected_output, actual_output):
        if not expected_output and not actual_output:
            if os.path.exists(self._test_file.expected_output):
                os.remove(self._test_file.expected_output)
            return
        with open(self._test_file.expected_output, "w", encoding="utf-8") as f:
            writer = csv.writer(f, dialect="test")
            for line in actual_output:
                writer.writerow(line.to_csv())


def get_tests():
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "functional")
    suite = []
    for dirpath, _, filenames in os.walk(input_dir):
        if dirpath.endswith("__pycache__"):
            continue

        assert (
            len(filenames) <= REASONABLY_DISPLAYABLE_VERTICALLY
        ), f"{dirpath} contain too much functional tests files."

        for filename in filenames:
            if filename != "__init__.py" and filename.endswith(".py"):
                # isort 5 has slightly different rules as isort 4. Testing
                # both would be hard: test with isort 5 only.
                if filename == "wrong_import_order.py" and not HAS_ISORT_5:
                    continue
                suite.append(testutils.FunctionalTestFile(dirpath, filename))
    return suite


TESTS = get_tests()
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
        # Catch <unknown>:x: DeprecationWarning: invalid escape sequence
        # so it's not shown during tests
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
