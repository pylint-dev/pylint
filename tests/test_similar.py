# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import contextlib
import os
import re
import sys
import warnings
from io import StringIO
from os.path import abspath, dirname, join
from typing import Iterator, List, TextIO

import pytest

from pylint.lint import Run

HERE = abspath(dirname(__file__))
DATA = join(HERE, "regrtest_data", "duplicate_code")
CLEAN_PATH = re.escape(dirname(dirname(__file__)) + os.path.sep)


@contextlib.contextmanager
def _patch_streams(out: TextIO) -> Iterator:
    sys.stderr = sys.stdout = out
    try:
        yield
    finally:
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__


class TestSimilarCodeChecker:
    def _runtest(self, args: List[str], code: int) -> None:
        """Runs the tests and sees if output code is as expected."""
        out = StringIO()
        pylint_code = self._run_pylint(args, out=out)
        output = out.getvalue()
        msg = f"expected output status {code}, got {pylint_code}"
        if output is not None:
            msg = f"{msg}. Below pylint output: \n{output}"
        assert pylint_code == code, msg

    @staticmethod
    def _run_pylint(args: List[str], out: TextIO) -> int:
        """Runs pylint with a patched output."""
        args = args + ["--persistent=no"]
        with _patch_streams(out):
            with pytest.raises(SystemExit) as cm:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    Run(args)
            return cm.value.code

    @staticmethod
    def _clean_paths(output: str) -> str:
        """Normalize path to the tests directory."""
        output = re.sub(CLEAN_PATH, "", output, flags=re.MULTILINE)
        return output.replace("\\", "/")

    def _test_output(self, args: List[str], expected_output: str) -> None:
        """Tests if the output of a pylint run is as expected."""
        out = StringIO()
        self._run_pylint(args, out=out)
        actual_output = self._clean_paths(out.getvalue())
        expected_output = self._clean_paths(expected_output)
        assert expected_output.strip() in actual_output.strip()

    def test_duplicate_code_raw_strings_all(self) -> None:
        """Test similar lines in 3 similar files."""
        path = join(DATA, "raw_strings_all")
        expected_output = "Similar lines in 2 files"
        self._test_output(
            [path, "--disable=all", "--enable=duplicate-code"],
            expected_output=expected_output,
        )

    def test_duplicate_code_raw_strings_disable_file(self) -> None:
        """Tests disabling duplicate-code at the file level in a single file."""
        path = join(DATA, "raw_strings_disable_file")
        expected_output = "Similar lines in 2 files"
        self._test_output(
            [path, "--disable=all", "--enable=duplicate-code"],
            expected_output=expected_output,
        )

    def test_duplicate_code_raw_strings_disable_file_double(self) -> None:
        """Tests disabling duplicate-code at the file level in two files."""
        path = join(DATA, "raw_strings_disable_file_double")
        self._runtest([path, "--disable=all", "--enable=duplicate-code"], code=0)

    def test_duplicate_code_raw_strings_disable_line_two(self) -> None:
        """Tests disabling duplicate-code at a line at the begin of a piece of similar code."""
        path = join(DATA, "raw_strings_disable_line_begin")
        expected_output = "Similar lines in 2 files"
        self._test_output(
            [path, "--disable=all", "--enable=duplicate-code"],
            expected_output=expected_output,
        )

    def test_duplicate_code_raw_strings_disable_line_disable_all(self) -> None:
        """Tests disabling duplicate-code with all similar lines disabled per line."""
        path = join(DATA, "raw_strings_disable_line_disable_all")
        self._runtest([path, "--disable=all", "--enable=duplicate-code"], code=0)

    def test_duplicate_code_raw_strings_disable_line_midle(self) -> None:
        """Tests disabling duplicate-code at a line in the middle of a piece of similar code."""
        path = join(DATA, "raw_strings_disable_line_middle")
        self._runtest([path, "--disable=all", "--enable=duplicate-code"], code=0)

    def test_duplicate_code_raw_strings_disable_line_end(self) -> None:
        """Tests disabling duplicate-code at a line at the end of a piece of similar code."""
        path = join(DATA, "raw_strings_disable_line_end")
        expected_output = "Similar lines in 2 files"
        self._test_output(
            [path, "--disable=all", "--enable=duplicate-code"],
            expected_output=expected_output,
        )

    def test_duplicate_code_raw_strings_disable_scope(self) -> None:
        """Tests disabling duplicate-code at an inner scope level."""
        path = join(DATA, "raw_strings_disable_scope")
        expected_output = "Similar lines in 2 files"
        self._test_output(
            [path, "--disable=all", "--enable=duplicate-code"],
            expected_output=expected_output,
        )

    def test_duplicate_code_raw_strings_disable_scope_double(self) -> None:
        """Tests disabling duplicate-code at an inner scope level in two files."""
        path = join(DATA, "raw_strings_disable_scope_double")
        self._runtest([path, "--disable=all", "--enable=duplicate-code"], code=0)

    def test_duplicate_code_raw_strings_disable_scope_function(self) -> None:
        """Tests disabling duplicate-code at an inner scope level with another scope with similarity."""
        path = join(DATA, "raw_strings_disable_scope_second_function")
        expected_output = "Similar lines in 2 files"
        self._test_output(
            [path, "--disable=all", "--enable=duplicate-code"],
            expected_output=expected_output,
        )
