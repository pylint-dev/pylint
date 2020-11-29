# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import collections
import csv
import itertools
import platform
import sys
from io import StringIO
from typing import Tuple

import pytest

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


class LintModuleTest:
    maxDiff = None

    def __init__(self, test_file: FunctionalTestFile):
        _test_reporter = FunctionalTestReporter()
        self._linter = PyLinter()
        self._linter.set_reporter(_test_reporter)
        self._linter.config.persistent = 0
        checkers.initialize(self._linter)
        self._linter.disable("I")
        try:
            self._linter.read_config_file(test_file.option_file)
            self._linter.load_config_file()
        except NoFileError:
            pass
        self._test_file = test_file

    def setUp(self):
        if self._should_be_skipped_due_to_version():
            pytest.skip(
                "Test cannot run with Python %s." % (sys.version.split(" ")[0],)
            )
        missing = []
        for req in self._test_file.options["requires"]:
            try:
                __import__(req)
            except ImportError:
                missing.append(req)
        if missing:
            pytest.skip("Requires %s to be present." % (",".join(missing),))
        if self._test_file.options["except_implementations"]:
            implementations = [
                item.strip()
                for item in self._test_file.options["except_implementations"].split(",")
            ]
            implementation = platform.python_implementation()
            if implementation in implementations:
                pytest.skip(
                    "Test cannot run with Python implementation %r" % (implementation,)
                )
        if self._test_file.options["exclude_platforms"]:
            platforms = [
                item.strip()
                for item in self._test_file.options["exclude_platforms"].split(",")
            ]
            if sys.platform.lower() in platforms:
                pytest.skip("Test cannot run on platform %r" % (sys.platform,))

    def _should_be_skipped_due_to_version(self):
        return (
            sys.version_info < self._test_file.options["min_pyver"]
            or sys.version_info > self._test_file.options["max_pyver"]
        )

    def __str__(self):
        return "%s (%s.%s)" % (
            self._test_file.base,
            self.__class__.__module__,
            self.__class__.__name__,
        )

    @staticmethod
    def get_expected_messages(stream):
        """Parses a file and get expected messages.

        :param stream: File-like input stream.
        :type stream: enumerable
        :returns: A dict mapping line,msg-symbol tuples to the count on this line.
        :rtype: dict
        """
        messages = collections.Counter()
        for i, line in enumerate(stream):
            match = _EXPECTED_RE.search(line)
            if match is None:
                continue
            line = match.group("line")
            if line is None:
                line = i + 1
            elif line.startswith("+") or line.startswith("-"):
                line = i + 1 + int(line)
            else:
                line = int(line)

            version = match.group("version")
            op = match.group("op")
            if version:
                required = parse_python_version(version)
                if not _OPERATORS[op](sys.version_info, required):
                    continue

            for msg_id in match.group("msgs").split(","):
                messages[line, msg_id.strip()] += 1
        return messages

    @staticmethod
    def multiset_difference(expected_entries: set, actual_entries: set) -> Tuple[set]:
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

    def _open_expected_file(self):
        try:
            return open(self._test_file.expected_output)
        except FileNotFoundError:
            return StringIO("")

    def _open_source_file(self):
        if self._test_file.base == "invalid_encoded_data":
            return open(self._test_file.source)
        if "latin1" in self._test_file.base:
            return open(self._test_file.source, encoding="latin1")
        return open(self._test_file.source, encoding="utf8")

    def _get_expected(self):
        with self._open_source_file() as fobj:
            expected_msgs = self.get_expected_messages(fobj)

        if expected_msgs:
            with self._open_expected_file() as fobj:
                expected_output_lines = [
                    OutputLine.from_csv(row) for row in csv.reader(fobj, "test")
                ]
        else:
            expected_output_lines = []
        return expected_msgs, expected_output_lines

    def _get_actual(self):
        messages = self._linter.reporter.messages
        messages.sort(key=lambda m: (m.line, m.symbol, m.msg))
        received_msgs = collections.Counter()
        received_output_lines = []
        for msg in messages:
            assert (
                msg.symbol != "fatal"
            ), "Pylint analysis failed because of '{}'".format(msg.msg)
            received_msgs[msg.line, msg.symbol] += 1
            received_output_lines.append(OutputLine.from_msg(msg))
        return received_msgs, received_output_lines

    def _runTest(self):
        modules_to_check = [self._test_file.source]
        self._linter.check(modules_to_check)
        expected_messages, expected_output = self._get_expected()
        actual_messages, actual_output = self._get_actual()

        if expected_messages != actual_messages:
            msg = ['Wrong results for file "%s":' % (self._test_file.base)]
            missing, unexpected = self.multiset_difference(
                expected_messages, actual_messages
            )
            if missing:
                msg.append("\nExpected in testdata:")
                msg.extend(" %3d: %s" % msg for msg in sorted(missing))
            if unexpected:
                msg.append("\nUnexpected in testdata:")
                msg.extend(" %3d: %s" % msg for msg in sorted(unexpected))
            pytest.fail("\n".join(msg))
        self._check_output_text(expected_messages, expected_output, actual_output)

    @classmethod
    def _split_lines(cls, expected_messages, lines):
        emitted, omitted = [], []
        for msg in lines:
            if (msg[1], msg[0]) in expected_messages:
                emitted.append(msg)
            else:
                omitted.append(msg)
        return emitted, omitted

    def _check_output_text(self, expected_messages, expected_lines, received_lines):
        expected_lines = self._split_lines(expected_messages, expected_lines)[0]
        for exp, rec in itertools.zip_longest(expected_lines, received_lines):
            assert exp == rec, (
                "Wrong output for '{_file}.txt':\n"
                "You can update the expected output automatically with: '"
                'python tests/test_functional.py {update_option} -k "test_functional[{_file}]"\'\n\n'
                "Expected : {expected}\n"
                "Received : {received}".format(
                    update_option=UPDATE_OPTION,
                    expected=exp,
                    received=rec,
                    _file=self._test_file.base,
                )
            )
