# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import csv
import os

from pylint.testutils.lint_module_test import LintModuleTest


class LintModuleOutputUpdate(LintModuleTest):
    """Class to be used if expected output files should be updated instead of
    checked.
    """

    class TestDialect(csv.excel):
        """Dialect used by the csv writer."""

        delimiter = ":"
        lineterminator = "\n"

    csv.register_dialect("test", TestDialect)

    def _runTest(self) -> None:
        """Overwrite or remove the expected output file based on actual output."""
        try:
            super()._runTest()
        finally:
            actual_messages, actual_output = self._get_actual()
            # Remove the expected file if no output is actually emitted and a file exists
            if not actual_output:
                if os.path.exists(self._test_file.expected_output):
                    os.remove(self._test_file.expected_output)
                return
            # Write file with expected output
            with open(self._test_file.expected_output, "w", encoding="utf-8") as f:
                writer = csv.writer(f, dialect="test")
                for line in actual_output:
                    writer.writerow(line.to_csv())
