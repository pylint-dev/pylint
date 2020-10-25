# -*- coding: utf-8 -*-
# Copyright (c) 2014-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 Michal Nowikowski <godfryd@gmail.com>
# Copyright (c) 2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Lucas Cimon <lucas.cimon@gmail.com>
# Copyright (c) 2018 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2019-2020 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Mr. Senko <atodorov@mrsenko.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 Damien Baty <damien.baty@polyconseil.fr>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2020 bernie gray <bfgray3@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Functional full-module tests for PyLint."""

import csv
import io
import os
import sys
import warnings
from pathlib import Path

import pytest

from pylint import testutils
from pylint.utils import HAS_ISORT_5


class test_dialect(csv.excel):
    delimiter = ":"
    lineterminator = "\n"


csv.register_dialect("test", test_dialect)


# Notes:
# - for the purpose of this test, the confidence levels HIGH and UNDEFINED
#   are treated as the same.

# TODOs
#  - implement exhaustivity tests

UPDATE = Path("pylint-functional-test-update")


class LintModuleOutputUpdate(testutils.LintModuleTest):
    """If message files should be updated instead of checked."""

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
            warnings.warn(
                "Updated '{}' with the new content generated from '{}'".format(
                    self._test_file.expected_output, self._test_file.base
                )
            )
            with open(self._test_file.expected_output, "w") as fobj:
                writer = csv.writer(fobj, dialect="test")
                for line in remaining:
                    writer.writerow(line.to_csv())


def get_tests():
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "functional")
    suite = []
    for dirpath, _, filenames in os.walk(input_dir):
        if dirpath.endswith("__pycache__"):
            continue
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


@pytest.mark.parametrize("test_file", TESTS, ids=TESTS_NAMES)
def test_functional(test_file):
    LintTest = (
        LintModuleOutputUpdate(test_file)
        if UPDATE.exists()
        else testutils.LintModuleTest(test_file)
    )
    LintTest.setUp()
    LintTest._runTest()


if __name__ == "__main__":
    if testutils.UPDATE_OPTION in sys.argv:
        UPDATE.touch()
        sys.argv.remove(testutils.UPDATE_OPTION)
    pytest.main(sys.argv)
    if UPDATE.exists():
        UPDATE.unlink()
