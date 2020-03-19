# Copyright (c) 2014-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 Michal Nowikowski <godfryd@gmail.com>
# Copyright (c) 2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Ville Skyttä <ville.skytta@upcloud.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Functional full-module tests for PyLint."""

import csv
import io
import os
import sys

import pytest

from pylint import checkers, lint, reporters, testutils


class test_dialect(csv.excel):
    delimiter = ":"
    lineterminator = "\n"


csv.register_dialect("test", test_dialect)


# Notes:
# - for the purpose of this test, the confidence levels HIGH and UNDEFINED
#   are treated as the same.

# TODOs
#  - implement exhaustivity tests

# If message files should be updated instead of checked.
UPDATE = False


class LintModuleOutputUpdate(testutils.LintModuleTest):
    def _open_expected_file(self):
        try:
            return super()._open_expected_file()
        except OSError:
            return io.StringIO()

    def _check_output_text(self, expected_messages, expected_lines, received_lines):
        if not expected_messages:
            return
        emitted, remaining = self._split_lines(expected_messages, expected_lines)
        if emitted != received_lines:
            remaining.extend(received_lines)
            remaining.sort(key=lambda m: (m[1], m[0], m[3]))
            with open(self._test_file.expected_output, "w") as fobj:
                writer = csv.writer(fobj, dialect="test")
                for line in remaining:
                    writer.writerow(line.to_csv())


def get_tests():
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "functional")
    suite = []
    for dirpath, dirnames, filenames in os.walk(input_dir):
        if dirpath.endswith("__pycache__"):
            continue
        for filename in filenames:
            if filename != "__init__.py" and filename.endswith(".py"):
                suite.append(testutils.FunctionalTestFile(dirpath, filename))
    return suite


TESTS = get_tests()
TESTS_NAMES = [t.base for t in TESTS]


@pytest.mark.parametrize("test_file", TESTS, ids=TESTS_NAMES)
def test_functional(test_file):
    LintTest = (
        LintModuleOutputUpdate(test_file)
        if UPDATE
        else testutils.LintModuleTest(test_file)
    )
    LintTest.setUp()
    LintTest._runTest()


if __name__ == "__main__":
    if "-u" in sys.argv:
        UPDATE = True
        sys.argv.remove("-u")
    pytest.main(sys.argv)
