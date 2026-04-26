# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the JUnit XML reporter."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from io import StringIO
from typing import Any

import pytest

from pylint import checkers
from pylint.interfaces import HIGH, UNDEFINED
from pylint.lint import PyLinter
from pylint.message import Message
from pylint.reporters.junit_reporter import JUnitReporter
from pylint.typing import MessageLocationTuple


def _get_junit_output(
    messages: list[dict[str, Any]],
    module_name: str = "test_module",
) -> ET.Element:
    """Helper: create a linter with JUnitReporter, add messages, return parsed XML root."""
    output = StringIO()
    reporter = JUnitReporter(output)
    linter = PyLinter(reporter=reporter)
    checkers.initialize(linter)
    linter.config.persistent = 0
    linter.open()
    linter.set_current_module(module_name)
    for msg in messages:
        linter.add_message(
            msg["msg"],
            line=msg["line"],
            args=msg.get("args", ()),
            end_lineno=msg.get("end_line"),
            end_col_offset=msg.get("end_column"),
        )
    reporter.display_messages(None)
    xml_output = output.getvalue()
    return ET.fromstring(xml_output)


class TestJUnitReporterRegistration:
    """Test that the JUnit reporter is registered and discoverable."""

    def test_reporter_name(self) -> None:
        """The reporter must have name 'junit' for --output-format=junit."""
        assert JUnitReporter.name == "junit"

    def test_reporter_extension(self) -> None:
        """The reporter file extension must be 'xml'."""
        assert JUnitReporter.extension == "xml"

    def test_reporter_is_registered(self) -> None:
        """The reporter must be discoverable via linter._reporters."""
        from pylint import reporters

        linter = PyLinter()
        checkers.initialize(linter)
        reporters.initialize(linter)
        assert "junit" in linter._reporters


class TestJUnitReporterOutput:
    """Test the XML structure produced by JUnitReporter."""

    def test_single_message_output(self) -> None:
        """A single message should produce valid JUnit XML with one testcase
        and one failure element."""
        root = _get_junit_output(
            [{"msg": "line-too-long", "line": 1, "args": (100, 80)}]
        )
        assert root.tag == "testsuites"
        testsuite = root.find("testsuite")
        assert testsuite is not None
        assert testsuite.get("name") == "pylint"
        assert testsuite.get("tests") == "1"
        assert testsuite.get("failures") == "1"

        testcases = testsuite.findall("testcase")
        assert len(testcases) == 1
        assert testcases[0].get("name") == "test_module"
        assert testcases[0].get("classname") == "test_module"

        failures = testcases[0].findall("failure")
        assert len(failures) == 1
        assert failures[0].get("type") == "convention"
        assert "C0301" in failures[0].get("message", "")
        assert "line-too-long" in failures[0].get("message", "")

    def test_multiple_messages_same_module(self) -> None:
        """Multiple messages in the same module should be grouped under one
        testcase with multiple failure elements."""
        root = _get_junit_output(
            [
                {"msg": "line-too-long", "line": 1, "args": (100, 80)},
                {"msg": "line-too-long", "line": 5, "args": (120, 80)},
            ]
        )
        testsuite = root.find("testsuite")
        assert testsuite is not None
        assert testsuite.get("tests") == "1"
        assert testsuite.get("failures") == "2"

        testcases = testsuite.findall("testcase")
        assert len(testcases) == 1
        failures = testcases[0].findall("failure")
        assert len(failures) == 2

    def test_multiple_modules(self) -> None:
        """Messages from different modules should produce separate testcases."""
        output = StringIO()
        reporter = JUnitReporter(output)
        linter = PyLinter(reporter=reporter)
        checkers.initialize(linter)
        linter.config.persistent = 0
        linter.open()

        # First module
        linter.set_current_module("module_a")
        linter.add_message("line-too-long", line=1, args=(100, 80))

        # Second module
        linter.set_current_module("module_b")
        linter.add_message("line-too-long", line=3, args=(110, 80))

        reporter.display_messages(None)
        root = ET.fromstring(output.getvalue())

        testsuite = root.find("testsuite")
        assert testsuite is not None
        assert testsuite.get("tests") == "2"
        assert testsuite.get("failures") == "2"

        testcases = testsuite.findall("testcase")
        assert len(testcases) == 2
        tc_names = {tc.get("name") for tc in testcases}
        assert tc_names == {"module_a", "module_b"}

    def test_no_messages(self) -> None:
        """When there are no messages, testsuite should have zero tests."""
        output = StringIO()
        reporter = JUnitReporter(output)
        linter = PyLinter(reporter=reporter)
        checkers.initialize(linter)
        linter.config.persistent = 0
        linter.open()
        reporter.display_messages(None)

        root = ET.fromstring(output.getvalue())
        testsuite = root.find("testsuite")
        assert testsuite is not None
        assert testsuite.get("tests") == "0"
        assert testsuite.get("failures") == "0"
        assert len(testsuite.findall("testcase")) == 0

    def test_output_is_valid_xml(self) -> None:
        """The output must be parseable XML — any malformed output will raise."""
        root = _get_junit_output(
            [{"msg": "line-too-long", "line": 1, "args": (100, 80)}]
        )
        # If we got here, the XML parsed successfully
        assert root.tag == "testsuites"

    def test_xml_declaration_present(self) -> None:
        """The output should start with an XML declaration."""
        output = StringIO()
        reporter = JUnitReporter(output)
        linter = PyLinter(reporter=reporter)
        checkers.initialize(linter)
        linter.config.persistent = 0
        linter.open()
        reporter.display_messages(None)

        xml_str = output.getvalue()
        assert xml_str.startswith("<?xml")

    def test_failure_text_contains_file_info(self) -> None:
        """The failure element text should contain file path and message details."""
        root = _get_junit_output(
            [{"msg": "line-too-long", "line": 10, "args": (100, 80)}]
        )
        failure = root.find(".//failure")
        assert failure is not None
        assert failure.text is not None
        assert "line-too-long" in failure.text
        assert "C0301" in failure.text

    def test_special_xml_characters_escaped(self) -> None:
        """Messages with XML-special characters must be properly escaped."""
        output = StringIO()
        reporter = JUnitReporter(output)
        linter = PyLinter(reporter=reporter)
        checkers.initialize(linter)
        linter.config.persistent = 0
        linter.open()
        linter.set_current_module("test_module")

        # Create a message directly with special characters
        msg = Message(
            msg_id="C0301",
            symbol="line-too-long",
            location=MessageLocationTuple(
                abspath="/path/to/file.py",
                path="file.py",
                module="test_module",
                obj="",
                line=1,
                column=0,
                end_line=None,
                end_column=None,
            ),
            msg='Line has <special> & "characters"',
            confidence=UNDEFINED,
        )
        reporter.handle_message(msg)
        reporter.display_messages(None)

        # Must not raise — valid XML even with special chars
        xml_str = output.getvalue()
        root = ET.fromstring(xml_str)
        failure = root.find(".//failure")
        assert failure is not None
        assert "<special>" in (failure.text or "")
        assert '"characters"' in (failure.text or "")

    def test_failure_message_attribute_format(self) -> None:
        """The failure message attribute should follow the format:
        '{msg_id}({symbol}): {message} (line {line})'."""
        root = _get_junit_output(
            [{"msg": "line-too-long", "line": 42, "args": (100, 80)}]
        )
        failure = root.find(".//failure")
        assert failure is not None
        msg_attr = failure.get("message", "")
        assert msg_attr.startswith("C0301(line-too-long):")
        assert "(line 42)" in msg_attr

    def test_display_reports_is_noop(self) -> None:
        """display_reports should not produce any output."""
        output = StringIO()
        reporter = JUnitReporter(output)
        linter = PyLinter(reporter=reporter)
        checkers.initialize(linter)
        # _display and display_reports are no-ops — should not raise
        from pylint.reporters.ureports.nodes import Section

        section = Section()
        reporter._display(section)
        assert output.getvalue() == ""


class TestJUnitReporterWithErrorTypes:
    """Test that different pylint message categories map correctly."""

    def test_error_category(self) -> None:
        """Error messages should have type='error' in the failure element."""
        output = StringIO()
        reporter = JUnitReporter(output)
        linter = PyLinter(reporter=reporter)
        checkers.initialize(linter)
        linter.config.persistent = 0
        linter.open()
        linter.set_current_module("test_module")

        msg = Message(
            msg_id="E0001",
            symbol="syntax-error",
            location=MessageLocationTuple(
                abspath="/path/to/file.py",
                path="file.py",
                module="test_module",
                obj="",
                line=1,
                column=0,
                end_line=None,
                end_column=None,
            ),
            msg="Syntax error in file",
            confidence=HIGH,
        )
        reporter.handle_message(msg)
        reporter.display_messages(None)

        root = ET.fromstring(output.getvalue())
        failure = root.find(".//failure")
        assert failure is not None
        assert failure.get("type") == "error"

    def test_warning_category(self) -> None:
        """Warning messages should have type='warning' in the failure element."""
        output = StringIO()
        reporter = JUnitReporter(output)
        linter = PyLinter(reporter=reporter)
        checkers.initialize(linter)
        linter.config.persistent = 0
        linter.open()
        linter.set_current_module("test_module")

        msg = Message(
            msg_id="W0611",
            symbol="unused-import",
            location=MessageLocationTuple(
                abspath="/path/to/file.py",
                path="file.py",
                module="test_module",
                obj="",
                line=1,
                column=0,
                end_line=None,
                end_column=None,
            ),
            msg="Unused import os",
            confidence=HIGH,
        )
        reporter.handle_message(msg)
        reporter.display_messages(None)

        root = ET.fromstring(output.getvalue())
        failure = root.find(".//failure")
        assert failure is not None
        assert failure.get("type") == "warning"
