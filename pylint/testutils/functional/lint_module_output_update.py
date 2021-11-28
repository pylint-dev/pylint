# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import csv
import os

from pylint.testutils.lint_module_test import LintModuleTest


class LintModuleOutputUpdate(LintModuleTest):
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
