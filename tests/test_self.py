# Copyright (c) 2006-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Vlad Temian <vladtemian@gmail.com>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2016 Moises Lopez <moylop260@vauxoo.com>
# Copyright (c) 2017, 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2017, 2021 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2017, 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2017, 2019 Thomas Hisch <t.hisch@gmail.com>
# Copyright (c) 2017 Daniel Miller <millerdev@gmail.com>
# Copyright (c) 2017 Bryce Guinta <bryce.paul.guinta@gmail.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2018 Jason Owen <jason.a.owen@gmail.com>
# Copyright (c) 2018 Jace Browning <jacebrowning@gmail.com>
# Copyright (c) 2018 Reverb C <reverbc@users.noreply.github.com>
# Copyright (c) 2019 Hugues <hugues.bruant@affirm.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 Frank Harrison <frank@doublethefish.com>
# Copyright (c) 2020 Matěj Grabovský <mgrabovs@redhat.com>
# Copyright (c) 2020 Pieter Engelbrecht <pengelbrecht@rems2.com>
# Copyright (c) 2020 Clément Pit-Claudel <cpitclaudel@users.noreply.github.com>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Mark Bell <mark00bell@googlemail.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Dr. Nick <das-intensity@users.noreply.github.com>
# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>
# Copyright (c) 2021 chohner <mail@chohner.com>
# Copyright (c) 2021 Louis Sautier <sautier.louis@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

# pylint: disable=too-many-public-methods

import configparser
import contextlib
import json
import os
import platform
import re
import subprocess
import sys
import textwrap
import warnings
from copy import copy
from io import StringIO
from os.path import abspath, dirname, join
from pathlib import Path
from typing import TYPE_CHECKING, Any, Generator, Iterator, List, Optional, TextIO
from unittest import mock
from unittest.mock import patch

import pytest
from py._path.local import LocalPath  # type: ignore[import]

from pylint import extensions, modify_sys_path
from pylint.constants import MAIN_CHECKER_NAME, MSG_TYPES_STATUS
from pylint.lint import Run
from pylint.lint.pylinter import PyLinter
from pylint.message import Message
from pylint.reporters import JSONReporter
from pylint.reporters.text import BaseReporter, ColorizedTextReporter, TextReporter
from pylint.utils import utils

if TYPE_CHECKING:
    from pylint.reporters.ureports.nodes import Section

HERE = abspath(dirname(__file__))
CLEAN_PATH = re.escape(dirname(dirname(__file__)) + os.path.sep)
UNNECESSARY_LAMBDA = join(
    HERE, "functional", "u", "unnecessary", "unnecessary_lambda.py"
)


@contextlib.contextmanager
def _patch_streams(out: TextIO) -> Iterator:
    sys.stderr = sys.stdout = out
    try:
        yield
    finally:
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__


@contextlib.contextmanager
def _configure_lc_ctype(lc_ctype: str) -> Iterator:
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
    def __init__(self, reporters: List[BaseReporter]) -> None:
        # pylint: disable=super-init-not-called
        # We don't call it because there is an attribute "linter" that is set inside the base class
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

    def _display(self, layout: "Section") -> None:
        pass

    @property
    def out(self) -> TextIO:  # type: ignore[override]
        return self._reporters[0].out

    @property  # type: ignore[override]
    def linter(self) -> PyLinter:  # type: ignore[override]
        return self._linter

    @linter.setter
    def linter(self, value: PyLinter) -> None:
        self._linter = value
        for rep in self._reporters:
            rep.linter = value


class TestRunTC:
    def _runtest(
        self,
        args: List[str],
        reporter: Any = None,
        out: Optional[StringIO] = None,
        code: Optional[int] = None,
    ) -> None:
        if out is None:
            out = StringIO()
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
    def _run_pylint(args: List[str], out: TextIO, reporter: Any = None) -> int:
        args = args + ["--persistent=no"]
        with _patch_streams(out):
            with pytest.raises(SystemExit) as cm:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    Run(args, reporter=reporter)
            return cm.value.code

    @staticmethod
    def _clean_paths(output: str) -> str:
        """Normalize path to the tests directory."""
        output = re.sub(CLEAN_PATH, "", output, flags=re.MULTILINE)
        return output.replace("\\", "/")

    def _test_output(self, args: List[str], expected_output: str) -> None:
        out = StringIO()
        self._run_pylint(args, out=out)
        actual_output = self._clean_paths(out.getvalue())
        expected_output = self._clean_paths(expected_output)
        assert expected_output.strip() in actual_output.strip()

    def _test_output_file(
        self, args: List[str], filename: LocalPath, expected_output: str
    ) -> None:
        """
        Run Pylint with the ``output`` option set (must be included in
        the ``args`` passed to this method!) and check the file content afterwards.
        """
        out = StringIO()
        self._run_pylint(args, out=out)
        cmdline_output = out.getvalue()
        file_output = self._clean_paths(Path(filename).read_text(encoding="utf-8"))
        expected_output = self._clean_paths(expected_output)
        assert (
            cmdline_output == ""
        ), "Unexpected output to stdout/stderr while output option was set"
        assert expected_output.strip() in file_output.strip()

    def test_pkginfo(self) -> None:
        """Make pylint check itself."""
        self._runtest(["pylint.__pkginfo__"], reporter=TextReporter(StringIO()), code=0)

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

    def test_generate_config_option(self) -> None:
        self._runtest(["--generate-rcfile"], code=0)

    def test_generate_config_option_order(self) -> None:
        out1 = StringIO()
        out2 = StringIO()
        self._runtest(["--generate-rcfile"], code=0, out=out1)
        self._runtest(["--generate-rcfile"], code=0, out=out2)
        output1 = out1.getvalue()
        output2 = out2.getvalue()
        assert output1 == output2

    def test_generate_config_disable_symbolic_names(self) -> None:
        # Test that --generate-rcfile puts symbolic names in the --disable
        # option.

        out = StringIO()
        self._run_pylint(["--generate-rcfile", "--rcfile="], out=out)

        output = out.getvalue()
        # Get rid of the pesky messages that pylint emits if the
        # configuration file is not found.
        pattern = fr"\[{MAIN_CHECKER_NAME.upper()}"
        master = re.search(pattern, output)
        assert master is not None, f"{pattern} not found in {output}"
        out = StringIO(output[master.start() :])
        parser = configparser.RawConfigParser()
        parser.read_file(out)
        messages = utils._splitstrip(parser.get("MESSAGES CONTROL", "disable"))
        assert "suppressed-message" in messages

    def test_generate_rcfile_no_obsolete_methods(self) -> None:
        out = StringIO()
        self._run_pylint(["--generate-rcfile"], out=out)
        output = out.getvalue()
        assert "profile" not in output

    def test_nonexistent_config_file(self) -> None:
        self._runtest(["--rcfile=/tmp/this_file_does_not_exist"], code=32)

    def test_help_message_option(self) -> None:
        self._runtest(["--help-msg", "W0101"], code=0)

    def test_error_help_message_option(self) -> None:
        self._runtest(["--help-msg", "WX101"], code=0)

    def test_error_missing_arguments(self) -> None:
        self._runtest([], code=32)

    def test_no_out_encoding(self) -> None:
        """test redirection of stdout with non ascii characters"""
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

    def test_abbreviations_are_not_supported(self) -> None:
        expected = "no such option: --load-plugin"
        self._test_output([".", "--load-plugin"], expected_output=expected)

    def test_enable_all_works(self) -> None:
        module = join(HERE, "data", "clientmodule_test.py")
        expected = textwrap.dedent(
            f"""
        ************* Module data.clientmodule_test
        {module}:10:8: W0612: Unused variable 'local_variable' (unused-variable)
        {module}:18:4: C0116: Missing function or method docstring (missing-function-docstring)
        {module}:22:0: C0115: Missing class docstring (missing-class-docstring)
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

    def test_import_itself_not_accounted_for_relative_imports(self) -> None:
        expected = "Your code has been rated at 10.00/10"
        package = join(HERE, "regrtest_data", "dummy")
        self._test_output(
            [package, "--disable=locally-disabled", "-rn"], expected_output=expected
        )

    def test_reject_empty_indent_strings(self) -> None:
        expected = "indent string can't be empty"
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
        config_path = join(HERE, "regrtest_data", ".pylintrc")
        expected = "Your code has been rated at 10.00/10"
        self._test_output(
            [path, f"--rcfile={config_path}", "-rn"], expected_output=expected
        )

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
                "--help-msg=dummy-message-01,dummy-message-02",
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
    def test_parseable_file_path(self):
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
    def test_stdin(self, input_path, module, expected_path):
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
    def test_relative_imports(self, write_bpy_to_disk, tmpdir):
        a = tmpdir.join("a")

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
        a.join("__init__.py").write("")
        if write_bpy_to_disk:
            a.join("b.py").write(b_code)
        a.join("c.py").write(c_code)

        with tmpdir.as_cwd():
            # why don't we start pylint in a subprocess?
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

            # this code needs to work w/ and w/o a file named a/b.py on the
            # harddisk.
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

    def test_stdin_syntaxerror(self) -> None:
        expected_output = (
            "************* Module a\n"
            "a.py:1:4: E0001: invalid syntax (<unknown>, line 1) (syntax-error)"
        )

        with mock.patch(
            "pylint.lint.pylinter._read_stdin", return_value="for\n"
        ) as mock_stdin:
            self._test_output(
                ["--from-stdin", "a.py", "--disable=all", "--enable=syntax-error"],
                expected_output=expected_output,
            )
            assert mock_stdin.call_count == 1

    def test_version(self) -> None:
        def check(lines: List[str]) -> None:
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
        self._runtest(
            [
                "--fail-under",
                "-9",
                "--enable=all",
                join(HERE, "regrtest_data", "fail_under_minus10.py"),
            ],
            code=22,
        )
        self._runtest(
            [
                "--fail-under",
                "-5",
                "--enable=all",
                join(HERE, "regrtest_data", "fail_under_minus10.py"),
            ],
            code=22,
        )

    @pytest.mark.parametrize(
        "fu_score,fo_msgs,fname,out",
        [
            # Essentially same test cases as --fail-under, but run with/without a detected issue code
            # missing-function-docstring (C0116) is issue in both files
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
            (-10, "broad-except", "fail_under_plus7_5.py", 0),
            (6, "broad-except", "fail_under_plus7_5.py", 0),
            (7.5, "broad-except", "fail_under_plus7_5.py", 0),
            (7.6, "broad-except", "fail_under_plus7_5.py", 16),
            (-11, "broad-except", "fail_under_minus10.py", 0),
            (-10, "broad-except", "fail_under_minus10.py", 0),
            (-9, "broad-except", "fail_under_minus10.py", 22),
            (-5, "broad-except", "fail_under_minus10.py", 22),
            # Enable by message id
            (-10, "C0116", "fail_under_plus7_5.py", 16),
            # Enable by category
            (-10, "C", "fail_under_plus7_5.py", 16),
            (-10, "fake1,C,fake2", "fail_under_plus7_5.py", 16),
            # Ensure entire category not enabled by any msg id
            (-10, "C0115", "fail_under_plus7_5.py", 0),
        ],
    )
    def test_fail_on(self, fu_score, fo_msgs, fname, out):
        self._runtest(
            [
                "--fail-under",
                f"{fu_score:f}",
                f"--fail-on={fo_msgs}",
                "--enable=all",
                join(HERE, "regrtest_data", fname),
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
    def test_fail_on_edge_case(self, opts, out):
        self._runtest(
            opts + [join(HERE, "regrtest_data", "fail_under_plus7_5.py")],
            code=out,
        )

    @staticmethod
    def test_modify_sys_path() -> None:
        @contextlib.contextmanager
        def test_sys_path() -> Generator[None, None, None]:
            original_path = sys.path
            try:
                yield
            finally:
                sys.path = original_path

        @contextlib.contextmanager
        def test_environ_pythonpath(
            new_pythonpath: Optional[str],
        ) -> Generator[None, None, None]:
            original_pythonpath = os.environ.get("PYTHONPATH")
            if new_pythonpath:
                os.environ["PYTHONPATH"] = new_pythonpath
            elif new_pythonpath is None and original_pythonpath is not None:
                # If new_pythonpath is None, make sure to delete PYTHONPATH if present
                del os.environ["PYTHONPATH"]
            try:
                yield
            finally:
                if original_pythonpath:
                    os.environ["PYTHONPATH"] = original_pythonpath
                elif new_pythonpath is not None:
                    # Only delete PYTHONPATH if new_pythonpath wasn't None
                    del os.environ["PYTHONPATH"]

        with test_sys_path(), patch("os.getcwd") as mock_getcwd:
            cwd = "/tmp/pytest-of-root/pytest-0/test_do_not_import_files_from_0"
            mock_getcwd.return_value = cwd
            default_paths = [
                "/usr/local/lib/python39.zip",
                "/usr/local/lib/python3.9",
                "/usr/local/lib/python3.9/lib-dynload",
                "/usr/local/lib/python3.9/site-packages",
            ]

            paths = [
                cwd,
                *default_paths,
            ]
            sys.path = copy(paths)
            with test_environ_pythonpath(None):
                modify_sys_path()
            assert sys.path == paths[1:]

            paths = [
                cwd,
                cwd,
                *default_paths,
            ]
            sys.path = copy(paths)
            with test_environ_pythonpath("."):
                modify_sys_path()
            assert sys.path == paths[1:]

            paths = [
                cwd,
                "/custom_pythonpath",
                *default_paths,
            ]
            sys.path = copy(paths)
            with test_environ_pythonpath("/custom_pythonpath"):
                modify_sys_path()
            assert sys.path == paths[1:]

            paths = [
                cwd,
                "/custom_pythonpath",
                cwd,
                *default_paths,
            ]
            sys.path = copy(paths)
            with test_environ_pythonpath("/custom_pythonpath:"):
                modify_sys_path()
            assert sys.path == [paths[1]] + paths[3:]

            paths = [
                "",
                cwd,
                "/custom_pythonpath",
                *default_paths,
            ]
            sys.path = copy(paths)
            with test_environ_pythonpath(":/custom_pythonpath"):
                modify_sys_path()
            assert sys.path == paths[2:]

            paths = [
                cwd,
                cwd,
                "/custom_pythonpath",
                *default_paths,
            ]
            sys.path = copy(paths)
            with test_environ_pythonpath(":/custom_pythonpath:"):
                modify_sys_path()
            assert sys.path == paths[2:]

            paths = [
                cwd,
                cwd,
                *default_paths,
            ]
            sys.path = copy(paths)
            with test_environ_pythonpath(":."):
                modify_sys_path()
            assert sys.path == paths[1:]
            sys.path = copy(paths)
            with test_environ_pythonpath(f":{cwd}"):
                modify_sys_path()
            assert sys.path == paths[1:]

            sys.path = copy(paths)
            with test_environ_pythonpath(".:"):
                modify_sys_path()
            assert sys.path == paths[1:]
            sys.path = copy(paths)
            with test_environ_pythonpath(f"{cwd}:"):
                modify_sys_path()
            assert sys.path == paths[1:]

            paths = [
                "",
                cwd,
                *default_paths,
                cwd,
            ]
            sys.path = copy(paths)
            with test_environ_pythonpath(cwd):
                modify_sys_path()
            assert sys.path == paths[1:]

    @staticmethod
    def test_do_not_import_files_from_local_directory(tmpdir: LocalPath) -> None:
        p_astroid = tmpdir / "astroid.py"
        p_astroid.write("'Docstring'\nimport completely_unknown\n")
        p_hmac = tmpdir / "hmac.py"
        p_hmac.write("'Docstring'\nimport completely_unknown\n")

        with tmpdir.as_cwd():
            subprocess.check_output(
                [
                    sys.executable,
                    "-m",
                    "pylint",
                    "astroid.py",
                    "--disable=import-error,unused-import",
                ],
                cwd=str(tmpdir),
            )

        # Linting this astroid file does not import it
        with tmpdir.as_cwd():
            subprocess.check_output(
                [
                    sys.executable,
                    "-m",
                    "pylint",
                    "-j2",
                    "astroid.py",
                    "--disable=import-error,unused-import",
                ],
                cwd=str(tmpdir),
            )

        # Test with multiple jobs for hmac.py for which we have a
        # CVE against: https://github.com/PyCQA/pylint/issues/959
        with tmpdir.as_cwd():
            subprocess.call(
                [
                    sys.executable,
                    "-m",
                    "pylint",
                    "-j2",
                    "hmac.py",
                    "--disable=import-error,unused-import",
                ],
                cwd=str(tmpdir),
            )

    @staticmethod
    def test_do_not_import_files_from_local_directory_with_pythonpath(
        tmpdir: LocalPath,
    ) -> None:
        p_astroid = tmpdir / "astroid.py"
        p_astroid.write("'Docstring'\nimport completely_unknown\n")
        p_hmac = tmpdir / "hmac.py"
        p_hmac.write("'Docstring'\nimport completely_unknown\n")

        # Appending a colon to PYTHONPATH should not break path stripping
        # https://github.com/PyCQA/pylint/issues/3636
        with tmpdir.as_cwd():
            orig_pythonpath = os.environ.get("PYTHONPATH")
            os.environ["PYTHONPATH"] = f"{(orig_pythonpath or '').strip(':')}:"
            subprocess.check_output(
                [
                    sys.executable,
                    "-m",
                    "pylint",
                    "astroid.py",
                    "--disable=import-error,unused-import",
                ],
                cwd=str(tmpdir),
            )
            if orig_pythonpath:
                os.environ["PYTHONPATH"] = orig_pythonpath
            else:
                del os.environ["PYTHONPATH"]

    @staticmethod
    def test_import_plugin_from_local_directory_if_pythonpath_cwd(
        tmpdir: LocalPath,
    ) -> None:
        p_plugin = tmpdir / "plugin.py"
        p_plugin.write("# Some plugin content")

        with tmpdir.as_cwd():
            orig_pythonpath = os.environ.get("PYTHONPATH")
            if sys.platform == "win32":
                os.environ["PYTHONPATH"] = "."
            else:
                os.environ["PYTHONPATH"] = f"{(orig_pythonpath or '').strip(':')}:."
            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pylint",
                    "--load-plugins",
                    "plugin",
                ],
                cwd=str(tmpdir),
                stderr=subprocess.PIPE,
                check=False,
            )
            assert (
                "AttributeError: module 'plugin' has no attribute 'register'"
                in process.stderr.decode()
            )
            if orig_pythonpath:
                os.environ["PYTHONPATH"] = orig_pythonpath
            else:
                del os.environ["PYTHONPATH"]

    def test_allow_import_of_files_found_in_modules_during_parallel_check(
        self, tmpdir: LocalPath
    ) -> None:
        test_directory = tmpdir / "test_directory"
        test_directory.mkdir()
        spam_module = test_directory / "spam.py"
        spam_module.write("'Empty'")

        init_module = test_directory / "__init__.py"
        init_module.write("'Empty'")

        # For multiple jobs we could not find the `spam.py` file.
        with tmpdir.as_cwd():
            self._runtest(
                [
                    "-j2",
                    "--disable=missing-docstring, missing-final-newline",
                    "test_directory",
                ],
                code=0,
            )

        # A single job should be fine as well
        with tmpdir.as_cwd():
            self._runtest(
                [
                    "-j1",
                    "--disable=missing-docstring, missing-final-newline",
                    "test_directory",
                ],
                code=0,
            )

    @staticmethod
    def test_can_list_directories_without_dunder_init(tmpdir: LocalPath) -> None:
        test_directory = tmpdir / "test_directory"
        test_directory.mkdir()
        spam_module = test_directory / "spam.py"
        spam_module.write("'Empty'")

        subprocess.check_output(
            [
                sys.executable,
                "-m",
                "pylint",
                "--disable=missing-docstring, missing-final-newline",
                "test_directory",
            ],
            cwd=str(tmpdir),
            stderr=subprocess.PIPE,
        )

    def test_jobs_score(self) -> None:
        path = join(HERE, "regrtest_data", "unused_variable.py")
        expected = "Your code has been rated at 7.50/10"
        self._test_output([path, "--jobs=2", "-ry"], expected_output=expected)

    def test_duplicate_code_raw_strings(self) -> None:
        path = join(HERE, "regrtest_data", "duplicate_data_raw_strings")
        expected_output = "Similar lines in 2 files"
        self._test_output(
            [path, "--disable=all", "--enable=duplicate-code"],
            expected_output=expected_output,
        )

    def test_regression_parallel_mode_without_filepath(self) -> None:
        # Test that parallel mode properly passes filepath
        # https://github.com/PyCQA/pylint/issues/3564
        path = join(
            HERE, "regrtest_data", "regression_missing_init_3564", "subdirectory/"
        )
        self._test_output([path, "-j2"], expected_output="No such file or directory")

    def test_output_file_valid_path(self, tmpdir: LocalPath) -> None:
        path = join(HERE, "regrtest_data", "unused_variable.py")
        output_file = tmpdir / "output.txt"
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
    def test_fail_on_exit_code(self, args, expected):
        path = join(HERE, "regrtest_data", "fail_on.py")
        # We set fail-under to be something very low so that even with the warnings
        # and errors that are generated they don't affect the exit code.
        self._runtest([path, "--fail-under=-10"] + args, code=expected)

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
    def test_fail_on_info_only_exit_code(self, args, expected):
        path = join(HERE, "regrtest_data", "fail_on_info_only.py")
        self._runtest([path] + args, code=expected)

    @pytest.mark.parametrize(
        "output_format, expected_output",
        [
            (
                "text",
                "tests/regrtest_data/unused_variable.py:4:4: W0612: Unused variable 'variable' (unused-variable)",
            ),
            (
                "parseable",
                "tests/regrtest_data/unused_variable.py:4: [W0612(unused-variable), test] Unused variable 'variable'",
            ),
            (
                "msvs",
                "tests/regrtest_data/unused_variable.py(4): [W0612(unused-variable)test] Unused variable 'variable'",
            ),
            (
                "colorized",
                "tests/regrtest_data/unused_variable.py:4:4: W0612: [35mUnused variable 'variable'[0m ([35munused-variable[0m)",
            ),
            ("json", '"message": "Unused variable \'variable\'",'),
        ],
    )
    def test_output_file_can_be_combined_with_output_format_option(
        self, tmpdir, output_format, expected_output
    ):
        path = join(HERE, "regrtest_data", "unused_variable.py")
        output_file = tmpdir / "output.txt"
        self._test_output_file(
            [path, f"--output={output_file}", f"--output-format={output_format}"],
            output_file,
            expected_output,
        )

    def test_output_file_can_be_combined_with_custom_reporter(
        self, tmpdir: LocalPath
    ) -> None:
        path = join(HERE, "regrtest_data", "unused_variable.py")
        output_file = tmpdir / "output.txt"
        # It does not really have to be a truly custom reporter.
        # It is only important that it is being passed explicitly to ``Run``.
        myreporter = TextReporter()
        self._run_pylint(
            [path, f"--output={output_file}"],
            out=sys.stdout,
            reporter=myreporter,
        )
        assert output_file.exists()

    def test_output_file_specified_in_rcfile(self, tmpdir: LocalPath) -> None:
        output_file = tmpdir / "output.txt"
        rcfile = tmpdir / "pylintrc"
        rcfile_contents = textwrap.dedent(
            f"""
        [MASTER]
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
    def test_enable_all_extensions() -> None:
        """Test to see if --enable-all-extensions does indeed load all extensions"""
        # Record all extensions
        plugins = []
        for filename in os.listdir(os.path.dirname(extensions.__file__)):
            # pylint: disable=fixme
            # TODO: Remove the check for deprecated check_docs after the extension has been removed
            if (
                filename.endswith(".py")
                and not filename.startswith("_")
                and not filename.startswith("check_docs")
            ):
                plugins.append(f"pylint.extensions.{filename[:-3]}")

        # Check if they are loaded
        runner = Run(
            ["--enable-all-extensions", join(HERE, "regrtest_data", "empty.py")],
            exit=False,
        )
        assert sorted(plugins) == sorted(runner.linter._dynamic_plugins)
