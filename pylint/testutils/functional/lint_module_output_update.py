# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import csv
import os
import sys
from pathlib import Path

from pylint.testutils.lint_module_test import LintModuleTest, MessageCounter
from pylint.testutils.output_line import OutputLine


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
        """Overwrite or remove the expected output file based on actual output.

        When the resolved expected-output file is owned by an *older* Python
        version (e.g. ``foo.313.txt`` while running on Python 3.14), do not
        delete or overwrite it. Instead, write a new version-specific file
        for the current interpreter (``foo.314.txt``). This preserves the
        recorded expectations for older versions while letting the user
        record the new behaviour on the running version. See #10844.
        """
        expected_path = Path(self._test_file.expected_output)
        current_suffix = f"{sys.version_info[0]}{sys.version_info[1]}"
        target_path = self._target_path_for_current_version(
            expected_path, current_suffix
        )

        # Empty actual output: the running interpreter emits no diagnostics.
        if not actual_output:
            if target_path == expected_path:
                # The resolved file belongs to this Python version (or is
                # the version-less base file); preserve the historical
                # behaviour of removing it.
                if os.path.exists(expected_path):
                    os.remove(expected_path)
                return
            # The resolved file belongs to an older Python version. Don't
            # delete it — write an empty current-version file to shadow it
            # instead, so we record "no diagnostics on this version"
            # without erasing what older versions still expect.
            target_path.write_text("", encoding="utf-8")
            return

        # Non-empty actual output: write to the current version's file
        # (which may or may not be the resolved file).
        with open(target_path, "w", encoding="utf-8") as f:
            writer = csv.writer(f, dialect="test")
            for line in actual_output:
                self.safe_write_output_line(writer, line)

    def _target_path_for_current_version(
        self, expected_path: Path, current_suffix: str
    ) -> Path:
        """Return the file path we should write to for the current Python.

        If ``expected_path`` is the bare ``<base>.txt`` (no version suffix)
        or already matches the current version (``<base>.<current>.txt``),
        write to it directly. Otherwise the resolved file belongs to an
        older Python — return a sibling ``<base>.<current>.txt`` so we
        don't clobber the older version's expectations.
        """
        # ``self._test_file.base`` may be an absolute path (the legacy code
        # constructs ``FunctionalTestFile`` with the full filename as the
        # ``filename`` argument and strips ``.py`` from it). The actual
        # filename stem we need to compare against is just the trailing
        # path component.
        base_short = os.path.basename(self._test_file.base)
        # Examples:
        #   "foo.txt"         -> stem "foo"          -> file_suffix=""
        #   "foo.313.txt"     -> stem "foo.313"      -> file_suffix="313"
        # The base may itself contain dots (e.g. "sub.foo"), so we strip
        # the base prefix off the stem rather than splitting on "." blindly.
        stem = expected_path.stem  # filename without ".txt"
        if stem == base_short:
            file_suffix = ""
        else:
            prefix = f"{base_short}."
            # Defensively guard against unexpected layouts and fall through
            # to "no rewrite needed" if the stem doesn't start with the base.
            file_suffix = stem[len(prefix) :] if stem.startswith(prefix) else ""
        if file_suffix in ("", current_suffix):
            return expected_path
        return expected_path.with_name(f"{base_short}.{current_suffix}.txt")
