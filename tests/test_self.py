# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

# pylint: disable=too-many-public-methods

from __future__ import annotations

import configparser
import contextlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import textwrap
import warnings
from collections.abc import Iterator
from copy import copy
from io import BytesIO, StringIO
from os.path import abspath, dirname, join
from pathlib import Path
from typing import TYPE_CHECKING, Any, TextIO
from unittest import mock
from unittest.mock import patch

import pytest

from pylint import extensions, modify_sys_path
from pylint.constants import MAIN_CHECKER_NAME, MSG_TYPES_STATUS
from pylint.lint.pylinter import PyLinter
from pylint.message import Message
from pylint.reporters import BaseReporter, JSONReporter
from pylint.reporters.text import ColorizedTextReporter, TextReporter
from pylint.testutils._run import _add_rcfile_default_pylintrc
from pylint.testutils._run import _Run as Run
from pylint.testutils.utils import (
    _patch_streams,
    _test_cwd,
    _test_environ_pythonpath,
    _test_sys_path,
)
from pylint.utils import utils

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


if TYPE_CHECKING:
    from pylint.reporters.ureports.nodes import Section

HERE = abspath(dirname(__file__))
CLEAN_PATH = re.escape(dirname(dirname(__file__)) + os.path.sep)
UNNECESSARY_LAMBDA = join(
    HERE, "functional", "u", "unnecessary", "unnecessary_lambda.py"
)


@contextlib.contextmanager
def _configure_lc_ctype(lc_ctype: str) -> Iterator[None]:
    lc_ctype_env = "LC_CTYPE"
    original_lctype = os.environ.get(lc_ctype_env)
    os.environ[lc_ctype_env] = lc_ctype
    try:
        yield
    finally:
        os.environ.pop(lc_ctype_env)
        if original_lctype:
            os.environ[lc_ctype_env] = original_lctype


class MultiReporter(BaseReporter):
    def __init__(self, reporters: list[BaseReporter]) -> None:
        # pylint: disable=super-init-not-called
        # We don't call it because there is an attribute "linter" that is set inside the base class,
        # and we have another setter here using yet undefined attribute.
        # I don't think fixing the init order in a test class used once is worth it.
        self._reporters = reporters
        self.path_strip_prefix = os.getcwd() + os.sep

    def on_set_current_module(self, *args: str, **kwargs: Any) -> None:
        for rep in self._reporters:
            rep.on_set_current_module(*args, **kwargs)

    def handle_message(self, msg: Message) -> None:
        for rep in self._reporters:
            rep.handle_message(msg)

    def _display(self, layout: Section) -> None:
        pass

    @property
    def out(self) -> TextIO:  # type: ignore[override]
        return self._reporters[0].out

    @property
    def linter(self) -> PyLinter:
        return self._linter

    @linter.setter
    def linter(self, value: PyLinter) -> None:
        self._linter = value
        for rep in self._reporters:
            rep.linter = value


class TestRunTC:
    def _runtest(
        self,
        args: list[str],
        reporter: Any = None,
        out: StringIO | None = None,
        code: int | None = None,
    ) -> None:
        if out is None:
            out = StringIO()
        args = _add_rcfile_default_pylintrc(args)
        pylint_code = self._run_pylint(args, reporter=reporter, out=out)
        if reporter:
            output = reporter.out.getvalue()
        elif hasattr(out, "getvalue"):
            output = out.getvalue()
        else:
            output = None
        msg = f"expected output status {code}, got {pylint_code}"
        if output is not None:
            msg = f"{msg}. Below pylint output: \n{output}"
        assert pylint_code == code, msg

    @staticmethod
    def _run_pylint(args: list[str], out: TextIO, reporter: Any = None) -> int:
        args = _add_rcfile_default_pylintrc([*args, "--persistent=no"])
        with _patch_streams(out):
            with pytest.raises(SystemExit) as cm:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    Run(args, reporter=reporter)
            return int(cm.value.code)

    @staticmethod
    def _clean_paths(output: str) -> str:
        """Normalize path to the tests directory."""
        output = re.sub(CLEAN_PATH, "", output, flags=re.MULTILINE)
        return output.replace("\\", "/")

    def _test_output(
        self, args: list[str], expected_output: str, unexpected_output: str = ""
    ) -> None:
        out = StringIO()
        args = _add_rcfile_default_pylintrc(args)
        self._run_pylint(args, out=out)
        actual_output = self._clean_paths(out.getvalue())
        expected_output = self._clean_paths(expected_output)
        assert expected_output.strip() in actual_output.strip()

        if unexpected_output:
            assert unexpected_output.strip() not in actual_output.strip()

    def _test_output_file(
        self, args: list[str], filename: Path, expected_output: str
    ) -> None:
        """Run Pylint with the ``output`` option set (must be included in
        the ``args`` passed to this method!) and check the file content afterwards.
        """
        out = StringIO()
        args = _add_rcfile_default_pylintrc(args)
        self._run_pylint(args, out=out)
        cmdline_output = out.getvalue()
        file_output = self._clean_paths(Path(filename).read_text(encoding="utf-8"))
        expected_output = self._clean_paths(expected_output)
        assert (
            cmdline_output == ""
        ), "Unexpected output to stdout/stderr while output option was set"
        assert expected_output.strip() in file_output.strip()

    def test_pkginfo(self) -> None:
        """Make pylint check 'pylint.__pkginfo__.py'."""
        # Disable invalid-name because of invalid argument names
        args = ["pylint.__pkginfo__", "--disable=invalid-name"]
        self._runtest(args, reporter=TextReporter(StringIO()), code=0)

    def test_all(self) -> None:
        """Make pylint check itself."""
        reporters = [
            TextReporter(StringIO()),
            ColorizedTextReporter(StringIO()),
            JSONReporter(StringIO()),
        ]
        self._runtest(
            [join(HERE, "functional", "a", "arguments.py")],
            reporter=MultiReporter(reporters),
            code=2,
        )

    def test_no_ext_file(self) -> None:
        self._runtest([join(HERE, "input", "noext")], code=0)

    def test_w0704_ignored(self) -> None:
        self._runtest([join(HERE, "input", "ignore_except_pass_by_default.py")], code=0)

    def test_exit_zero(self) -> None:
        self._runtest(
            ["--exit-zero", join(HERE, "regrtest_data", "syntax_error.py")], code=0
        )

    def test_nonexistent_config_file(self) -> None:
        self._runtest(["--rcfile=/tmp/this_file_does_not_exist"], code=32)

    def test_error_missing_arguments(self) -> None:
        self._runtest([], code=32)

    def test_no_out_encoding(self) -> None:
        """Test redirection of stdout with non ascii characters."""
        # This test reproduces bug #48066 ; it happens when stdout is redirected
        # through '>' : the sys.stdout.encoding becomes then None, and if the
        # output contains non ascii, pylint will crash
        strio = StringIO()
        assert strio.encoding is None
        self._runtest(
            [join(HERE, "regrtest_data", "no_stdout_encoding.py"), "--enable=all"],
            out=strio,
            code=28,
        )

    def test_parallel_execution(self) -> None:
        out = StringIO()
        self._runtest(
            [
                "-j 2",
                join(HERE, "functional", "a", "arguments.py"),
            ],
            out=out,
            # We expect similarities to fail and an error
            code=MSG_TYPES_STATUS["E"],
        )
        assert (
            "Unexpected keyword argument 'fourth' in function call"
            in out.getvalue().strip()
        )

    def test_parallel_execution_missing_arguments(self) -> None:
        self._runtest(["-j 2", "not_here", "not_here_too"], code=1)

    # TODO: PY3.7: Turn off abbreviations in ArgumentsManager after 3.7 support has been dropped
    # argparse changed behaviour with abbreviations on/off in 3.8+ so we can't
    @pytest.mark.xfail
    def test_abbreviations_are_not_supported(self) -> None:
        expected = "No module named --load-plugin"
        self._test_output([".", "--load-plugin"], expected_output=expected)

    def test_enable_all_works(self) -> None:
        module = join(HERE, "data", "clientmodule_test.py")
        expected = textwrap.dedent(
            f"""
        ************* Module data.clientmodule_test
        {module}:9:8: W0612: Unused variable 'local_variable' (unused-variable)
        {module}:17:4: C0116: Missing function or method docstring (missing-function-docstring)
        {module}:21:0: C0115: Missing class docstring (missing-class-docstring)
        """
        )
        self._test_output(
            [module, "--disable=all", "--enable=all", "-rn"], expected_output=expected
        )

    def test_wrong_import_position_when_others_disabled(self) -> None:
        module1 = join(HERE, "regrtest_data", "import_something.py")
        module2 = join(HERE, "regrtest_data", "wrong_import_position.py")
        expected_output = textwrap.dedent(
            f"""
        ************* Module wrong_import_position
        {module2}:11:0: C0413: Import "import os" should be placed at the top of the module (wrong-import-position)
        """
        )
        args = [
            module2,
            module1,
            "--disable=all",
            "--enable=wrong-import-position",
            "-rn",
            "-sn",
        ]
        out = StringIO()
        self._run_pylint(args, out=out)
        actual_output = self._clean_paths(out.getvalue().strip())

        to_remove = "No config file found, using default configuration"
        if to_remove in actual_output:
            actual_output = actual_output[len(to_remove) :]
        if actual_output.startswith("Using config file "):
            # If ~/.pylintrc is present remove the
            # Using config file...  line
            actual_output = actual_output[actual_output.find("\n") :]
        assert self._clean_paths(expected_output.strip()) == actual_output.strip()

    def test_type_annotation_names(self) -> None:
        """Test resetting the `_type_annotation_names` list to `[]` when leaving a module.

        An import inside `module_a`, which is used as a type annotation in `module_a`, should not prevent
        emitting the `unused-import` message when the same import occurs in `module_b` & is unused.
        See: https://github.com/PyCQA/pylint/issues/4150
        """
        module1 = join(
            HERE, "regrtest_data", "imported_module_in_typehint", "module_a.py"
        )

        module2 = join(
            HERE, "regrtest_data", "imported_module_in_typehint", "module_b.py"
        )
        expected_output = textwrap.dedent(
            f"""
        ************* Module module_b
        {module2}:1:0: W0611: Unused import uuid (unused-import)
        """
        )
        args = [
            module1,
            module2,
            "--disable=all",
            "--enable=unused-import",
            "-rn",
            "-sn",
        ]
        out = StringIO()
        self._run_pylint(args, out=out)
        actual_output = self._clean_paths(out.getvalue().strip())
        assert self._clean_paths(expected_output.strip()) in actual_output.strip()

    def test_import_itself_not_accounted_for_relative_imports(self) -> None:
        expected = "Your code has been rated at 10.00/10"
        package = join(HERE, "regrtest_data", "dummy")
        self._test_output(
            [package, "--disable=locally-disabled", "-rn"], expected_output=expected
        )

    def test_reject_empty_indent_strings(self) -> None:
        expected = "Option cannot be an empty string"
        module = join(HERE, "data", "clientmodule_test.py")
        self._test_output([module, "--indent-string="], expected_output=expected)

    def test_json_report_when_file_has_syntax_error(self) -> None:
        out = StringIO()
        module = join(HERE, "regrtest_data", "syntax_error.py")
        self._runtest([module], code=2, reporter=JSONReporter(out))
        output = json.loads(out.getvalue())
        assert isinstance(output, list)
        assert len(output) == 1
        assert isinstance(output[0], dict)
        # So each version wants a different column number...
        if platform.python_implementation() == "PyPy":
            column = 9
        elif sys.version_info >= (3, 8):
            column = 9
        else:
            column = 15
        expected = {
            "obj": "",
            "column": column,
            "line": 1,
            "type": "error",
            "symbol": "syntax-error",
            "module": "syntax_error",
        }
        message = output[0]
        for key, value in expected.items():
            assert key in message
            assert message[key] == value
        msg = message["message"].lower()
        assert any(x in msg for x in ("expected ':'", "invalid syntax"))
        assert "<unknown>" in msg
        assert "line 1" in msg

    def test_json_report_when_file_is_missing(self) -> None:
        out = StringIO()
        module = join(HERE, "regrtest_data", "totally_missing.py")
        self._runtest([module], code=1, reporter=JSONReporter(out))
        output = json.loads(out.getvalue())
        assert isinstance(output, list)
        assert len(output) == 1
        assert isinstance(output[0], dict)
        expected = {
            "obj": "",
            "column": 0,
            "line": 1,
            "type": "fatal",
            "symbol": "fatal",
            "module": module,
        }
        message = output[0]
        for key, value in expected.items():
            assert key in message
            assert message[key] == value
        assert message["message"].startswith("No module named")

    def test_json_report_does_not_escape_quotes(self) -> None:
        out = StringIO()
        module = join(HERE, "regrtest_data", "unused_variable.py")
        self._runtest([module], code=4, reporter=JSONReporter(out))
        output = json.loads(out.getvalue())
        assert isinstance(output, list)
        assert len(output) == 1
        assert isinstance(output[0], dict)
        expected = {
            "symbol": "unused-variable",
            "module": "unused_variable",
            "column": 4,
            "message": "Unused variable 'variable'",
            "message-id": "W0612",
            "line": 4,
            "type": "warning",
        }
        message = output[0]
        for key, value in expected.items():
            assert key in message
            assert message[key] == value

    def test_information_category_disabled_by_default(self) -> None:
        expected = "Your code has been rated at 10.00/10"
        path = join(HERE, "regrtest_data", "meta.py")
        self._test_output([path], expected_output=expected)

    def test_error_mode_shows_no_score(self) -> None:
        module = join(HERE, "regrtest_data", "application_crash.py")
        expected_output = textwrap.dedent(
            f"""
        ************* Module application_crash
        {module}:1:6: E0602: Undefined variable 'something_undefined' (undefined-variable)
        """
        )
        self._test_output([module, "-E"], expected_output=expected_output)

    def test_evaluation_score_shown_by_default(self) -> None:
        expected_output = "Your code has been rated at "
        module = join(HERE, "regrtest_data", "application_crash.py")
        self._test_output([module], expected_output=expected_output)

    def test_confidence_levels(self) -> None:
        expected = "Your code has been rated at"
        path = join(HERE, "regrtest_data", "meta.py")
        self._test_output(
            [path, "--confidence=HIGH,INFERENCE"], expected_output=expected
        )

    def test_bom_marker(self) -> None:
        path = join(HERE, "regrtest_data", "meta.py")
        expected = "Your code has been rated at 10.00/10"
        self._test_output([path, "-rn"], expected_output=expected)

    def test_pylintrc_plugin_duplicate_options(self) -> None:
        dummy_plugin_path = join(HERE, "regrtest_data", "dummy_plugin")
        # Enable --load-plugins=dummy_plugin
        sys.path.append(dummy_plugin_path)
        config_path = join(HERE, "regrtest_data", "dummy_plugin.rc")
        expected = (
            ":dummy-message-01 (I9061): *Dummy short desc 01*\n"
            "  Dummy long desc This message belongs to the dummy_plugin checker.\n\n"
            ":dummy-message-02 (I9060): *Dummy short desc 02*\n"
            "  Dummy long desc This message belongs to the dummy_plugin checker."
        )
        self._test_output(
            [
                f"--rcfile={config_path}",
                "--help-msg",
                "dummy-message-01",
                "dummy-message-02",
            ],
            expected_output=expected,
        )
        expected = (
            "[DUMMY_PLUGIN]\n\n# Dummy option 1\ndummy_option_1=dummy value 1\n\n"
            "# Dummy option 2\ndummy_option_2=dummy value 2"
        )
        self._test_output(
            [f"--rcfile={config_path}", "--generate-rcfile"], expected_output=expected
        )
        sys.path.remove(dummy_plugin_path)

    def test_pylintrc_comments_in_values(self) -> None:
        path = join(HERE, "regrtest_data", "test_pylintrc_comments.py")
        config_path = join(HERE, "regrtest_data", "comments_pylintrc")
        expected = textwrap.dedent(
            f"""
        ************* Module test_pylintrc_comments
        {path}:2:0: W0311: Bad indentation. Found 1 spaces, expected 4 (bad-indentation)
        {path}:1:0: C0114: Missing module docstring (missing-module-docstring)
        {path}:1:0: C0116: Missing function or method docstring (missing-function-docstring)
        """
        )
        self._test_output(
            [path, f"--rcfile={config_path}", "-rn"], expected_output=expected
        )

    def test_no_crash_with_formatting_regex_defaults(self) -> None:
        self._runtest(
            ["--ignore-patterns=a"], reporter=TextReporter(StringIO()), code=32
        )

    def test_getdefaultencoding_crashes_with_lc_ctype_utf8(self) -> None:
        module = join(HERE, "regrtest_data", "application_crash.py")
        expected_output = textwrap.dedent(
            f"""
        {module}:1:6: E0602: Undefined variable 'something_undefined' (undefined-variable)
        """
        )
        with _configure_lc_ctype("UTF-8"):
            self._test_output([module, "-E"], expected_output=expected_output)

    @pytest.mark.skipif(sys.platform == "win32", reason="only occurs on *nix")
    def test_parseable_file_path(self) -> None:
        file_name = "test_target.py"
        fake_path = HERE + os.getcwd()
        module = join(fake_path, file_name)

        try:
            # create module under directories which have the same name as reporter.path_strip_prefix
            # e.g. /src/some/path/src/test_target.py when reporter.path_strip_prefix = /src/
            os.makedirs(fake_path)
            with open(module, "w", encoding="utf-8") as test_target:
                test_target.write("a,b = object()")

            self._test_output(
                [module, "--output-format=parseable"], expected_output=file_name
            )
        finally:
            os.remove(module)
            os.removedirs(fake_path)

    @pytest.mark.parametrize(
        "input_path,module,expected_path",
        [
            (join(HERE, "mymodule.py"), "mymodule", join(HERE, "mymodule.py")),
            ("mymodule.py", "mymodule", "mymodule.py"),
        ],
    )
    def test_stdin(self, input_path: str, module: str, expected_path: str) -> None:
        expected_output = f"""************* Module {module}
{expected_path}:1:0: W0611: Unused import os (unused-import)

"""

        with mock.patch(
            "pylint.lint.pylinter._read_stdin", return_value="import os\n"
        ) as mock_stdin:
            self._test_output(
                ["--from-stdin", input_path, "--disable=all", "--enable=unused-import"],
                expected_output=expected_output,
            )
            assert mock_stdin.call_count == 1

    def test_stdin_missing_modulename(self) -> None:
        self._runtest(["--from-stdin"], code=32)

    @pytest.mark.parametrize("write_bpy_to_disk", [False, True])
    def test_relative_imports(self, write_bpy_to_disk: bool, tmp_path: Path) -> None:
        a = tmp_path / "a"

        b_code = textwrap.dedent(
            """
            from .c import foobar
            from .d import bla  # module does not exist

            foobar('hello')
            bla()
            """
        )

        c_code = textwrap.dedent(
            """
            def foobar(arg):
                pass
            """
        )

        a.mkdir()
        (a / "__init__.py").write_text("")
        if write_bpy_to_disk:
            (a / "b.py").write_text(b_code)
        (a / "c.py").write_text(c_code)

        with _test_cwd(tmp_path):
            # why don't we start pylint in a sub-process?
            expected = (
                "************* Module a.b\n"
                "a/b.py:3:0: E0401: Unable to import 'a.d' (import-error)\n\n"
            )

            if write_bpy_to_disk:
                # --from-stdin is not used here
                self._test_output(
                    ["a/b.py", "--disable=all", "--enable=import-error"],
                    expected_output=expected,
                )

            # this code needs to work w/ and w/o a file named a/b.py on the hard disk.
            with mock.patch("pylint.lint.pylinter._read_stdin", return_value=b_code):
                self._test_output(
                    [
                        "--from-stdin",
                        join("a", "b.py"),
                        "--disable=all",
                        "--enable=import-error",
                    ],
                    expected_output=expected,
                )

    def test_stdin_syntax_error(self) -> None:
        expected_output = """************* Module a
a.py:1:4: E0001: Parsing failed: 'invalid syntax (<unknown>, line 1)' (syntax-error)"""
        with mock.patch(
            "pylint.lint.pylinter._read_stdin", return_value="for\n"
        ) as mock_stdin:
            self._test_output(
                ["--from-stdin", "a.py", "--disable=all", "--enable=syntax-error"],
                expected_output=expected_output,
            )
            assert mock_stdin.call_count == 1

    def test_version(self) -> None:
        def check(lines: list[str]) -> None:
            assert lines[0].startswith("pylint ")
            assert lines[1].startswith("astroid ")
            assert lines[2].startswith("Python ")

        out = StringIO()
        self._run_pylint(["--version"], out=out)
        check(out.getvalue().splitlines())

        result = subprocess.check_output([sys.executable, "-m", "pylint", "--version"])
        result_str = result.decode("utf-8")
        check(result_str.splitlines())

    def test_fail_under(self) -> None:
        self._runtest(
            [
                "--fail-under",
                "-10",
                "--enable=all",
                join(HERE, "regrtest_data", "fail_under_plus7_5.py"),
            ],
            code=0,
        )
        self._runtest(
            [
                "--fail-under",
                "6",
                "--enable=all",
                join(HERE, "regrtest_data", "fail_under_plus7_5.py"),
            ],
            code=0,
        )
        self._runtest(
            [
                "--fail-under",
                "7.5",
                "--enable=all",
                join(HERE, "regrtest_data", "fail_under_plus7_5.py"),
            ],
            code=0,
        )
        self._runtest(
            [
                "--fail-under",
                "7.6",
                "--enable=all",
                join(HERE, "regrtest_data", "fail_under_plus7_5.py"),
            ],
            code=16,
        )

        self._runtest(
            [
                "--fail-under",
                "-11",
                "--enable=all",
                join(HERE, "regrtest_data", "fail_under_minus10.py"),
            ],
            code=0,
        )
        self._runtest(
            [
                "--fail-under",
                "-10",
                "--enable=all",
                join(HERE, "regrtest_data", "fail_under_minus10.py"),
            ],
            code=0,
        )
        # Need the old evaluation formula to test a negative score
        # failing below a negative --fail-under threshold
        self._runtest(
            [
                "--fail-under",
                "-9",
                "--enable=all",
                "--evaluation",
                "0 if fatal else 10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10)",
                join(HERE, "regrtest_data", "fail_under_minus10.py"),
            ],
            code=22,
        )
        self._runtest(
            [
                "--fail-under",
                "-5",
                "--enable=all",
                "--evaluation",
                "0 if fatal else 10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10)",
                join(HERE, "regrtest_data", "fail_under_minus10.py"),
            ],
            code=22,
        )

    @pytest.mark.parametrize(
        "fu_score,fo_msgs,fname,out",
        [
            # Essentially same test cases as --fail-under, but run with/without a detected
            # issue code missing-function-docstring (C0116) is issue in both files
            # --fail-under should be irrelevant as missing-function-docstring is hit
            (-10, "missing-function-docstring", "fail_under_plus7_5.py", 16),
            (6, "missing-function-docstring", "fail_under_plus7_5.py", 16),
            (7.5, "missing-function-docstring", "fail_under_plus7_5.py", 16),
            (7.6, "missing-function-docstring", "fail_under_plus7_5.py", 16),
            (-11, "missing-function-docstring", "fail_under_minus10.py", 22),
            (-10, "missing-function-docstring", "fail_under_minus10.py", 22),
            (-9, "missing-function-docstring", "fail_under_minus10.py", 22),
            (-5, "missing-function-docstring", "fail_under_minus10.py", 22),
            # --fail-under should guide whether error code as missing-function-docstring is not hit
            (-10, "broad-exception-caught", "fail_under_plus7_5.py", 0),
            (6, "broad-exception-caught", "fail_under_plus7_5.py", 0),
            (7.5, "broad-exception-caught", "fail_under_plus7_5.py", 0),
            (7.6, "broad-exception-caught", "fail_under_plus7_5.py", 16),
            (-11, "broad-exception-caught", "fail_under_minus10.py", 0),
            (-10, "broad-exception-caught", "fail_under_minus10.py", 0),
            (-9, "broad-exception-caught", "fail_under_minus10.py", 22),
            (-5, "broad-exception-caught", "fail_under_minus10.py", 22),
            # Enable by message id
            (-10, "C0116", "fail_under_plus7_5.py", 16),
            # Enable by category
            (-10, "C", "fail_under_plus7_5.py", 16),
            (-10, "fake1,C,fake2", "fail_under_plus7_5.py", 16),
            # Ensure entire category not enabled by any msg id
            (-10, "C0115", "fail_under_plus7_5.py", 0),
        ],
    )
    def test_fail_on(self, fu_score: int, fo_msgs: str, fname: str, out: int) -> None:
        self._runtest(
            [
                "--fail-under",
                f"{fu_score:f}",
                f"--fail-on={fo_msgs}",
                "--enable=all",
                join(HERE, "regrtest_data", fname),
                # Use the old form of the evaluation that can go negative
                "--evaluation",
                "0 if fatal else 10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10)",
            ],
            code=out,
        )

    @pytest.mark.parametrize(
        "opts,out",
        [
            # Special case to ensure that disabled items from category aren't enabled
            (["--disable=C0116", "--fail-on=C"], 0),
            # Ensure order does not matter
            (["--fail-on=C", "--disable=C0116"], 0),
            # Ensure --fail-on takes precedence over --disable
            (["--disable=C0116", "--fail-on=C0116"], 16),
            # Ensure order does not matter
            (["--fail-on=C0116", "--disable=C0116"], 16),
        ],
    )
    def test_fail_on_edge_case(self, opts: list[str], out: int) -> None:
        self._runtest(
            [*opts, join(HERE, "regrtest_data", "fail_under_plus7_5.py")],
            code=out,
        )

    @staticmethod
    def test_modify_sys_path() -> None:
        # pylint: disable = too-many-statements
        cwd = "/tmp/pytest-of-root/pytest-0/test_do_not_import_files_from_0"
        default_paths = [
            "/usr/local/lib/python39.zip",
            "/usr/local/lib/python3.9",
            "/usr/local/lib/python3.9/lib-dynload",
            "/usr/local/lib/python3.9/site-packages",
        ]
        with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            paths = [cwd, *default_paths]
            sys.path = copy(paths)
            with _test_environ_pythonpath():
                modify_sys_path()
            assert sys.path == paths[1:]

            paths = ["", *default_paths]
            sys.path = copy(paths)
            with _test_environ_pythonpath():
                modify_sys_path()
            assert sys.path == paths[1:]

            paths = [".", *default_paths]
            sys.path = copy(paths)
            with _test_environ_pythonpath():
                modify_sys_path()
            assert sys.path == paths[1:]

            paths = ["/do_not_remove", *default_paths]
            sys.path = copy(paths)
            with _test_environ_pythonpath():
                modify_sys_path()
            assert sys.path == paths

            paths = [cwd, cwd, *default_paths]
            sys.path = copy(paths)
            with _test_environ_pythonpath("."):
                modify_sys_path()
            assert sys.path == paths[1:]

            paths = [cwd, "/custom_pythonpath", *default_paths]
            sys.path = copy(paths)
            with _test_environ_pythonpath("/custom_pythonpath"):
                modify_sys_path()
            assert sys.path == paths[1:]

            paths = [cwd, "/custom_pythonpath", cwd, *default_paths]
            sys.path = copy(paths)
            with _test_environ_pythonpath("/custom_pythonpath:"):
                modify_sys_path()
            assert sys.path == [paths[1]] + paths[3:]

            paths = ["", cwd, "/custom_pythonpath", *default_paths]
            sys.path = copy(paths)
            with _test_environ_pythonpath(":/custom_pythonpath"):
                modify_sys_path()
            assert sys.path == paths[2:]

            paths = [cwd, cwd, "/custom_pythonpath", *default_paths]
            sys.path = copy(paths)
            with _test_environ_pythonpath(":/custom_pythonpath:"):
                modify_sys_path()
            assert sys.path == paths[2:]

            paths = [cwd, cwd, *default_paths]
            sys.path = copy(paths)
            with _test_environ_pythonpath(":."):
                modify_sys_path()
            assert sys.path == paths[1:]
            sys.path = copy(paths)
            with _test_environ_pythonpath(f":{cwd}"):
                modify_sys_path()
            assert sys.path == paths[1:]

            sys.path = copy(paths)
            with _test_environ_pythonpath(".:"):
                modify_sys_path()
            assert sys.path == paths[1:]
            sys.path = copy(paths)
            with _test_environ_pythonpath(f"{cwd}:"):
                modify_sys_path()
            assert sys.path == paths[1:]

            paths = ["", cwd, *default_paths, cwd]
            sys.path = copy(paths)
            with _test_environ_pythonpath(cwd):
                modify_sys_path()
            assert sys.path == paths[1:]

    @staticmethod
    def test_plugin_that_imports_from_open() -> None:
        """Test that a plugin that imports a source file from a checker open()
        function (ala pylint_django) does not raise an exception."""
        with _test_sys_path():
            # Enable --load-plugins=importing_plugin
            sys.path.append(join(HERE, "regrtest_data", "importing_plugin"))
            with _test_cwd(join(HERE, "regrtest_data", "settings_project")):
                Run(
                    ["--load-plugins=importing_plugin", "models.py"],
                    exit=False,
                )

    @pytest.mark.parametrize(
        "args",
        [
            ["--disable=import-error,unused-import"],
            # Test with multiple jobs for 'hmac.py' for which we have a
            # CVE against: https://github.com/PyCQA/pylint/issues/959
            ["-j2", "--disable=import-error,unused-import"],
        ],
    )
    def test_do_not_import_files_from_local_directory(
        self, tmp_path: Path, args: list[str]
    ) -> None:
        for path in ("astroid.py", "hmac.py"):
            file_path = tmp_path / path
            file_path.write_text("'Docstring'\nimport completely_unknown\n")
            pylint_call = [sys.executable, "-m", "pylint", *args, path]
            with _test_cwd(tmp_path):
                subprocess.check_output(pylint_call, cwd=str(tmp_path))
            new_python_path = os.environ.get("PYTHONPATH", "").strip(":")
            with _test_cwd(tmp_path), _test_environ_pythonpath(f"{new_python_path}:"):
                # Appending a colon to PYTHONPATH should not break path stripping
                # https://github.com/PyCQA/pylint/issues/3636
                subprocess.check_output(pylint_call, cwd=str(tmp_path))

    @staticmethod
    def test_import_plugin_from_local_directory_if_pythonpath_cwd(
        tmp_path: Path,
    ) -> None:
        p_plugin = tmp_path / "plugin.py"
        p_plugin.write_text("# Some plugin content")
        if sys.platform == "win32":
            python_path = "."
        else:
            python_path = f"{os.environ.get('PYTHONPATH', '').strip(':')}:."
        with _test_cwd(tmp_path), _test_environ_pythonpath(python_path):
            args = [sys.executable, "-m", "pylint", "--load-plugins", "plugin"]
            process = subprocess.run(
                args, cwd=str(tmp_path), stderr=subprocess.PIPE, check=False
            )
            assert (
                "AttributeError: module 'plugin' has no attribute 'register'"
                in process.stderr.decode()
            )

    def test_allow_import_of_files_found_in_modules_during_parallel_check(
        self, tmp_path: Path
    ) -> None:
        test_directory = tmp_path / "test_directory"
        test_directory.mkdir()
        spam_module = test_directory / "spam.py"
        spam_module.write_text("'Empty'")

        init_module = test_directory / "__init__.py"
        init_module.write_text("'Empty'")

        # For multiple jobs we could not find the `spam.py` file.
        with _test_cwd(tmp_path):
            args = [
                "-j2",
                "--disable=missing-docstring, missing-final-newline",
                "test_directory",
            ]
            self._runtest(args, code=0)

        # A single job should be fine as well
        with _test_cwd(tmp_path):
            args = [
                "-j1",
                "--disable=missing-docstring, missing-final-newline",
                "test_directory",
            ]
            self._runtest(args, code=0)

    @staticmethod
    def test_can_list_directories_without_dunder_init(tmp_path: Path) -> None:
        test_directory = tmp_path / "test_directory"
        test_directory.mkdir()
        spam_module = test_directory / "spam.py"
        spam_module.write_text("'Empty'")

        subprocess.check_output(
            [
                sys.executable,
                "-m",
                "pylint",
                "--disable=missing-docstring, missing-final-newline",
                "test_directory",
            ],
            cwd=str(tmp_path),
            stderr=subprocess.PIPE,
        )

    @pytest.mark.needs_two_cores
    def test_jobs_score(self) -> None:
        path = join(HERE, "regrtest_data", "unused_variable.py")
        expected = "Your code has been rated at 7.50/10"
        self._test_output([path, "--jobs=2", "-ry"], expected_output=expected)

    def test_regression_parallel_mode_without_filepath(self) -> None:
        # Test that parallel mode properly passes filepath
        # https://github.com/PyCQA/pylint/issues/3564
        path = join(
            HERE, "regrtest_data", "regression_missing_init_3564", "subdirectory/"
        )
        self._test_output([path, "-j2"], expected_output="")

    def test_output_file_valid_path(self, tmp_path: Path) -> None:
        path = join(HERE, "regrtest_data", "unused_variable.py")
        output_file = tmp_path / "output.txt"
        expected = "Your code has been rated at 7.50/10"
        self._test_output_file(
            [path, f"--output={output_file}"],
            output_file,
            expected_output=expected,
        )

    def test_output_file_invalid_path_exits_with_code_32(self) -> None:
        path = join(HERE, "regrtest_data", "unused_variable.py")
        output_file = "thisdirectorydoesnotexit/output.txt"
        self._runtest([path, f"--output={output_file}"], code=32)

    @pytest.mark.parametrize(
        "args, expected",
        [
            ([], 0),
            (["--enable=C"], 0),
            (["--fail-on=superfluous-parens"], 0),
            (["--fail-on=import-error"], 6),
            (["--fail-on=unused-import"], 6),
            (["--fail-on=unused-import", "--enable=C"], 22),
            (["--fail-on=missing-function-docstring"], 22),
            (["--fail-on=useless-suppression"], 6),
            (["--fail-on=useless-suppression", "--enable=C"], 22),
        ],
    )
    def test_fail_on_exit_code(self, args: list[str], expected: int) -> None:
        path = join(HERE, "regrtest_data", "fail_on.py")
        # We set fail-under to be something very low so that even with the warnings
        # and errors that are generated they don't affect the exit code.
        self._runtest([path, "--fail-under=-10", "--disable=C", *args], code=expected)

    def test_one_module_fatal_error(self) -> None:
        """Fatal errors in one of several modules linted still exits non-zero."""
        valid_path = join(HERE, "conftest.py")
        invalid_path = join(HERE, "garbagePath.py")
        self._runtest([valid_path, invalid_path, "--disable=C"], code=1)

    @pytest.mark.parametrize(
        "args, expected",
        [
            ([], 0),
            (["--enable=C"], 0),
            (["--fail-on=superfluous-parens"], 0),
            (["--fail-on=import-error"], 0),
            (["--fail-on=unused-import"], 0),
            (["--fail-on=unused-import", "--enable=C"], 0),
            (["--fail-on=missing-function-docstring"], 0),
            (["--fail-on=useless-suppression"], 1),
            (["--fail-on=useless-suppression", "--enable=C"], 1),
        ],
    )
    def test_fail_on_info_only_exit_code(self, args: list[str], expected: int) -> None:
        path = join(HERE, "regrtest_data", "fail_on_info_only.py")
        self._runtest([path, *args], code=expected)

    @pytest.mark.parametrize(
        "output_format, expected_output",
        [
            (
                "text",
                "{path}:4:4: W0612: Unused variable 'variable' (unused-variable)",
            ),
            (
                "parseable",
                "{path}:4: [W0612(unused-variable), test] Unused variable 'variable'",
            ),
            (
                "msvs",
                "{path}(4): [W0612(unused-variable)test] Unused variable 'variable'",
            ),
            (
                "colorized",
                (
                    "{path}:4:4: W0612: \x1B[35mUnused variable 'variable'\x1B[0m (\x1B[35munused-variable\x1B[0m)"
                ),
            ),
            ("json", '"message": "Unused variable \'variable\'",'),
        ],
    )
    def test_output_file_can_be_combined_with_output_format_option(
        self, tmp_path: Path, output_format: str, expected_output: str
    ) -> None:
        path = join(HERE, "regrtest_data", "unused_variable.py")
        output_file = tmp_path / "output.txt"
        self._test_output_file(
            [path, f"--output={output_file}", f"--output-format={output_format}"],
            output_file,
            expected_output.format(path="tests/regrtest_data/unused_variable.py"),
        )

    def test_output_file_can_be_combined_with_custom_reporter(
        self, tmp_path: Path
    ) -> None:
        path = join(HERE, "regrtest_data", "unused_variable.py")
        output_file = tmp_path / "output.txt"
        # It does not really have to be a truly custom reporter.
        # It is only important that it is being passed explicitly to ``Run``.
        myreporter = TextReporter()
        self._run_pylint(
            [path, f"--output={output_file}"],
            out=sys.stdout,
            reporter=myreporter,
        )
        assert output_file.exists()

    def test_output_file_specified_in_rcfile(self, tmp_path: Path) -> None:
        output_file = tmp_path / "output.txt"
        rcfile = tmp_path / "pylintrc"
        rcfile_contents = textwrap.dedent(
            f"""
        [MAIN]
        output={output_file}
        """
        )
        rcfile.write_text(rcfile_contents, encoding="utf-8")
        path = join(HERE, "regrtest_data", "unused_variable.py")
        expected = "Your code has been rated at 7.50/10"
        self._test_output_file(
            [path, f"--output={output_file}", f"--rcfile={rcfile}"],
            output_file,
            expected_output=expected,
        )

    @staticmethod
    def test_load_text_repoter_if_not_provided() -> None:
        """Test if PyLinter.reporter is a TextReporter if no reporter is provided."""
        linter = PyLinter()

        assert isinstance(linter.reporter, TextReporter)

    @staticmethod
    def test_regex_paths_csv_validator() -> None:
        """Test to see if _regexp_paths_csv_validator works.
        Previously the validator crashed when encountering already validated values.
        Reported in https://github.com/PyCQA/pylint/issues/5437
        """
        with pytest.raises(SystemExit) as ex:
            args = _add_rcfile_default_pylintrc(
                ["--ignore-paths", "test", join(HERE, "regrtest_data", "empty.py")]
            )
            Run(args)
        assert ex.value.code == 0

    @staticmethod
    def test_max_inferred_for_complicated_class_hierarchy() -> None:
        """Regression test for a crash reported in https://github.com/PyCQA/pylint/issues/5679.

        The class hierarchy of 'sqlalchemy' is so intricate that it becomes uninferable with
        the standard max_inferred of 100. We used to crash when this happened.
        """
        with pytest.raises(SystemExit) as ex:
            path = join(
                HERE, "regrtest_data", "max_inferable_limit_for_classes", "main.py"
            )
            Run([path])
        # Error code should not include bit-value 1 for crash
        assert not ex.value.code % 2

    def test_recursive(self) -> None:
        """Tests if running linter over directory using --recursive=y"""
        self._runtest(
            [join(HERE, "regrtest_data", "directory", "subdirectory"), "--recursive=y"],
            code=0,
        )

    def test_recursive_globbing(self) -> None:
        """Tests if running linter over directory using --recursive=y and globbing"""
        self._runtest(
            [join(HERE, "regrtest_data", "d?rectory", "subd*"), "--recursive=y"],
            code=0,
        )

    @pytest.mark.parametrize("ignore_value", ["ignored_subdirectory", "failing.py"])
    def test_ignore_recursive(self, ignore_value: str) -> None:
        """Tests recursive run of linter ignoring directory using --ignore parameter.

        Ignored directory contains files yielding lint errors. If directory is not ignored
        test would fail due these errors.
        """
        directory = join(HERE, "regrtest_data", "directory")
        self._runtest([directory, "--recursive=y", f"--ignore={ignore_value}"], code=0)

    @pytest.mark.parametrize("ignore_pattern_value", ["ignored_.*", "failing.*"])
    def test_ignore_pattern_recursive(self, ignore_pattern_value: str) -> None:
        """Tests recursive run of linter ignoring directory using --ignore-parameter parameter.

        Ignored directory contains files yielding lint errors. If directory is not ignored
        test would fail due these errors.
        """
        directory = join(HERE, "regrtest_data", "directory")
        self._runtest(
            [directory, "--recursive=y", f"--ignore-patterns={ignore_pattern_value}"],
            code=0,
        )

    def test_ignore_pattern_from_stdin(self) -> None:
        """Test if linter ignores standard input if the filename matches the ignore pattern."""
        with mock.patch("pylint.lint.pylinter._read_stdin", return_value="import os\n"):
            self._runtest(
                [
                    "--from-stdin",
                    "mymodule.py",
                    "--disable=all",
                    "--enable=unused-import",
                    "--ignore-patterns=mymodule.py",
                ],
                code=0,
            )

    @pytest.mark.parametrize("ignore_path_value", [".*ignored.*", ".*failing.*"])
    def test_ignore_path_recursive(self, ignore_path_value: str) -> None:
        """Tests recursive run of linter ignoring directory using --ignore-path parameter.

        Ignored directory contains files yielding lint errors. If directory is not ignored
        test would fail due these errors.
        """
        directory = join(HERE, "regrtest_data", "directory")
        self._runtest(
            [directory, "--recursive=y", f"--ignore-paths={ignore_path_value}"], code=0
        )

    def test_recursive_current_dir(self) -> None:
        with _test_sys_path():
            # pytest is including directory HERE/regrtest_data to sys.path which causes
            # astroid to believe that directory is a package.
            sys.path = [
                path
                for path in sys.path
                if not os.path.basename(path) == "regrtest_data"
            ]
            with _test_cwd():
                os.chdir(join(HERE, "regrtest_data", "directory", "subdirectory"))
                self._runtest(
                    [".", "--recursive=y"],
                    code=0,
                )

    def test_ignore_path_recursive_current_dir(self) -> None:
        """Tests that path is normalized before checked that is ignored. GitHub issue #6964"""
        with _test_sys_path():
            # pytest is including directory HERE/regrtest_data to sys.path which causes
            # astroid to believe that directory is a package.
            sys.path = [
                path
                for path in sys.path
                if not os.path.basename(path) == "regrtest_data"
            ]
            with _test_cwd():
                os.chdir(join(HERE, "regrtest_data", "directory"))
                self._runtest(
                    [
                        ".",
                        "--recursive=y",
                        "--ignore-paths=^ignored_subdirectory/.*",
                    ],
                    code=0,
                )

    def test_syntax_error_invalid_encoding(self) -> None:
        module = join(HERE, "regrtest_data", "invalid_encoding.py")
        expected_output = "unknown encoding"
        self._test_output([module, "-E"], expected_output=expected_output)

    @pytest.mark.parametrize(
        "module_name,expected_output",
        [
            ("good.py", ""),
            ("bad_wrong_num.py", "(syntax-error)"),
            ("bad_missing_num.py", "(bad-file-encoding)"),
        ],
    )
    def test_encoding(self, module_name: str, expected_output: str) -> None:
        path = join(HERE, "regrtest_data", "encoding", module_name)
        self._test_output(
            [path], expected_output=expected_output, unexpected_output="(astroid-error)"
        )

    def test_line_too_long_useless_suppression(self) -> None:
        """A test that demonstrates a known false positive for useless-suppression

        See https://github.com/PyCQA/pylint/issues/3368

        If you manage to make this test fail and remove the useless-suppression
        warning please contact open a Pylint PR!
        """
        module = join(HERE, "regrtest_data", "line_too_long_no_code.py")
        expected = textwrap.dedent(
            f"""
        {module}:1:0: I0011: Locally disabling line-too-long (C0301) (locally-disabled)
        {module}:1:0: I0021: Useless suppression of 'line-too-long' (useless-suppression)
        """
        )

        self._test_output([module, "--enable=all"], expected_output=expected)

    def test_output_no_header(self) -> None:
        module = join(HERE, "data", "clientmodule_test.py")
        expected = "Unused variable 'local_variable'"
        not_expected = textwrap.dedent(
            """************* Module data.clientmodule_test"""
        )

        args = [module, "--output-format=no-header"]
        self._test_output(
            args, expected_output=expected, unexpected_output=not_expected
        )

    def test_no_name_in_module(self) -> None:
        """Test that a package with both a variable name `base` and a module `base`
        does not emit a no-name-in-module msg."""
        module = join(HERE, "regrtest_data", "test_no_name_in_module.py")
        unexpected = "No name 'errors' in module 'list' (no-name-in-module)"
        self._test_output(
            [module, "-E"], expected_output="", unexpected_output=unexpected
        )


class TestCallbackOptions:
    """Test for all callback options we support."""

    @staticmethod
    @pytest.mark.parametrize(
        "command,expected",
        [
            (["--list-msgs"], "Emittable messages with current interpreter:"),
            (["--list-msgs-enabled"], "Enabled messages:"),
            (["--list-groups"], "nonascii-checker"),
            (["--list-conf-levels"], "Confidence(name='HIGH', description="),
            (["--list-extensions"], "pylint.extensions.empty_comment"),
            (["--full-documentation"], "Pylint global options and switches"),
            (["--long-help"], "Environment variables:"),
        ],
    )
    def test_output_of_callback_options(
        command: list[str], expected: str, tmp_path: Path
    ) -> None:
        """Test whether certain strings are in the output of a callback command."""
        command = _add_rcfile_default_pylintrc(command)
        process = subprocess.run(
            [sys.executable, "-m", "pylint", *command],
            capture_output=True,
            encoding="utf-8",
            check=False,
            cwd=str(tmp_path),
        )
        assert expected in process.stdout

    @staticmethod
    @pytest.mark.parametrize(
        "args,expected,error",
        [
            [["--help-msg", "W0101"], ":unreachable (W0101)", False],
            [["--help-msg", "WX101"], "No such message id", False],
            [["--help-msg"], "--help-msg: expected at least one argumen", True],
            [["--help-msg", "C0102,C0103"], ":invalid-name (C0103):", False],
        ],
    )
    def test_help_msg(
        args: list[str], expected: str, error: bool, tmp_path: Path
    ) -> None:
        """Test the --help-msg flag."""
        args = _add_rcfile_default_pylintrc(args)
        process = subprocess.run(
            [sys.executable, "-m", "pylint", *args],
            capture_output=True,
            encoding="utf-8",
            check=False,
            cwd=str(tmp_path),
        )
        if error:
            result = process.stderr
        else:
            result = process.stdout
        assert expected in result

    @staticmethod
    def test_generate_rcfile(tmp_path: Path) -> None:
        """Test the --generate-rcfile flag."""
        args = _add_rcfile_default_pylintrc(["--generate-rcfile"])
        process = subprocess.run(
            [sys.executable, "-m", "pylint", *args],
            capture_output=True,
            encoding="utf-8",
            check=False,
            cwd=str(tmp_path),
        )
        assert "[MAIN]" in process.stdout
        assert "[MASTER]" not in process.stdout
        assert "profile" not in process.stdout
        args = _add_rcfile_default_pylintrc(["--generate-rcfile"])
        process_two = subprocess.run(
            [sys.executable, "-m", "pylint", *args],
            capture_output=True,
            encoding="utf-8",
            check=False,
            cwd=str(tmp_path),
        )
        assert process.stdout == process_two.stdout

        # Check that the generated file is valid
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
            filename = temp.name
            temp.write(process.stdout)
            runner = Run(
                [join(HERE, "regrtest_data", "empty.py"), f"--rcfile={filename}"],
                exit=False,
            )
            assert not runner.linter.msg_status
        os.remove(filename)

    @staticmethod
    def test_generate_config_disable_symbolic_names() -> None:
        """Test that --generate-rcfile puts symbolic names in the --disable option."""
        out = StringIO()
        with _patch_streams(out):
            with pytest.raises(SystemExit):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    Run(["--generate-rcfile", "--rcfile=", "--persistent=no"])
        output = out.getvalue()

        # Get rid of the pesky messages that pylint emits if the
        # configuration file is not found.
        pattern = rf"\[{MAIN_CHECKER_NAME.upper()}"
        main = re.search(pattern, output)
        assert main is not None, f"{pattern} not found in {output}"

        out = StringIO(output[main.start() :])
        parser = configparser.RawConfigParser()
        parser.read_file(out)
        messages = utils._splitstrip(parser.get("MESSAGES CONTROL", "disable"))
        assert "suppressed-message" in messages

    @staticmethod
    def test_generate_toml_config(tmp_path: Path) -> None:
        """Test the --generate-toml-config flag."""
        args = _add_rcfile_default_pylintrc(
            [
                "--preferred-modules=a:b",
                "--generate-toml-config",
            ]
        )
        process = subprocess.run(
            [sys.executable, "-m", "pylint", *args],
            capture_output=True,
            encoding="utf-8",
            check=False,
            cwd=str(tmp_path),
        )
        assert "[tool.pylint.main]" in process.stdout
        assert "[tool.pylint.master]" not in process.stdout
        assert '"positional arguments"' not in process.stdout
        assert '"optional arguments"' not in process.stdout
        assert 'preferred-modules = ["a:b"]' in process.stdout

        process_two = subprocess.run(
            [sys.executable, "-m", "pylint", *args],
            capture_output=True,
            encoding="utf-8",
            check=False,
            cwd=str(tmp_path),
        )
        assert process.stdout == process_two.stdout

        # Check that the generated file is valid
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".toml", delete=False
        ) as temp:
            filename = temp.name
            temp.write(process.stdout)
            runner = Run(
                [join(HERE, "regrtest_data", "empty.py"), f"--rcfile={filename}"],
                exit=False,
            )
            assert not runner.linter.msg_status
        os.remove(filename)

    @staticmethod
    def test_generate_toml_config_disable_symbolic_names() -> None:
        """Test that --generate-toml-config puts symbolic names in the --disable option."""
        output_stream = StringIO()
        with _patch_streams(output_stream):
            with pytest.raises(SystemExit):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    Run(["--generate-toml-config"])

        out = output_stream.getvalue()
        bytes_out = BytesIO(out.encode("utf-8"))
        content = tomllib.load(bytes_out)
        messages = content["tool"]["pylint"]["messages control"]["disable"]
        assert "useless-suppression" in messages, out

    @staticmethod
    def test_errors_only() -> None:
        """Test the --errors-only flag."""
        with pytest.raises(SystemExit):
            run = Run(["--errors-only"])
            assert run.linter._error_mode

    @staticmethod
    def test_errors_only_functions_as_disable() -> None:
        """--errors-only functions as a shortcut for --disable=W,C,R,I;
        it no longer enables any messages."""
        run = Run(
            [str(UNNECESSARY_LAMBDA), "--disable=import-error", "--errors-only"],
            exit=False,
        )
        assert not run.linter.is_message_enabled("import-error")

    @staticmethod
    def test_verbose() -> None:
        """Test the --verbose flag."""
        with pytest.raises(SystemExit):
            run = Run(["--verbose"])
            assert run.verbose

        with pytest.raises(SystemExit):
            run = Run(["--verbose=True"])
            assert run.verbose

    @staticmethod
    def test_enable_all_extensions() -> None:
        """Test to see if --enable-all-extensions does indeed load all extensions."""
        # Record all extensions
        plugins = []
        for filename in os.listdir(os.path.dirname(extensions.__file__)):
            if filename.endswith(".py") and not filename.startswith("_"):
                plugins.append(f"pylint.extensions.{filename[:-3]}")

        # Check if they are loaded
        runner = Run(
            ["--enable-all-extensions", join(HERE, "regrtest_data", "empty.py")],
            exit=False,
        )
        assert sorted(plugins) == sorted(runner.linter._dynamic_plugins)
