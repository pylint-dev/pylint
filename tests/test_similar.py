# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import os
import re
import warnings
from io import StringIO
from os.path import abspath, dirname, join
from typing import TextIO

import pytest

from pylint.reporters.text import TextReporter
from pylint.testutils._run import _Run as Run
from pylint.testutils.utils import _patch_streams

HERE = abspath(dirname(__file__))
DATA = join(HERE, "regrtest_data", "duplicate_code")
CLEAN_PATH = re.escape(dirname(dirname(__file__)) + os.path.sep)


class TestSymilarCodeChecker:
    def _runtest(self, args: list[str], code: int) -> None:
        """Runs the tests and sees if output code is as expected."""
        out = StringIO()
        pylint_code = self._run_pylint(args, out=out)
        output = out.getvalue()
        msg = f"expected output status {code}, got {pylint_code}"
        if output is not None:
            msg = f"{msg}. Below pylint output: \n{output}"
        assert pylint_code == code, msg

    @staticmethod
    def _run_pylint(args: list[str], out: TextIO) -> int:
        """Runs pylint with a patched output."""
        args += [
            "--persistent=no",
            "--enable=astroid-error",
            # Enable functionality that will build another ast
            "--ignore-imports=y",
            "--ignore-signatures=y",
        ]
        with _patch_streams(out):
            with pytest.raises(SystemExit) as cm:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    Run(args)
            return int(cm.value.code)

    @staticmethod
    def _clean_paths(output: str) -> str:
        """Normalize path to the tests directory."""
        output = re.sub(CLEAN_PATH, "", output, flags=re.MULTILINE)
        return output.replace("\\", "/")

    def _test_output(self, args: list[str], expected_output: str) -> None:
        """Tests if the output of a pylint run is as expected."""
        out = StringIO()
        self._run_pylint(args, out=out)
        actual_output = self._clean_paths(out.getvalue())
        actual_output_stripped = actual_output.strip()
        expected_output = self._clean_paths(expected_output)
        assert expected_output.strip() in actual_output_stripped
        assert "Fatal error" not in actual_output_stripped

    def test_duplicate_code_raw_strings_all(self) -> None:
        """Test similar lines in 3 similar files."""
        path = join(DATA, "raw_strings_all")
        expected_output = "Similar lines in 2 files"
        self._test_output(
            [
                path,
                "--disable=all",
                "--enable=duplicate-code",
                "--ignore-imports=no",
                "--ignore-signatures=no",
                "--min-similarity-lines=4",
            ],
            expected_output=expected_output,
        )

    @pytest.mark.needs_two_cores
    def test_duplicate_code_parallel(self) -> None:
        path = join(DATA, "raw_strings_all")
        expected_output = "Similar lines in 2 files"
        self._test_output(
            [
                path,
                "--disable=all",
                "--enable=duplicate-code",
                "--ignore-imports=no",
                "--ignore-signatures=no",
                "--min-similarity-lines=4",
                "--jobs=2",
            ],
            expected_output=expected_output,
        )

    def test_duplicate_code_raw_strings_disable_file(self) -> None:
        """Tests disabling duplicate-code at the file level in a single file."""
        path = join(DATA, "raw_strings_disable_file")
        expected_output = "Similar lines in 2 files"
        self._test_output(
            [
                path,
                "--disable=all",
                "--enable=duplicate-code",
                "--ignore-imports=no",
                "--ignore-signatures=no",
                "--min-similarity-lines=4",
            ],
            expected_output=expected_output,
        )

    def test_duplicate_code_raw_strings_disable_file_double(self) -> None:
        """Tests disabling duplicate-code at the file level in two files."""
        path = join(DATA, "raw_strings_disable_file_double")
        self._runtest(
            [
                path,
                "--disable=all",
                "--enable=duplicate-code",
                "--ignore-imports=no",
                "--ignore-signatures=no",
                "--min-similarity-lines=4",
            ],
            code=0,
        )

    def test_duplicate_code_raw_strings_disable_line_two(self) -> None:
        """Tests disabling duplicate-code at a line at the begin of a piece of similar code."""
        path = join(DATA, "raw_strings_disable_line_begin")
        expected_output = "Similar lines in 2 files"
        self._test_output(
            [
                path,
                "--disable=all",
                "--enable=duplicate-code",
                "--ignore-imports=no",
                "--ignore-signatures=no",
                "--min-similarity-lines=4",
            ],
            expected_output=expected_output,
        )

    def test_duplicate_code_raw_strings_disable_line_disable_all(self) -> None:
        """Tests disabling duplicate-code with all similar lines disabled per line."""
        path = join(DATA, "raw_strings_disable_line_disable_all")
        self._runtest(
            [
                path,
                "--disable=all",
                "--enable=duplicate-code",
                "--ignore-imports=no",
                "--ignore-signatures=no",
                "--min-similarity-lines=4",
            ],
            code=0,
        )

    def test_duplicate_code_raw_strings_disable_line_middle(self) -> None:
        """Tests disabling duplicate-code at a line in the middle of a piece of similar code."""
        path = join(DATA, "raw_strings_disable_line_middle")
        self._runtest(
            [
                path,
                "--disable=all",
                "--enable=duplicate-code",
                "--ignore-imports=no",
                "--ignore-signatures=no",
                "--min-similarity-lines=4",
            ],
            code=0,
        )

    def test_duplicate_code_raw_strings_disable_line_end(self) -> None:
        """Tests disabling duplicate-code at a line at the end of a piece of similar code."""
        path = join(DATA, "raw_strings_disable_line_end")
        expected_output = "Similar lines in 2 files"
        self._test_output(
            [
                path,
                "--disable=all",
                "--enable=duplicate-code",
                "--ignore-imports=no",
                "--ignore-signatures=no",
                "--min-similarity-lines=4",
            ],
            expected_output=expected_output,
        )

    def test_duplicate_code_raw_strings_disable_scope(self) -> None:
        """Tests disabling duplicate-code at an inner scope level."""
        path = join(DATA, "raw_strings_disable_scope")
        expected_output = "Similar lines in 2 files"
        self._test_output(
            [
                path,
                "--disable=all",
                "--enable=duplicate-code",
                "--ignore-imports=no",
                "--ignore-signatures=no",
                "--min-similarity-lines=4",
            ],
            expected_output=expected_output,
        )

    def test_duplicate_code_raw_strings_disable_scope_double(self) -> None:
        """Tests disabling duplicate-code at an inner scope level in two files."""
        path = join(DATA, "raw_strings_disable_scope_double")
        self._runtest(
            [
                path,
                "--disable=all",
                "--enable=duplicate-code",
                "--ignore-imports=no",
                "--ignore-signatures=no",
                "--min-similarity-lines=4",
            ],
            code=0,
        )

    def test_duplicate_code_raw_strings_disable_scope_function(self) -> None:
        """Tests disabling duplicate-code at an inner scope level with another scope with
        similarity.
        """
        path = join(DATA, "raw_strings_disable_scope_second_function")
        expected_output = "Similar lines in 2 files"
        self._test_output(
            [
                path,
                "--disable=all",
                "--enable=duplicate-code",
                "--ignore-imports=no",
                "--ignore-signatures=no",
                "--min-similarity-lines=4",
            ],
            expected_output=expected_output,
        )

    def test_ignore_imports(self) -> None:
        """Tests enabling ignore-imports works correctly."""
        path = join(DATA, "ignore_imports")
        self._runtest(
            [path, "-e=duplicate-code", "-d=unused-import,C", "--ignore-imports=y"],
            code=0,
        )

    @staticmethod
    def test_useless_suppression() -> None:
        """Tests that duplicate code and useless-suppression work well together."""
        path = join(DATA, "useless_suppression")
        pylint_output = StringIO()
        reporter = TextReporter(pylint_output)
        runner = Run(
            [
                path,
                "-e=duplicate-code, useless-suppression",
                "-d=missing-module-docstring, unused-import",
            ],
            reporter=reporter,
            exit=False,
        )
        assert not runner.linter.stats.by_msg

    def test_conditional_imports(self) -> None:
        """Tests enabling ignore-imports with conditional imports works correctly."""
        path = join(DATA, "ignore_conditional_imports")
        expected_output = "==ignore_conditional_imports.file_one:[2:4]"
        self._test_output(
            [
                path,
                "-e=duplicate-code",
                "-d=unused-import,C",
                "--ignore-imports=y",
                "--min-similarity-lines=1",
            ],
            expected_output=expected_output,
        )
