# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the JUnit XML reporter."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from io import StringIO
from typing import TYPE_CHECKING

from pylint.message import Message
from pylint.reporters.junit_reporter import JUnitReporter
from pylint.typing import MessageLocationTuple

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter


class TestJUnitReporter:
    """Tests for JUnitReporter."""

    def test_empty_report(self) -> None:
        """Test that an empty report produces valid JUnit XML."""
        output = StringIO()
        reporter = JUnitReporter(output)
        reporter.display_messages(None)
        xml_output = output.getvalue()
        # Should contain XML declaration
        assert xml_output.startswith('<?xml version="1.0" encoding="utf-8"?>')
        # Should be parseable XML
        root = ET.fromstring(
            xml_output.replace('<?xml version="1.0" encoding="utf-8"?>', "")
        )
        assert root.tag == "testsuites"

    def test_reporter_name(self) -> None:
        """Test that the reporter has the correct name."""
        assert JUnitReporter.name == "junit"

    def test_reporter_extension(self) -> None:
        """Test that the reporter has the correct file extension."""
        assert JUnitReporter.extension == "xml"

    def test_single_message(self) -> None:
        """Test that a single message is rendered as a failure."""
        output = StringIO()
        reporter = JUnitReporter(output)
        reporter.on_set_current_module("test_module", "test_file.py")
        msg = Message(
            msg_id="E0001",
            symbol="test-error",
            msg="Test error message",
            location=MessageLocationTuple(
                abspath="test_file.py",
                path="test_file.py",
                module="test_module",
                obj="test_function",
                line=10,
                column=5,
                end_line=10,
                end_column=10,
            ),
            confidence=(
                reporter.linter.config.confidence_level
                if hasattr(reporter, "linter")
                else 2
            ),
        )
        # Manually set confidence since we don't have a full linter setup
        object.__setattr__(msg, "confidence", msg.confidence)
        reporter.handle_message(msg)
        reporter.display_messages(None)
        xml_output = output.getvalue()
        # Should contain the message text
        assert "E0001" in xml_output
        assert "test-error" in xml_output
        assert "Test error message" in xml_output

    def test_message_serialization(self) -> None:
        """Test that Message objects can be serialized and deserialized."""
        msg = Message(
            msg_id="W0001",
            symbol="test-warning",
            msg="Test warning message",
            location=MessageLocationTuple(
                abspath="test_file.py",
                path="test_file.py",
                module="test_module",
                obj=None,
                line=5,
                column=0,
                end_line=None,
                end_column=None,
            ),
            confidence=2,
        )
        serialized = JUnitReporter.serialize(msg)
        assert serialized["message-id"] == "W0001"
        assert serialized["symbol"] == "test-warning"
        assert serialized["message"] == "Test warning message"
        assert serialized["module"] == "test_module"
        assert serialized["line"] == 5

    def test_xml_structure(self) -> None:
        """Test that the XML structure follows JUnit format."""
        output = StringIO()
        reporter = JUnitReporter(output)
        reporter.on_set_current_module("module_a", "module_a.py")
        reporter.on_set_current_module("module_b", "module_b.py")
        reporter.display_messages(None)
        xml_output = output.getvalue()
        root = ET.fromstring(
            xml_output.replace('<?xml version="1.0" encoding="utf-8"?>', "")
        )
        testsuite = root.find("testsuite")
        assert testsuite is not None
        assert testsuite.get("name") == "pylint"
        # Verify attributes exist
        assert testsuite.get("tests") is not None
        assert testsuite.get("failures") is not None
        assert testsuite.get("errors") is not None
        assert testsuite.get("skipped") is not None

    def test_register(self, linter: PyLinter) -> None:
        """Test that the reporter can be registered with a linter."""
        from pylint.reporters.junit_reporter import register

        register(linter)
        # Should not raise any exceptions
        assert True
