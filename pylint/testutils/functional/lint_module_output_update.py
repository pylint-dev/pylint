# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import csv
import os
import re

from pylint.testutils.lint_module_test import LintModuleTest, MessageCounter
from pylint.testutils.output_line import OutputLine

# Like 'name.314.txt', the expected output for Python 3.14 and later
VERSION_SPECIFIC_OUTPUT = re.compile(r"\.\d+\.txt$")


class LintModuleOutputUpdate(LintModuleTest):
    """Class to be used if expected output files should be updated instead of
    checked.
    """

    class TestDialect(csv.excel):
        """Dialect used by the csv writer."""

        delimiter = ":"
        lineterminator = "\n"

    csv.register_dialect("test", TestDialect)

    def _check_output_text(
        self,
        _: MessageCounter,
        expected_output: list[OutputLine],
        actual_output: list[OutputLine],
    ) -> None:
        """Overwrite or remove the expected output file based on actual output."""
        # Remove the expected file if no output is actually emitted and a file exists
        if not actual_output:
            if os.path.exists(self._test_file.expected_output):
                if VERSION_SPECIFIC_OUTPUT.search(self._test_file.expected_output):
                    # It overrides the output of older interpreters, keep it empty
                    with open(self._test_file.expected_output, "w", encoding="utf-8"):
                        pass
                else:
                    os.remove(self._test_file.expected_output)
            return
        # Write file with expected output
        with open(self._test_file.expected_output, "w", encoding="utf-8") as f:
            writer = csv.writer(f, dialect="test")
            for line in actual_output:
                self.safe_write_output_line(writer, line)
