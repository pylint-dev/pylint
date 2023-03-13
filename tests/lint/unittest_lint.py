# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

# pylint: disable=redefined-outer-name

from __future__ import annotations

import argparse
import datetime
import os
import re
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from io import StringIO
from os import chdir, getcwd
from os.path import abspath, dirname, join, sep
from pathlib import Path
from shutil import copy, rmtree

import platformdirs
import pytest
from astroid import nodes
from pytest import CaptureFixture

from pylint import checkers, constants, exceptions, interfaces, lint, testutils
from pylint.checkers.utils import only_required_for_messages
from pylint.constants import (
    MSG_STATE_CONFIDENCE,
    MSG_STATE_SCOPE_CONFIG,
    MSG_STATE_SCOPE_MODULE,
    OLD_DEFAULT_PYLINT_HOME,
    PYLINT_HOME,
    USER_HOME,
    _get_pylint_home,
    _warn_about_old_home,
)
from pylint.exceptions import InvalidMessageError
from pylint.lint import PyLinter, expand_modules
from pylint.message import Message
from pylint.reporters import text
from pylint.testutils import create_files
from pylint.testutils._run import _Run as Run
from pylint.typing import MessageLocationTuple
from pylint.utils import FileState, print_full_documentation, tokenize_module

if os.name == "java":
    if os.name == "nt":
        HOME = "USERPROFILE"
    else:
        HOME = "HOME"
elif sys.platform == "win32":
    HOME = "USERPROFILE"
else:
    HOME = "HOME"


@contextmanager
def fake_home() -> Iterator[str]:
    folder = tempfile.mkdtemp("fake-home")
    old_home = os.environ.get(HOME)
    try:
        os.environ[HOME] = folder
        yield folder
    finally:
        os.environ.pop("PYLINTRC", "")
        if old_home is None:
            del os.environ[HOME]
        else:
            os.environ[HOME] = old_home
        rmtree(folder, ignore_errors=True)


def remove(file: str) -> None:
    try:
        os.remove(file)
    except OSError:
        pass


HERE = abspath(dirname(__file__))
INPUT_DIR = join(HERE, "..", "input")
REGRTEST_DATA_DIR = join(HERE, "..", "regrtest_data")
DATA_DIR = join(HERE, "..", "data")


@contextmanager
def tempdir() -> Iterator[str]:
    """Create a temp directory and change the current location to it.

    This is supposed to be used with a *with* statement.
    """
    tmp = tempfile.mkdtemp()

    # Get real path of tempfile, otherwise test fail on mac os x
    current_dir = getcwd()
    chdir(tmp)
    abs_tmp = abspath(".")

    try:
        yield abs_tmp
    finally:
        chdir(current_dir)
        rmtree(abs_tmp)


@pytest.fixture
def fake_path() -> Iterator[list[str]]:
    orig = list(sys.path)
    fake = ["1", "2", "3"]
    sys.path[:] = fake
    yield fake
    sys.path[:] = orig


def test_no_args(fake_path: list[str]) -> None:
    with lint.augmented_sys_path([]):
        assert sys.path == fake_path
    assert sys.path == fake_path


@pytest.mark.parametrize(
    "case", [["a/b/"], ["a/b"], ["a/b/__init__.py"], ["a/"], ["a"]]
)
def test_one_arg(fake_path: list[str], case: list[str]) -> None:
    with tempdir() as chroot:
        create_files(["a/b/__init__.py"])
        expected = [join(chroot, "a"), *fake_path]

        extra_sys_paths = [
            expand_modules.discover_package_path(arg, []) for arg in case
        ]

        assert sys.path == fake_path
        with lint.augmented_sys_path(extra_sys_paths):
            assert sys.path == expected
        assert sys.path == fake_path


@pytest.mark.parametrize(
    "case",
    [
        ["a/b", "a/c"],
        ["a/c/", "a/b/"],
        ["a/b/__init__.py", "a/c/__init__.py"],
        ["a", "a/c/__init__.py"],
    ],
)
def test_two_similar_args(fake_path: list[str], case: list[str]) -> None:
    with tempdir() as chroot:
        create_files(["a/b/__init__.py", "a/c/__init__.py"])
        expected = [join(chroot, "a"), *fake_path]

        extra_sys_paths = [
            expand_modules.discover_package_path(arg, []) for arg in case
        ]

        assert sys.path == fake_path
        with lint.augmented_sys_path(extra_sys_paths):
            assert sys.path == expected
        assert sys.path == fake_path


@pytest.mark.parametrize(
    "case",
    [
        ["a/b/c/__init__.py", "a/d/__init__.py", "a/e/f.py"],
        ["a/b/c", "a", "a/e"],
        ["a/b/c", "a", "a/b/c", "a/e", "a"],
    ],
)
def test_more_args(fake_path: list[str], case: list[str]) -> None:
    with tempdir() as chroot:
        create_files(["a/b/c/__init__.py", "a/d/__init__.py", "a/e/f.py"])
        expected = [
            join(chroot, suffix)
            for suffix in (sep.join(("a", "b")), "a", sep.join(("a", "e")))
        ] + fake_path

        extra_sys_paths = [
            expand_modules.discover_package_path(arg, []) for arg in case
        ]

        assert sys.path == fake_path
        with lint.augmented_sys_path(extra_sys_paths):
            assert sys.path == expected
        assert sys.path == fake_path


@pytest.fixture(scope="module")
def disable() -> list[str]:
    return ["I"]


@pytest.fixture(scope="module")
def reporter() -> type[testutils.GenericTestReporter]:
    return testutils.GenericTestReporter


@pytest.fixture
def initialized_linter(linter: PyLinter) -> PyLinter:
    linter.open()
    linter.set_current_module("long_test_file", "long_test_file")
    linter.file_state = FileState(
        "long_test_file",
        linter.msgs_store,
        linter.get_ast(
            str(join(REGRTEST_DATA_DIR, "long_test_file.py")), "long_test_file"
        ),
    )
    return linter


def test_pylint_visit_method_taken_in_account(linter: PyLinter) -> None:
    class CustomChecker(checkers.BaseChecker):
        name = "custom"
        msgs = {"W9999": ("", "custom", "")}

        @only_required_for_messages("custom")
        def visit_class(self, _: nodes.ClassDef) -> None:
            pass

    linter.register_checker(CustomChecker(linter))
    linter.open()
    out = StringIO()
    linter.set_reporter(text.TextReporter(out))
    linter.check(["abc"])


def test_enable_message(initialized_linter: PyLinter) -> None:
    linter = initialized_linter
    assert linter.is_message_enabled("W0101")
    assert linter.is_message_enabled("W0102")
    linter.disable("W0101", scope="package")
    linter.disable("W0102", scope="module", line=1)
    assert not linter.is_message_enabled("W0101")
    assert not linter.is_message_enabled("W0102", 1)
    linter.set_current_module("tutu")
    assert not linter.is_message_enabled("W0101")
    assert linter.is_message_enabled("W0102")
    linter.enable("W0101", scope="package")
    linter.enable("W0102", scope="module", line=1)
    assert linter.is_message_enabled("W0101")
    assert linter.is_message_enabled("W0102", 1)


def test_enable_message_category(initialized_linter: PyLinter) -> None:
    linter = initialized_linter
    assert linter.is_message_enabled("W0101")
    assert linter.is_message_enabled("C0202")
    linter.disable("W", scope="package")
    linter.disable("C", scope="module", line=1)
    assert not linter.is_message_enabled("W0101")
    assert linter.is_message_enabled("C0202")
    assert not linter.is_message_enabled("C0202", line=1)
    linter.set_current_module("tutu")
    assert not linter.is_message_enabled("W0101")
    assert linter.is_message_enabled("C0202")
    linter.enable("W", scope="package")
    linter.enable("C", scope="module", line=1)
    assert linter.is_message_enabled("W0101")
    assert linter.is_message_enabled("C0202")
    assert linter.is_message_enabled("C0202", line=1)


def test_message_state_scope(initialized_linter: PyLinter) -> None:
    class FakeConfig(argparse.Namespace):
        confidence = ["HIGH"]

    linter = initialized_linter
    linter.disable("C0202")
    assert MSG_STATE_SCOPE_CONFIG == linter._get_message_state_scope("C0202")
    linter.disable("W0101", scope="module", line=3)
    assert MSG_STATE_SCOPE_CONFIG == linter._get_message_state_scope("C0202")
    assert MSG_STATE_SCOPE_MODULE == linter._get_message_state_scope("W0101", 3)
    linter.enable("W0102", scope="module", line=3)
    assert MSG_STATE_SCOPE_MODULE == linter._get_message_state_scope("W0102", 3)
    linter.config = FakeConfig()
    assert MSG_STATE_CONFIDENCE == linter._get_message_state_scope(
        "this-is-bad", confidence=interfaces.INFERENCE
    )


def test_enable_message_block(initialized_linter: PyLinter) -> None:
    linter = initialized_linter
    linter.open()
    filepath = join(REGRTEST_DATA_DIR, "func_block_disable_msg.py")
    linter.set_current_module("func_block_disable_msg")
    astroid = linter.get_ast(filepath, "func_block_disable_msg")
    linter.file_state = FileState("func_block_disable_msg", linter.msgs_store, astroid)
    linter.process_tokens(tokenize_module(astroid))
    fs = linter.file_state
    # global (module level)
    assert linter.is_message_enabled("W0613")
    assert linter.is_message_enabled("E1101")
    # meth1
    assert linter.is_message_enabled("W0613", 13)
    # meth2
    assert not linter.is_message_enabled("W0613", 18)
    # meth3
    assert not linter.is_message_enabled("E1101", 24)
    assert linter.is_message_enabled("E1101", 26)
    # meth4
    assert not linter.is_message_enabled("E1101", 32)
    assert linter.is_message_enabled("E1101", 36)
    # meth5
    assert not linter.is_message_enabled("E1101", 42)
    assert not linter.is_message_enabled("E1101", 43)
    assert linter.is_message_enabled("E1101", 46)
    assert not linter.is_message_enabled("E1101", 49)
    assert not linter.is_message_enabled("E1101", 51)
    # meth6
    assert not linter.is_message_enabled("E1101", 57)
    assert linter.is_message_enabled("E1101", 61)
    assert not linter.is_message_enabled("E1101", 64)
    assert not linter.is_message_enabled("E1101", 66)

    assert linter.is_message_enabled("E0602", 57)
    assert linter.is_message_enabled("E0602", 61)
    assert not linter.is_message_enabled("E0602", 62)
    assert linter.is_message_enabled("E0602", 64)
    assert linter.is_message_enabled("E0602", 66)
    # meth7
    assert not linter.is_message_enabled("E1101", 70)
    assert linter.is_message_enabled("E1101", 72)
    assert linter.is_message_enabled("E1101", 75)
    assert linter.is_message_enabled("E1101", 77)

    assert fs._suppression_mapping["W0613", 18] == 17
    assert fs._suppression_mapping["E1101", 33] == 30
    assert ("E1101", 46) not in fs._suppression_mapping
    assert fs._suppression_mapping["C0302", 18] == 1
    assert fs._suppression_mapping["C0302", 50] == 1
    # This is tricky. While the disable in line 106 is disabling
    # both 108 and 110, this is usually not what the user wanted.
    # Therefore, we report the closest previous disable comment.
    assert fs._suppression_mapping["E1101", 108] == 106
    assert fs._suppression_mapping["E1101", 110] == 109


def test_enable_by_symbol(initialized_linter: PyLinter) -> None:
    """Messages can be controlled by symbolic names.

    The state is consistent across symbols and numbers.
    """
    linter = initialized_linter
    assert linter.is_message_enabled("W0101")
    assert linter.is_message_enabled("unreachable")
    assert linter.is_message_enabled("W0102")
    assert linter.is_message_enabled("dangerous-default-value")
    linter.disable("unreachable", scope="package")
    linter.disable("dangerous-default-value", scope="module", line=1)
    assert not linter.is_message_enabled("W0101")
    assert not linter.is_message_enabled("unreachable")
    assert not linter.is_message_enabled("W0102", 1)
    assert not linter.is_message_enabled("dangerous-default-value", 1)
    linter.set_current_module("tutu")
    assert not linter.is_message_enabled("W0101")
    assert not linter.is_message_enabled("unreachable")
    assert linter.is_message_enabled("W0102")
    assert linter.is_message_enabled("dangerous-default-value")
    linter.enable("unreachable", scope="package")
    linter.enable("dangerous-default-value", scope="module", line=1)
    assert linter.is_message_enabled("W0101")
    assert linter.is_message_enabled("unreachable")
    assert linter.is_message_enabled("W0102", 1)
    assert linter.is_message_enabled("dangerous-default-value", 1)


def test_enable_report(linter: PyLinter) -> None:
    assert linter.report_is_enabled("RP0001")
    linter.disable("RP0001")
    assert not linter.report_is_enabled("RP0001")
    linter.enable("RP0001")
    assert linter.report_is_enabled("RP0001")


def test_report_output_format_aliased(linter: PyLinter) -> None:
    text.register(linter)
    linter.set_option("output-format", "text")
    assert linter.reporter.__class__.__name__ == "TextReporter"


def test_set_unsupported_reporter(linter: PyLinter) -> None:
    text.register(linter)
    # ImportError
    with pytest.raises(exceptions.InvalidReporterError):
        linter.set_option("output-format", "missing.module.Class")

    # AssertionError
    with pytest.raises(exceptions.InvalidReporterError):
        linter.set_option("output-format", "lint.unittest_lint._CustomPyLinter")

    # AttributeError
    with pytest.raises(exceptions.InvalidReporterError):
        linter.set_option("output-format", "lint.unittest_lint.MyReporter")


def test_set_option_1(initialized_linter: PyLinter) -> None:
    linter = initialized_linter
    linter.set_option("disable", "C0111,W0234")
    assert not linter.is_message_enabled("C0111")
    assert not linter.is_message_enabled("W0234")
    assert linter.is_message_enabled("W0113")
    assert not linter.is_message_enabled("missing-docstring")
    assert not linter.is_message_enabled("non-iterator-returned")


def test_set_option_2(initialized_linter: PyLinter) -> None:
    linter = initialized_linter
    linter.set_option("disable", ("C0111", "W0234"))
    assert not linter.is_message_enabled("C0111")
    assert not linter.is_message_enabled("W0234")
    assert linter.is_message_enabled("W0113")
    assert not linter.is_message_enabled("missing-docstring")
    assert not linter.is_message_enabled("non-iterator-returned")


def test_enable_checkers(linter: PyLinter) -> None:
    linter.disable("design")
    assert "design" not in [c.name for c in linter.prepare_checkers()]
    linter.enable("design")
    assert "design" in [c.name for c in linter.prepare_checkers()]


def test_errors_only(initialized_linter: PyLinter) -> None:
    linter = initialized_linter
    linter._error_mode = True
    linter._parse_error_mode()
    checkers = linter.prepare_checkers()
    checker_names = {c.name for c in checkers}
    should_not = {"design", "format", "metrics", "miscellaneous", "similarities"}
    assert set() == should_not & checker_names


def test_disable_similar(initialized_linter: PyLinter) -> None:
    linter = initialized_linter
    linter.set_option("disable", "RP0801")
    linter.set_option("disable", "R0801")
    assert "similarities" not in [c.name for c in linter.prepare_checkers()]


def test_disable_alot(linter: PyLinter) -> None:
    """Check that we disabled a lot of checkers."""
    linter.set_option("reports", False)
    linter.set_option("disable", "R,C,W")
    checker_names = [c.name for c in linter.prepare_checkers()]
    for cname in ("design", "metrics", "similarities"):
        assert cname not in checker_names, cname


def test_addmessage(linter: PyLinter) -> None:
    linter.set_reporter(testutils.GenericTestReporter())
    linter.open()
    linter.set_current_module("0123")
    linter.add_message("C0301", line=1, args=(1, 2))
    linter.add_message("line-too-long", line=2, args=(3, 4))
    assert len(linter.reporter.messages) == 2
    assert linter.reporter.messages[0] == Message(
        msg_id="C0301",
        symbol="line-too-long",
        msg="Line too long (1/2)",
        confidence=interfaces.Confidence(
            name="UNDEFINED",
            description="Warning without any associated confidence level.",
        ),
        location=MessageLocationTuple(
            abspath="0123",
            path="0123",
            module="0123",
            obj="",
            line=1,
            column=0,
            end_line=None,
            end_column=None,
        ),
    )
    assert linter.reporter.messages[1] == Message(
        msg_id="C0301",
        symbol="line-too-long",
        msg="Line too long (3/4)",
        confidence=interfaces.Confidence(
            name="UNDEFINED",
            description="Warning without any associated confidence level.",
        ),
        location=MessageLocationTuple(
            abspath="0123",
            path="0123",
            module="0123",
            obj="",
            line=2,
            column=0,
            end_line=None,
            end_column=None,
        ),
    )


def test_addmessage_invalid(linter: PyLinter) -> None:
    linter.set_reporter(testutils.GenericTestReporter())
    linter.open()
    linter.set_current_module("0123")

    with pytest.raises(InvalidMessageError) as cm:
        linter.add_message("line-too-long", args=(1, 2))
    assert str(cm.value) == "Message C0301 must provide line, got None"

    with pytest.raises(InvalidMessageError) as cm:
        linter.add_message("line-too-long", line=2, node="fake_node", args=(1, 2))
    assert (
        str(cm.value)
        == "Message C0301 must only provide line, got line=2, node=fake_node"
    )

    with pytest.raises(InvalidMessageError) as cm:
        linter.add_message("C0321")
    assert str(cm.value) == "Message C0321 must provide Node, got None"


def test_load_plugin_command_line() -> None:
    dummy_plugin_path = join(REGRTEST_DATA_DIR, "dummy_plugin")
    sys.path.append(dummy_plugin_path)

    run = Run(
        ["--load-plugins", "dummy_plugin", join(REGRTEST_DATA_DIR, "empty.py")],
        exit=False,
    )
    assert (
        len([ch.name for ch in run.linter.get_checkers() if ch.name == "dummy_plugin"])
        == 2
    )

    sys.path.remove(dummy_plugin_path)


@pytest.mark.usefixtures("pop_pylintrc")
def test_load_plugin_path_manipulation_case_6() -> None:
    """Case 6 refers to GitHub issue #7264.

    This is where we supply a plugin we want to load on both the CLI and
    config file, but that plugin is only loadable after the ``init-hook`` in
    the config file has run. This is not supported, and was previously a silent
    failure. This test ensures a ``bad-plugin-value`` message is emitted.
    """
    dummy_plugin_path = abspath(
        join(REGRTEST_DATA_DIR, "dummy_plugin", "dummy_plugin.py")
    )
    with fake_home() as home_path:
        # construct a basic rc file that just modifies the path
        pylintrc_file = join(home_path, "pylintrc")
        with open(pylintrc_file, "w", encoding="utf8") as out:
            out.writelines(
                [
                    "[MASTER]\n",
                    f"init-hook=\"import sys; sys.path.append(r'{home_path}')\"\n",
                    "load-plugins=copy_dummy\n",
                ]
            )

        copy(dummy_plugin_path, join(home_path, "copy_dummy.py"))

        # To confirm we won't load this module _without_ the init hook running.
        assert home_path not in sys.path

        run = Run(
            [
                "--rcfile",
                pylintrc_file,
                "--load-plugins",
                "copy_dummy",
                join(REGRTEST_DATA_DIR, "empty.py"),
            ],
            reporter=testutils.GenericTestReporter(),
            exit=False,
        )
        assert run._rcfile == pylintrc_file
        assert home_path in sys.path
        # The module should not be loaded
        assert not any(ch.name == "dummy_plugin" for ch in run.linter.get_checkers())

        # There should be a bad-plugin-message for this module
        assert len(run.linter.reporter.messages) == 1
        assert run.linter.reporter.messages[0] == Message(
            msg_id="E0013",
            symbol="bad-plugin-value",
            msg="Plugin 'copy_dummy' is impossible to load, is it installed ? ('No module named 'copy_dummy'')",
            confidence=interfaces.Confidence(
                name="UNDEFINED",
                description="Warning without any associated confidence level.",
            ),
            location=MessageLocationTuple(
                abspath="Command line or configuration file",
                path="Command line or configuration file",
                module="Command line or configuration file",
                obj="",
                line=1,
                column=0,
                end_line=None,
                end_column=None,
            ),
        )

        # Necessary as the executed init-hook modifies sys.path
        sys.path.remove(home_path)


@pytest.mark.usefixtures("pop_pylintrc")
def test_load_plugin_path_manipulation_case_3() -> None:
    """Case 3 refers to GitHub issue #7264.

    This is where we supply a plugin we want to load on the CLI only,
    but that plugin is only loadable after the ``init-hook`` in
    the config file has run. This is not supported, and was previously a silent
    failure. This test ensures a ``bad-plugin-value`` message is emitted.
    """
    dummy_plugin_path = abspath(
        join(REGRTEST_DATA_DIR, "dummy_plugin", "dummy_plugin.py")
    )
    with fake_home() as home_path:
        # construct a basic rc file that just modifies the path
        pylintrc_file = join(home_path, "pylintrc")
        with open(pylintrc_file, "w", encoding="utf8") as out:
            out.writelines(
                [
                    "[MASTER]\n",
                    f"init-hook=\"import sys; sys.path.append(r'{home_path}')\"\n",
                ]
            )

        copy(dummy_plugin_path, join(home_path, "copy_dummy.py"))

        # To confirm we won't load this module _without_ the init hook running.
        assert home_path not in sys.path

        run = Run(
            [
                "--rcfile",
                pylintrc_file,
                "--load-plugins",
                "copy_dummy",
                join(REGRTEST_DATA_DIR, "empty.py"),
            ],
            reporter=testutils.GenericTestReporter(),
            exit=False,
        )
        assert run._rcfile == pylintrc_file
        assert home_path in sys.path
        # The module should not be loaded
        assert not any(ch.name == "dummy_plugin" for ch in run.linter.get_checkers())

        # There should be a bad-plugin-message for this module
        assert len(run.linter.reporter.messages) == 1
        assert run.linter.reporter.messages[0] == Message(
            msg_id="E0013",
            symbol="bad-plugin-value",
            msg="Plugin 'copy_dummy' is impossible to load, is it installed ? ('No module named 'copy_dummy'')",
            confidence=interfaces.Confidence(
                name="UNDEFINED",
                description="Warning without any associated confidence level.",
            ),
            location=MessageLocationTuple(
                abspath="Command line or configuration file",
                path="Command line or configuration file",
                module="Command line or configuration file",
                obj="",
                line=1,
                column=0,
                end_line=None,
                end_column=None,
            ),
        )

        # Necessary as the executed init-hook modifies sys.path
        sys.path.remove(home_path)


@pytest.mark.usefixtures("pop_pylintrc")
def test_load_plugin_pylintrc_order_independent() -> None:
    """Test that the init-hook is called independent of the order in a config file.

    We want to ensure that any path manipulation in init hook
    that means a plugin can load (as per GitHub Issue #7264 Cases 4+7)
    runs before the load call, regardless of the order of lines in the
    pylintrc file.
    """
    dummy_plugin_path = abspath(
        join(REGRTEST_DATA_DIR, "dummy_plugin", "dummy_plugin.py")
    )

    with fake_home() as home_path:
        copy(dummy_plugin_path, join(home_path, "copy_dummy.py"))
        # construct a basic rc file that just modifies the path
        pylintrc_file_before = join(home_path, "pylintrc_before")
        with open(pylintrc_file_before, "w", encoding="utf8") as out:
            out.writelines(
                [
                    "[MASTER]\n",
                    f"init-hook=\"import sys; sys.path.append(r'{home_path}')\"\n",
                    "load-plugins=copy_dummy\n",
                ]
            )
        pylintrc_file_after = join(home_path, "pylintrc_after")
        with open(pylintrc_file_after, "w", encoding="utf8") as out:
            out.writelines(
                [
                    "[MASTER]\n",
                    "load-plugins=copy_dummy\n"
                    f"init-hook=\"import sys; sys.path.append(r'{home_path}')\"\n",
                ]
            )
        for rcfile in (pylintrc_file_before, pylintrc_file_after):
            # To confirm we won't load this module _without_ the init hook running.
            assert home_path not in sys.path
            run = Run(
                [
                    "--rcfile",
                    rcfile,
                    join(REGRTEST_DATA_DIR, "empty.py"),
                ],
                exit=False,
            )
            assert (
                len(
                    [
                        ch.name
                        for ch in run.linter.get_checkers()
                        if ch.name == "dummy_plugin"
                    ]
                )
                == 2
            )
            assert run._rcfile == rcfile
            assert home_path in sys.path

            # Necessary as the executed init-hook modifies sys.path
            sys.path.remove(home_path)


def test_load_plugin_command_line_before_init_hook() -> None:
    """Check that the order of 'load-plugins' and 'init-hook' doesn't affect execution."""
    dummy_plugin_path = abspath(
        join(REGRTEST_DATA_DIR, "dummy_plugin", "dummy_plugin.py")
    )

    with fake_home() as home_path:
        copy(dummy_plugin_path, join(home_path, "copy_dummy.py"))
        # construct a basic rc file that just modifies the path
        assert home_path not in sys.path
        run = Run(
            [
                "--load-plugins",
                "copy_dummy",
                "--init-hook",
                f'import sys; sys.path.append(r"{home_path}")',
                join(REGRTEST_DATA_DIR, "empty.py"),
            ],
            exit=False,
        )
        assert home_path in sys.path
        assert (
            len(
                [
                    ch.name
                    for ch in run.linter.get_checkers()
                    if ch.name == "dummy_plugin"
                ]
            )
            == 2
        )

        # Necessary as the executed init-hook modifies sys.path
        sys.path.remove(home_path)


def test_load_plugin_command_line_with_init_hook_command_line() -> None:
    dummy_plugin_path = abspath(
        join(REGRTEST_DATA_DIR, "dummy_plugin", "dummy_plugin.py")
    )

    with fake_home() as home_path:
        copy(dummy_plugin_path, join(home_path, "copy_dummy.py"))
        # construct a basic rc file that just modifies the path
        assert home_path not in sys.path
        run = Run(
            [
                "--init-hook",
                f'import sys; sys.path.append(r"{home_path}")',
                "--load-plugins",
                "copy_dummy",
                join(REGRTEST_DATA_DIR, "empty.py"),
            ],
            exit=False,
        )
        assert (
            len(
                [
                    ch.name
                    for ch in run.linter.get_checkers()
                    if ch.name == "dummy_plugin"
                ]
            )
            == 2
        )
        assert home_path in sys.path

        # Necessary as the executed init-hook modifies sys.path
        sys.path.remove(home_path)


def test_load_plugin_config_file() -> None:
    dummy_plugin_path = join(REGRTEST_DATA_DIR, "dummy_plugin")
    sys.path.append(dummy_plugin_path)
    config_path = join(REGRTEST_DATA_DIR, "dummy_plugin.rc")

    run = Run(
        ["--rcfile", config_path, join(REGRTEST_DATA_DIR, "empty.py")],
        exit=False,
    )
    assert (
        len([ch.name for ch in run.linter.get_checkers() if ch.name == "dummy_plugin"])
        == 2
    )

    sys.path.remove(dummy_plugin_path)


def test_load_plugin_configuration() -> None:
    dummy_plugin_path = join(REGRTEST_DATA_DIR, "dummy_plugin")
    sys.path.append(dummy_plugin_path)

    run = Run(
        [
            "--load-plugins",
            "dummy_conf_plugin",
            "--ignore",
            "foo,bar",
            join(REGRTEST_DATA_DIR, "empty.py"),
        ],
        exit=False,
    )

    sys.path.remove(dummy_plugin_path)
    assert run.linter.config.ignore == ["foo", "bar", "bin"]


def test_init_hooks_called_before_load_plugins() -> None:
    with pytest.raises(RuntimeError):
        Run(["--load-plugins", "unexistant", "--init-hook", "raise RuntimeError"])
    with pytest.raises(RuntimeError):
        Run(["--init-hook", "raise RuntimeError", "--load-plugins", "unexistant"])
    with pytest.raises(SystemExit):
        Run(["--init-hook"])


def test_analyze_explicit_script(linter: PyLinter) -> None:
    linter.set_reporter(testutils.GenericTestReporter())
    linter.check([os.path.join(DATA_DIR, "ascript")])
    assert len(linter.reporter.messages) == 1
    assert linter.reporter.messages[0] == Message(
        msg_id="C0301",
        symbol="line-too-long",
        msg="Line too long (175/100)",
        confidence=interfaces.Confidence(
            name="UNDEFINED",
            description="Warning without any associated confidence level.",
        ),
        location=MessageLocationTuple(
            abspath=os.path.join(abspath(dirname(__file__)), "ascript").replace(
                f"lint{os.path.sep}ascript", f"data{os.path.sep}ascript"
            ),
            path=f"tests{os.path.sep}data{os.path.sep}ascript",
            module="data.ascript",
            obj="",
            line=2,
            column=0,
            end_line=None,
            end_column=None,
        ),
    )


def test_full_documentation(linter: PyLinter) -> None:
    out = StringIO()
    print_full_documentation(linter, out)
    output = out.getvalue()
    # A few spot checks only
    for re_str in (
        # auto-generated text
        "^Pylint global options and switches$",
        "Verbatim name of the checker is ``variables``",
        # messages
        "^:undefined-loop-variable \\(W0631\\): *",
        # options
        "^:dummy-variables-rgx:",
    ):
        regexp = re.compile(re_str, re.MULTILINE)
        assert re.search(regexp, output)


def test_list_msgs_enabled(
    initialized_linter: PyLinter, capsys: CaptureFixture[str]
) -> None:
    linter = initialized_linter
    linter.enable("W0101", scope="package")
    linter.disable("W0102", scope="package")
    linter.list_messages_enabled()

    lines = capsys.readouterr().out.splitlines()

    assert "Enabled messages:" in lines
    assert "  unreachable (W0101)" in lines

    assert "Disabled messages:" in lines
    disabled_ix = lines.index("Disabled messages:")

    # W0101 should be in the enabled section
    assert lines.index("  unreachable (W0101)") < disabled_ix

    assert "  dangerous-default-value (W0102)" in lines
    # W0102 should be in the disabled section
    assert lines.index("  dangerous-default-value (W0102)") > disabled_ix


@pytest.fixture
def pop_pylintrc() -> None:
    os.environ.pop("PYLINTRC", None)


@pytest.mark.usefixtures("pop_pylintrc")
def test_pylint_home() -> None:
    uhome = os.path.expanduser("~")
    if uhome == "~":
        expected = OLD_DEFAULT_PYLINT_HOME
    else:
        expected = platformdirs.user_cache_dir("pylint")
    assert constants.PYLINT_HOME == expected
    assert PYLINT_HOME == expected


def test_pylint_home_from_environ() -> None:
    try:
        pylintd = join(tempfile.gettempdir(), OLD_DEFAULT_PYLINT_HOME)
        os.environ["PYLINTHOME"] = pylintd
        try:
            assert _get_pylint_home() == pylintd
        finally:
            try:
                rmtree(pylintd)
            except FileNotFoundError:
                pass
    finally:
        del os.environ["PYLINTHOME"]


def test_warn_about_old_home(capsys: CaptureFixture[str]) -> None:
    """Test that we correctly warn about old_home."""
    # Create old home
    old_home = Path(USER_HOME) / OLD_DEFAULT_PYLINT_HOME
    old_home.mkdir(parents=True, exist_ok=True)

    # Create spam prevention file
    ten_years_ago = datetime.datetime.now() - datetime.timedelta(weeks=520)
    new_prevention_file = Path(PYLINT_HOME) / ten_years_ago.strftime(
        "pylint_warned_about_old_cache_already_%Y-%m-%d.temp"
    )
    with open(new_prevention_file, "w", encoding="utf8") as f:
        f.write("")

    # Remove current prevention file
    cur_prevention_file = Path(PYLINT_HOME) / datetime.datetime.now().strftime(
        "pylint_warned_about_old_cache_already_%Y-%m-%d.temp"
    )
    if cur_prevention_file.exists():
        os.remove(cur_prevention_file)

    _warn_about_old_home(Path(PYLINT_HOME))

    assert not new_prevention_file.exists()
    assert cur_prevention_file.exists()

    out = capsys.readouterr()
    assert "PYLINTHOME is now" in out.err


class _CustomPyLinter(PyLinter):
    @staticmethod
    def should_analyze_file(modname: str, path: str, is_argument: bool = False) -> bool:
        if os.path.basename(path) == "wrong.py":
            return False

        return super(_CustomPyLinter, _CustomPyLinter).should_analyze_file(
            modname, path, is_argument=is_argument
        )


@pytest.mark.needs_two_cores
def test_custom_should_analyze_file() -> None:
    """Check that we can write custom should_analyze_file that work
    even for arguments.
    """
    package_dir = os.path.join(REGRTEST_DATA_DIR, "bad_package")
    wrong_file = os.path.join(package_dir, "wrong.py")

    for jobs in (1, 2):
        reporter = testutils.GenericTestReporter()
        linter = _CustomPyLinter()
        linter.config.jobs = jobs
        linter.config.persistent = 0
        linter.open()
        linter.set_reporter(reporter)

        try:
            sys.path.append(os.path.dirname(package_dir))
            linter.check([package_dir, wrong_file])
        finally:
            sys.path.pop()

        messages = reporter.messages
        assert len(messages) == 1
        assert "invalid syntax" in messages[0].msg


# we do the check with jobs=1 as well, so that we are sure that the duplicates
# are created by the multiprocessing problem.
@pytest.mark.needs_two_cores
@pytest.mark.parametrize("jobs", [1, 2])
def test_multiprocessing(jobs: int) -> None:
    """Check that multiprocessing does not create duplicates."""
    # For the bug (#3584) to show up we need more than one file with issues
    # per process
    filenames = [
        "special_attr_scope_lookup_crash.py",
        "syntax_error.py",
        "unused_variable.py",
        "wildcard.py",
        "wrong_import_position.py",
    ]

    reporter = testutils.GenericTestReporter()
    linter = PyLinter()
    linter.config.jobs = jobs
    linter.config.persistent = 0
    linter.open()
    linter.set_reporter(reporter)

    try:
        sys.path.append(os.path.dirname(REGRTEST_DATA_DIR))
        linter.check([os.path.join(REGRTEST_DATA_DIR, fname) for fname in filenames])
    finally:
        sys.path.pop()

    messages = reporter.messages
    assert len(messages) == len(set(messages))


def test_filename_with__init__(initialized_linter: PyLinter) -> None:
    # This tracks a regression where a file whose name ends in __init__.py,
    # such as flycheck__init__.py, would accidentally lead to linting the
    # entire containing directory.
    reporter = testutils.GenericTestReporter()
    linter = initialized_linter
    linter.open()
    linter.set_reporter(reporter)
    filepath = join(INPUT_DIR, "not__init__.py")
    linter.check([filepath])
    messages = reporter.messages
    assert len(messages) == 0


def test_by_module_statement_value(initialized_linter: PyLinter) -> None:
    """Test "statement" for each module analyzed of computed correctly."""
    linter = initialized_linter
    linter.check([os.path.join(os.path.dirname(__file__), "data")])

    by_module_stats = linter.stats.by_module
    for module, module_stats in by_module_stats.items():
        linter2 = initialized_linter
        if module == "data":
            linter2.check([os.path.join(os.path.dirname(__file__), "data/__init__.py")])
        else:
            linter2.check([os.path.join(os.path.dirname(__file__), module)])

        # Check that the by_module "statement" is equal to the global "statement"
        # computed for that module
        assert module_stats["statement"] == linter2.stats.statement


@pytest.mark.parametrize(
    "ignore_parameter,ignore_parameter_value",
    [
        ("--ignore", "failing.py"),
        ("--ignore", "ignored_subdirectory"),
        ("--ignore-patterns", "failing.*"),
        ("--ignore-patterns", "ignored_*"),
        ("--ignore-paths", ".*directory/ignored.*"),
        ("--ignore-paths", ".*ignored.*/failing.*"),
    ],
)
def test_recursive_ignore(ignore_parameter: str, ignore_parameter_value: str) -> None:
    run = Run(
        [
            "--recursive",
            "y",
            ignore_parameter,
            ignore_parameter_value,
            join(REGRTEST_DATA_DIR, "directory"),
        ],
        exit=False,
    )

    linted_files = run.linter._iterate_file_descrs(
        tuple(run.linter._discover_files([join(REGRTEST_DATA_DIR, "directory")]))
    )
    linted_file_paths = [file_item.filepath for file_item in linted_files]

    ignored_file = os.path.abspath(
        join(REGRTEST_DATA_DIR, "directory", "ignored_subdirectory", "failing.py")
    )
    assert ignored_file not in linted_file_paths

    for regrtest_data_module in (
        ("directory", "subdirectory", "subsubdirectory", "module.py"),
        ("directory", "subdirectory", "module.py"),
        ("directory", "package", "module.py"),
        ("directory", "package", "subpackage", "module.py"),
    ):
        module = os.path.abspath(join(REGRTEST_DATA_DIR, *regrtest_data_module))
    assert module in linted_file_paths


def test_source_roots_globbing() -> None:
    run = Run(
        [
            "--source-roots",
            join(REGRTEST_DATA_DIR, "pep420", "basic", "*"),
            join(REGRTEST_DATA_DIR, "pep420", "basic", "project"),
        ],
        exit=False,
    )
    assert run.linter.config.source_roots == [
        join(REGRTEST_DATA_DIR, "pep420", "basic", "project")
    ]


def test_recursive_implicit_namespace() -> None:
    run = Run(
        [
            "--verbose",
            "--recursive",
            "y",
            "--source-roots",
            join(REGRTEST_DATA_DIR, "pep420", "basic", "project"),
            join(REGRTEST_DATA_DIR, "pep420", "basic"),
        ],
        exit=False,
    )
    assert run.linter.file_state.base_name == "namespace.package"


def test_recursive_implicit_namespace_wrapper() -> None:
    run = Run(
        [
            "--recursive",
            "y",
            "--source-roots",
            join(REGRTEST_DATA_DIR, "pep420", "wrapper", "project"),
            join(REGRTEST_DATA_DIR, "pep420", "wrapper"),
        ],
        exit=False,
    )
    run.linter.set_reporter(testutils.GenericTestReporter())
    run.linter.check([join(REGRTEST_DATA_DIR, "pep420", "wrapper")])
    assert run.linter.reporter.messages == []


def test_globbing() -> None:
    run = Run(
        [
            "--verbose",
            "--source-roots",
            join(REGRTEST_DATA_DIR, "pep420", "basic", "project"),
            join(REGRTEST_DATA_DIR, "pep420", "basic", "project", "**", "__init__.py"),
        ],
        exit=False,
    )
    assert run.linter.file_state.base_name == "namespace.package.__init__"


def test_relative_imports(initialized_linter: PyLinter) -> None:
    """Regression test for https://github.com/PyCQA/pylint/issues/3651"""
    linter = initialized_linter
    with tempdir() as tmpdir:
        create_files(["x/y/__init__.py", "x/y/one.py", "x/y/two.py"], tmpdir)
        with open("x/y/__init__.py", "w", encoding="utf-8") as f:
            f.write(
                """
\"\"\"Module x.y\"\"\"
from .one import ONE
from .two import TWO
"""
            )
        with open("x/y/one.py", "w", encoding="utf-8") as f:
            f.write(
                """
\"\"\"Module x.y.one\"\"\"
ONE = 1
"""
            )
        with open("x/y/two.py", "w", encoding="utf-8") as f:
            f.write(
                """
\"\"\"Module x.y.two\"\"\"
from .one import ONE
TWO = ONE + ONE
"""
            )
        linter.check(["x/y"])
    assert not linter.stats.by_msg


def test_import_sibling_module_from_namespace(initialized_linter: PyLinter) -> None:
    """If the parent directory above `namespace` is on sys.path, ensure that
    modules under `namespace` can import each other without raising `import-error`."""
    linter = initialized_linter
    with tempdir() as tmpdir:
        create_files(["namespace/submodule1.py", "namespace/submodule2.py"])
        second_path = Path("namespace/submodule2.py")
        with open(second_path, "w", encoding="utf-8") as f:
            f.write(
                """\"\"\"This module imports submodule1.\"\"\"
import submodule1
print(submodule1)
"""
            )
        os.chdir("namespace")
        extra_sys_paths = [expand_modules.discover_package_path(tmpdir, [])]

        # Add the parent directory to sys.path
        with lint.augmented_sys_path(extra_sys_paths):
            linter.check(["submodule2.py"])
    assert not linter.stats.by_msg


def test_lint_namespace_package_under_dir(initialized_linter: PyLinter) -> None:
    """Regression test for https://github.com/PyCQA/pylint/issues/1667"""
    linter = initialized_linter
    with tempdir():
        create_files(["outer/namespace/__init__.py", "outer/namespace/module.py"])
        linter.check(["outer.namespace"])
    assert not linter.stats.by_msg


def test_lint_namespace_package_under_dir_on_path(initialized_linter: PyLinter) -> None:
    """If the directory above a namespace package is on sys.path,
    the namespace module under it is linted."""
    linter = initialized_linter
    with tempdir() as tmpdir:
        create_files(["namespace_on_path/submodule1.py"])
        os.chdir(tmpdir)
        extra_sys_paths = [expand_modules.discover_package_path(tmpdir, [])]
        with lint.augmented_sys_path(extra_sys_paths):
            linter.check(["namespace_on_path"])
    assert linter.file_state.base_name == "namespace_on_path"
