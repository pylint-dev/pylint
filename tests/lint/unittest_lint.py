# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

# pylint: disable=redefined-outer-name

import os
import re
import sys
import tempfile
from contextlib import contextmanager
from importlib import reload
from io import StringIO
from os import chdir, getcwd
from os.path import abspath, basename, dirname, isdir, join, sep
from shutil import rmtree
from typing import Iterable, Iterator, List, Optional, Tuple

import platformdirs
import pytest
from pytest import CaptureFixture

from pylint import checkers, config, exceptions, interfaces, lint, testutils
from pylint.checkers.utils import check_messages
from pylint.constants import (
    MSG_STATE_CONFIDENCE,
    MSG_STATE_SCOPE_CONFIG,
    MSG_STATE_SCOPE_MODULE,
    OLD_DEFAULT_PYLINT_HOME,
)
from pylint.exceptions import InvalidMessageError
from pylint.lint import ArgumentPreprocessingError, PyLinter, Run, preprocess_options
from pylint.message import Message
from pylint.reporters import text
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
def fake_home() -> Iterator:
    folder = tempfile.mkdtemp("fake-home")
    old_home = os.environ.get(HOME)
    try:
        os.environ[HOME] = folder
        yield
    finally:
        os.environ.pop("PYLINTRC", "")
        if old_home is None:
            del os.environ[HOME]
        else:
            os.environ[HOME] = old_home
        rmtree(folder, ignore_errors=True)


def remove(file):
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


def create_files(paths: List[str], chroot: str = ".") -> None:
    """Creates directories and files found in <path>.

    :param list paths: list of relative paths to files or directories
    :param str chroot: the root directory in which paths will be created

    >>> from os.path import isdir, isfile
    >>> isdir('/tmp/a')
    False
    >>> create_files(['a/b/foo.py', 'a/b/c/', 'a/b/c/d/e.py'], '/tmp')
    >>> isdir('/tmp/a')
    True
    >>> isdir('/tmp/a/b/c')
    True
    >>> isfile('/tmp/a/b/c/d/e.py')
    True
    >>> isfile('/tmp/a/b/foo.py')
    True
    """
    dirs, files = set(), set()
    for path in paths:
        path = join(chroot, path)
        filename = basename(path)
        # path is a directory path
        if filename == "":
            dirs.add(path)
        # path is a filename path
        else:
            dirs.add(dirname(path))
            files.add(path)
    for dirpath in dirs:
        if not isdir(dirpath):
            os.makedirs(dirpath)
    for filepath in files:
        with open(filepath, "w", encoding="utf-8"):
            pass


@pytest.fixture
def fake_path() -> Iterator[Iterable[str]]:
    orig = list(sys.path)
    fake: Iterable[str] = ["1", "2", "3"]
    sys.path[:] = fake
    yield fake
    sys.path[:] = orig


def test_no_args(fake_path: List[int]) -> None:
    with lint.fix_import_path([]):
        assert sys.path == fake_path
    assert sys.path == fake_path


@pytest.mark.parametrize(
    "case", [["a/b/"], ["a/b"], ["a/b/__init__.py"], ["a/"], ["a"]]
)
def test_one_arg(fake_path: List[str], case: List[str]) -> None:
    with tempdir() as chroot:
        create_files(["a/b/__init__.py"])
        expected = [join(chroot, "a")] + fake_path

        assert sys.path == fake_path
        with lint.fix_import_path(case):
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
def test_two_similar_args(fake_path, case):
    with tempdir() as chroot:
        create_files(["a/b/__init__.py", "a/c/__init__.py"])
        expected = [join(chroot, "a")] + fake_path

        assert sys.path == fake_path
        with lint.fix_import_path(case):
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
def test_more_args(fake_path, case):
    with tempdir() as chroot:
        create_files(["a/b/c/__init__.py", "a/d/__init__.py", "a/e/f.py"])
        expected = [
            join(chroot, suffix)
            for suffix in (sep.join(("a", "b")), "a", sep.join(("a", "e")))
        ] + fake_path

        assert sys.path == fake_path
        with lint.fix_import_path(case):
            assert sys.path == expected
        assert sys.path == fake_path


@pytest.fixture(scope="module")
def disable():
    return ["I"]


@pytest.fixture(scope="module")
def reporter():
    return testutils.GenericTestReporter


@pytest.fixture
def initialized_linter(linter: PyLinter) -> PyLinter:
    linter.open()
    linter.set_current_module("toto", "mydir/toto")
    linter.file_state = FileState("toto")
    return linter


def test_pylint_visit_method_taken_in_account(linter: PyLinter) -> None:
    class CustomChecker(checkers.BaseChecker):
        __implements__ = interfaces.IAstroidChecker
        name = "custom"
        msgs = {"W9999": ("", "custom", "")}

        @check_messages("custom")
        def visit_class(self, _):
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
    class FakeConfig:
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
    linter.process_tokens(tokenize_module(astroid))
    fs = linter.file_state
    fs.collect_block_lines(linter.msgs_store, astroid)
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

    fs = linter.file_state
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
    with pytest.raises(exceptions.InvalidReporterError):
        linter.set_option("output-format", "missing.module.Class")


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
    assert not ("design" in [c.name for c in linter.prepare_checkers()])
    linter.enable("design")
    assert "design" in [c.name for c in linter.prepare_checkers()]


def test_errors_only(initialized_linter: PyLinter) -> None:
    linter = initialized_linter
    linter.error_mode()
    checkers = linter.prepare_checkers()
    checker_names = {c.name for c in checkers}
    should_not = {"design", "format", "metrics", "miscellaneous", "similarities"}
    assert set() == should_not & checker_names


def test_disable_similar(initialized_linter: PyLinter) -> None:
    linter = initialized_linter
    linter.set_option("disable", "RP0801")
    linter.set_option("disable", "R0801")
    assert not ("similarities" in [c.name for c in linter.prepare_checkers()])


def test_disable_alot(linter: PyLinter) -> None:
    """Check that we disabled a lot of checkers."""
    linter.set_option("reports", False)
    linter.set_option("disable", "R,C,W")
    checker_names = [c.name for c in linter.prepare_checkers()]
    for cname in ("design", "metrics", "similarities"):
        assert not (cname in checker_names), cname


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
    assert run.linter.config.black_list == ["foo", "bar", "bin"]


def test_init_hooks_called_before_load_plugins() -> None:
    with pytest.raises(RuntimeError):
        Run(["--load-plugins", "unexistant", "--init-hook", "raise RuntimeError"])
    with pytest.raises(RuntimeError):
        Run(["--init-hook", "raise RuntimeError", "--load-plugins", "unexistant"])


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
        # autogenerated text
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
    initialized_linter: PyLinter, capsys: CaptureFixture
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
    assert config.PYLINT_HOME == expected

    try:
        pylintd = join(tempfile.gettempdir(), OLD_DEFAULT_PYLINT_HOME)
        os.environ["PYLINTHOME"] = pylintd
        try:
            reload(config)
            assert config.PYLINT_HOME == pylintd
        finally:
            try:
                rmtree(pylintd)
            except FileNotFoundError:
                pass
    finally:
        del os.environ["PYLINTHOME"]


@pytest.mark.usefixtures("pop_pylintrc")
def test_pylintrc() -> None:
    with fake_home():
        current_dir = getcwd()
        chdir(os.path.dirname(os.path.abspath(sys.executable)))
        try:
            assert config.find_pylintrc() is None
            os.environ["PYLINTRC"] = join(tempfile.gettempdir(), ".pylintrc")
            assert config.find_pylintrc() is None
            os.environ["PYLINTRC"] = "."
            assert config.find_pylintrc() is None
        finally:
            chdir(current_dir)
            reload(config)


@pytest.mark.usefixtures("pop_pylintrc")
def test_pylintrc_parentdir() -> None:
    with tempdir() as chroot:

        create_files(
            [
                "a/pylintrc",
                "a/b/__init__.py",
                "a/b/pylintrc",
                "a/b/c/__init__.py",
                "a/b/c/d/__init__.py",
                "a/b/c/d/e/.pylintrc",
            ]
        )
        with fake_home():
            assert config.find_pylintrc() is None
        results = {
            "a": join(chroot, "a", "pylintrc"),
            "a/b": join(chroot, "a", "b", "pylintrc"),
            "a/b/c": join(chroot, "a", "b", "pylintrc"),
            "a/b/c/d": join(chroot, "a", "b", "pylintrc"),
            "a/b/c/d/e": join(chroot, "a", "b", "c", "d", "e", ".pylintrc"),
        }
        for basedir, expected in results.items():
            os.chdir(join(chroot, basedir))
            assert config.find_pylintrc() == expected


@pytest.mark.usefixtures("pop_pylintrc")
def test_pylintrc_parentdir_no_package() -> None:
    with tempdir() as chroot:
        with fake_home():
            create_files(["a/pylintrc", "a/b/pylintrc", "a/b/c/d/__init__.py"])
            assert config.find_pylintrc() is None
            results = {
                "a": join(chroot, "a", "pylintrc"),
                "a/b": join(chroot, "a", "b", "pylintrc"),
                "a/b/c": None,
                "a/b/c/d": None,
            }
            for basedir, expected in results.items():
                os.chdir(join(chroot, basedir))
                assert config.find_pylintrc() == expected


class TestPreprocessOptions:
    def _callback(self, name: str, value: Optional[str]) -> None:
        self.args.append((name, value))

    def test_value_equal(self) -> None:
        self.args: List[Tuple[str, Optional[str]]] = []
        preprocess_options(
            ["--foo", "--bar=baz", "--qu=ux"],
            {"foo": (self._callback, False), "qu": (self._callback, True)},
        )
        assert [("foo", None), ("qu", "ux")] == self.args

    def test_value_space(self) -> None:
        self.args = []
        preprocess_options(["--qu", "ux"], {"qu": (self._callback, True)})
        assert [("qu", "ux")] == self.args

    @staticmethod
    def test_error_missing_expected_value() -> None:
        with pytest.raises(ArgumentPreprocessingError):
            preprocess_options(["--foo", "--bar", "--qu=ux"], {"bar": (None, True)})
        with pytest.raises(ArgumentPreprocessingError):
            preprocess_options(["--foo", "--bar"], {"bar": (None, True)})

    @staticmethod
    def test_error_unexpected_value() -> None:
        with pytest.raises(ArgumentPreprocessingError):
            preprocess_options(
                ["--foo", "--bar=spam", "--qu=ux"], {"bar": (None, False)}
            )


class _CustomPyLinter(PyLinter):
    @staticmethod
    def should_analyze_file(modname: str, path: str, is_argument: bool = False) -> bool:
        if os.path.basename(path) == "wrong.py":
            return False

        return super(_CustomPyLinter, _CustomPyLinter).should_analyze_file(
            modname, path, is_argument=is_argument
        )


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
