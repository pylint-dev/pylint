# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the JUnit XML reporter."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from io import StringIO
from pathlib import Path

import pytest

from pylint import checkers, reporters
from pylint.interfaces import HIGH, UNDEFINED
from pylint.lint import PyLinter
from pylint.message import Message
from pylint.reporters.junit_reporter import JUnitReporter
from pylint.reporters.ureports.nodes import Section
from pylint.typing import MessageLocationTuple

JUnitLinter = tuple[StringIO, JUnitReporter, PyLinter]


@pytest.fixture
def junit_linter() -> JUnitLinter:
    output = StringIO()
    reporter = JUnitReporter(output)
    linter = PyLinter(reporter=reporter)
    checkers.initialize(linter)
    linter.config.persistent = 0
    linter.open()
    return output, reporter, linter


def _message(
    *,
    msg_id: str = "C0301",
    symbol: str = "line-too-long",
    msg: str = "Line too long (100/80)",
    abspath: str = "/path/to/file.py",
    path: str = "file.py",
    module: str = "test_module",
    line: int = 1,
    column: int = 0,
) -> Message:
    return Message(
        msg_id=msg_id,
        symbol=symbol,
        location=MessageLocationTuple(
            abspath=abspath,
            path=path,
            module=module,
            obj="",
            line=line,
            column=column,
            end_line=None,
            end_column=None,
        ),
        msg=msg,
        confidence=HIGH,
    )


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
        linter = PyLinter()
        checkers.initialize(linter)
        reporters.initialize(linter)
        assert "junit" in linter._reporters


class TestJUnitReporterOutput:
    """Test the XML structure produced by JUnitReporter."""

    def test_clean_modules_emit_success_testcases(
        self, junit_linter: JUnitLinter
    ) -> None:
        output, reporter, linter = junit_linter
        linter.set_current_module("package.clean_a", "package/clean_a.py")
        linter.set_current_module("package.clean_b", "package/clean_b.py")

        reporter.display_messages(None)

        assert output.getvalue() == (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            '<testsuites tests="2" errors="0" failures="0">\n'
            '  <testsuite name="package.clean_a" tests="1" errors="0" failures="0">\n'
            '    <testcase name="package.clean_a:0:0" classname="pylint" '
            'file="package/clean_a.py" line="0">\n'
            "      <system-out>All checks passed for: package/clean_a.py</system-out>\n"
            "    </testcase>\n"
            "  </testsuite>\n"
            '  <testsuite name="package.clean_b" tests="1" errors="0" failures="0">\n'
            '    <testcase name="package.clean_b:0:0" classname="pylint" '
            'file="package/clean_b.py" line="0">\n'
            "      <system-out>All checks passed for: package/clean_b.py</system-out>\n"
            "    </testcase>\n"
            "  </testsuite>\n"
            "</testsuites>\n"
        )

    def test_message_output_matches_golden_master(
        self, junit_linter: JUnitLinter, tmp_path: Path
    ) -> None:
        output, reporter, linter = junit_linter
        source = tmp_path / "bad.py"
        source.write_text("x = 1\nprint('hello')\n", encoding="utf-8")
        linter.set_current_module("package.bad", "bad.py")
        reporter.handle_message(
            _message(
                abspath=str(source),
                path="bad.py",
                module="package.bad",
                line=2,
                column=4,
            )
        )

        reporter.display_messages(None)

        assert output.getvalue() == (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            '<testsuites tests="1" errors="0" failures="1">\n'
            '  <testsuite name="package.bad" tests="1" errors="0" failures="1">\n'
            '    <testcase name="package.bad:2:4" classname="pylint" file="bad.py" '
            'line="2" category="convention">\n'
            '      <failure type="convention" message="line-too-long">C0301:Line too long '
            "(100/80)\n"
            "bad.py:2:4:print('hello')</failure>\n"
            "      <system-out>bad.py:2:4:print('hello')</system-out>\n"
            '      <system-err>C0301:Line too long (100/80)\n'
            "bad.py:2:4:print('hello')</system-err>\n"
            "    </testcase>\n"
            "  </testsuite>\n"
            "</testsuites>\n"
        )

    def test_multiple_messages_in_same_module_are_separate_testcases(
        self, junit_linter: JUnitLinter
    ) -> None:
        output, reporter, linter = junit_linter
        linter.set_current_module("test_module")
        reporter.handle_message(_message(line=1, column=0))
        reporter.handle_message(_message(line=5, column=8))

        reporter.display_messages(None)

        root = ET.fromstring(output.getvalue())
        testsuite = root.find("testsuite")
        assert testsuite is not None
        assert testsuite.get("tests") == "2"
        assert testsuite.get("errors") == "0"
        assert testsuite.get("failures") == "2"
        testcases = testsuite.findall("testcase")
        assert [testcase.get("name") for testcase in testcases] == [
            "test_module:1:0",
            "test_module:5:8",
        ]
        assert all(testcase.find("failure") is not None for testcase in testcases)

    def test_messages_from_different_modules_produce_separate_testsuites(
        self, junit_linter: JUnitLinter
    ) -> None:
        output, reporter, linter = junit_linter
        linter.set_current_module("module_a")
        reporter.handle_message(_message(module="module_a"))
        linter.set_current_module("module_b")
        reporter.handle_message(_message(module="module_b", line=3))

        reporter.display_messages(None)

        root = ET.fromstring(output.getvalue())
        assert root.get("tests") == "2"
        assert root.get("errors") == "0"
        assert root.get("failures") == "2"
        testsuites = root.findall("testsuite")
        assert [testsuite.get("name") for testsuite in testsuites] == [
            "module_a",
            "module_b",
        ]
        assert [testsuite.get("tests") for testsuite in testsuites] == ["1", "1"]

    def test_empty_module_falls_back_to_path(self, junit_linter: JUnitLinter) -> None:
        output, reporter, _linter = junit_linter
        reporter.handle_message(_message(module="", path="standalone.py", line=7, column=2))

        reporter.display_messages(None)

        root = ET.fromstring(output.getvalue())
        testsuite = root.find("testsuite")
        assert testsuite is not None
        assert testsuite.get("name") == "standalone.py"
        testcase = testsuite.find("testcase")
        assert testcase is not None
        assert testcase.get("name") == "standalone.py:7:2"
        assert testcase.get("file") == "standalone.py"

    def test_error_category_still_produces_failure_element(
        self, junit_linter: JUnitLinter
    ) -> None:
        output, reporter, linter = junit_linter
        linter.set_current_module("test_module")
        reporter.handle_message(
            _message(
                msg_id="E0001",
                symbol="syntax-error",
                msg="Syntax error in file",
            )
        )

        reporter.display_messages(None)

        root = ET.fromstring(output.getvalue())
        assert root.get("errors") == "0"
        assert root.get("failures") == "1"
        assert root.find(".//error") is None
        failure = root.find(".//failure")
        assert failure is not None
        assert failure.get("type") == "error"
        assert failure.get("message") == "syntax-error"

    def test_output_is_valid_xml(self, junit_linter: JUnitLinter) -> None:
        output, reporter, linter = junit_linter
        linter.set_current_module("test_module")
        reporter.handle_message(_message())
        reporter.display_messages(None)

        root = ET.fromstring(output.getvalue())
        assert root.tag == "testsuites"

    def test_xml_declaration_present(self, junit_linter: JUnitLinter) -> None:
        output, reporter, _linter = junit_linter
        reporter.display_messages(None)

        assert output.getvalue().startswith("<?xml")

    def test_special_xml_characters_escaped(self, junit_linter: JUnitLinter) -> None:
        output, reporter, linter = junit_linter
        linter.set_current_module("test_module")

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

        failure = ET.fromstring(output.getvalue()).find(".//failure")
        assert failure is not None
        assert "<special>" in (failure.text or "")
        assert '"characters"' in (failure.text or "")

    def test_display_reports_is_noop(self, junit_linter: JUnitLinter) -> None:
        output, reporter, _linter = junit_linter
        section = Section()

        reporter._display(section)

        assert output.getvalue() == ""
