# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import csv
import operator
import platform
import sys
from collections import Counter
from io import StringIO, TextIOWrapper
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

import pytest
from _pytest.config import Config

from pylint import checkers
from pylint.lint import PyLinter
from pylint.testutils.constants import _EXPECTED_RE, _OPERATORS, UPDATE_OPTION
from pylint.testutils.functional_test_file import (
    FunctionalTestFile,
    NoFileError,
    parse_python_version,
)
from pylint.testutils.output_line import OutputLine
from pylint.testutils.reporter_for_tests import FunctionalTestReporter
from pylint.utils import utils

if TYPE_CHECKING:
    from typing import Counter as CounterType  # typing.Counter added in Python 3.6.1


class LintModuleTest:
    maxDiff = None

    def __init__(self, test_file: FunctionalTestFile, config: Optional[Config] = None):
        _test_reporter = FunctionalTestReporter()
        self._linter = PyLinter()
        self._linter.set_reporter(_test_reporter)
        self._linter.config.persistent = 0
        checkers.initialize(self._linter)
        self._linter.disable("suppressed-message")
        self._linter.disable("locally-disabled")
        self._linter.disable("useless-suppression")
        try:
            self._linter.read_config_file(test_file.option_file)
            if self._linter.cfgfile_parser.has_option("MASTER", "load-plugins"):
                plugins = utils._splitstrip(
                    self._linter.cfgfile_parser.get("MASTER", "load-plugins")
                )
                self._linter.load_plugin_modules(plugins)
            self._linter.load_config_file()
        except NoFileError:
            pass
        self._test_file = test_file
        self._config = config

    def setUp(self):
        if self._should_be_skipped_due_to_version():
            pytest.skip(
                f"Test cannot run with Python {sys.version.split(' ', maxsplit=1)[0]}."
            )
        missing = []
        for requirement in self._test_file.options["requires"]:
            try:
                __import__(requirement)
            except ImportError:
                missing.append(requirement)
        if missing:
            pytest.skip(f"Requires {','.join(missing)} to be present.")
        except_implementations = self._test_file.options["except_implementations"]
        if except_implementations:
            implementations = [i.strip() for i in except_implementations.split(",")]
            if platform.python_implementation() in implementations:
                msg = "Test cannot run with Python implementation %r"
                pytest.skip(msg % platform.python_implementation())
        excluded_platforms = self._test_file.options["exclude_platforms"]
        if excluded_platforms:
            platforms = [p.strip() for p in excluded_platforms.split(",")]
            if sys.platform.lower() in platforms:
                pytest.skip(f"Test cannot run on platform {sys.platform!r}")

    def runTest(self):
        self._runTest()

    def _should_be_skipped_due_to_version(self):
        return (
            sys.version_info < self._test_file.options["min_pyver"]
            or sys.version_info > self._test_file.options["max_pyver"]
        )

    def __str__(self):
        return f"{self._test_file.base} ({self.__class__.__module__}.{self.__class__.__name__})"

    @staticmethod
    def get_expected_messages(stream: TextIOWrapper) -> "CounterType[Tuple[int, str]]":
        """Parses a file and get expected messages.

        :param stream: File-like input stream.
        :type stream: enumerable
        :returns: A dict mapping line,msg-symbol tuples to the count on this line.
        :rtype: dict
        """
        messages: "CounterType[Tuple[int, str]]" = Counter()
        for i, line in enumerate(stream):
            match = _EXPECTED_RE.search(line)
            if match is None:
                continue
            line = match.group("line")
            if line is None:
                lineno = i + 1
            elif line.startswith("+") or line.startswith("-"):
                lineno = i + 1 + int(line)
            else:
                lineno = int(line)

            version = match.group("version")
            op = match.group("op")
            if version:
                required = parse_python_version(version)
                if not _OPERATORS[op](sys.version_info, required):
                    continue

            for msg_id in match.group("msgs").split(","):
                messages[lineno, msg_id.strip()] += 1
        return messages

    @staticmethod
    def multiset_difference(
        expected_entries: "CounterType", actual_entries: "CounterType"
    ) -> Tuple["CounterType", Dict[str, int]]:
        """Takes two multisets and compares them.

        A multiset is a dict with the cardinality of the key as the value."""
        missing = expected_entries.copy()
        missing.subtract(actual_entries)
        unexpected = {}
        for key, value in list(missing.items()):
            if value <= 0:
                missing.pop(key)
                if value < 0:
                    unexpected[key] = -value
        return missing, unexpected

    # pylint: disable=consider-using-with
    def _open_expected_file(self):
        try:
            return open(self._test_file.expected_output, encoding="utf-8")
        except FileNotFoundError:
            return StringIO("")

    # pylint: disable=consider-using-with
    def _open_source_file(self):
        if self._test_file.base == "invalid_encoded_data":
            return open(self._test_file.source, encoding="utf-8")
        if "latin1" in self._test_file.base:
            return open(self._test_file.source, encoding="latin1")
        return open(self._test_file.source, encoding="utf8")

    def _get_expected(self):
        with self._open_source_file() as f:
            expected_msgs = self.get_expected_messages(f)
        if not expected_msgs:
            expected_msgs = Counter()
        with self._open_expected_file() as f:
            expected_output_lines = [
                OutputLine.from_csv(row) for row in csv.reader(f, "test")
            ]
        return expected_msgs, expected_output_lines

    def _get_actual(self):
        messages = self._linter.reporter.messages
        messages.sort(key=lambda m: (m.line, m.symbol, m.msg))
        received_msgs = Counter()
        received_output_lines = []
        for msg in messages:
            assert (
                msg.symbol != "fatal"
            ), f"Pylint analysis failed because of '{msg.msg}'"
            received_msgs[msg.line, msg.symbol] += 1
            received_output_lines.append(OutputLine.from_msg(msg))
        return received_msgs, received_output_lines

    def _runTest(self):
        __tracebackhide__ = True  # pylint: disable=unused-variable
        modules_to_check = [self._test_file.source]
        self._linter.check(modules_to_check)
        expected_messages, expected_output = self._get_expected()
        actual_messages, actual_output = self._get_actual()
        assert (
            expected_messages == actual_messages
        ), self.error_msg_for_unequal_messages(
            actual_messages, expected_messages, actual_output
        )
        self._check_output_text(expected_messages, expected_output, actual_output)

    def error_msg_for_unequal_messages(
        self, actual_messages, expected_messages, actual_output: List[OutputLine]
    ):
        msg = [f'Wrong results for file "{self._test_file.base}":']
        missing, unexpected = self.multiset_difference(
            expected_messages, actual_messages
        )
        if missing:
            msg.append("\nExpected in testdata:")
            msg.extend(
                " %3d: %s" % msg  # pylint: disable=consider-using-f-string
                for msg in sorted(missing)
            )
        if unexpected:
            msg.append("\nUnexpected in testdata:")
            msg.extend(" %3d: %s" % msg for msg in sorted(unexpected))  # type: ignore #pylint: disable=consider-using-f-string
        error_msg = "\n".join(msg)
        if self._config and self._config.getoption("verbose") > 0:
            error_msg += "\n\nActual pylint output for this file:\n"
            error_msg += "\n".join(str(o) for o in actual_output)
        return error_msg

    def error_msg_for_unequal_output(self, expected_lines, received_lines) -> str:
        missing = set(expected_lines) - set(received_lines)
        unexpected = set(received_lines) - set(expected_lines)
        error_msg = (
            f"Wrong output for '{self._test_file.base}.txt':\n"
            "You can update the expected output automatically with: '"
            f"python tests/test_functional.py {UPDATE_OPTION} -k "
            f'"test_functional[{self._test_file.base}]"\'\n\n'
        )
        sort_by_line_number = operator.attrgetter("lineno")
        if missing:
            error_msg += "\n- Missing lines:\n"
            for line in sorted(missing, key=sort_by_line_number):
                error_msg += f"{line}\n"
        if unexpected:
            error_msg += "\n- Unexpected lines:\n"
            for line in sorted(unexpected, key=sort_by_line_number):
                error_msg += f"{line}\n"
        return error_msg

    def _check_output_text(self, _, expected_output, actual_output):
        """This is a function because we want to be able to update the text in LintModuleOutputUpdate"""
        assert expected_output == actual_output, self.error_msg_for_unequal_output(
            expected_output, actual_output
        )
