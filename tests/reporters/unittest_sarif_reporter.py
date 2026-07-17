# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Test for the SARIF reporter."""

from __future__ import annotations

import json
from io import StringIO
from typing import Any

from pylint import checkers
from pylint.__pkginfo__ import __version__
from pylint.interfaces import HIGH
from pylint.lint import PyLinter
from pylint.reporters.sarif_reporter import SARIFReporter


def get_linter_result(message: dict[str, Any]) -> dict[str, Any]:
    output = StringIO()
    reporter = SARIFReporter(output)
    linter = PyLinter(reporter=reporter)
    checkers.initialize(linter)
    linter.config.persistent = 0
    linter.open()
    linter.set_current_module("0123")
    linter.add_message(
        message["msg"],
        line=message["line"],
        args=message["args"],
        end_lineno=message["end_line"],
        end_col_offset=message["end_column"],
        confidence=HIGH,
    )
    reporter.display_messages(None)
    return json.loads(output.getvalue())  # type: ignore[no-any-return]


def test_simple_sarif_output() -> None:
    """Test SARIF reporter basic structure and message mapping."""
    message = {
        "msg": "line-too-long",
        "line": 1,
        "args": (1, 2),
        "end_line": 1,
        "end_column": 4,
    }
    report = get_linter_result(message)

    assert report["version"] == "2.1.0"
    assert report["$schema"] == "https://json.schemastore.org/sarif-2.1.0.json"
    assert len(report["runs"]) == 1

    run = report["runs"][0]
    driver = run["tool"]["driver"]
    assert driver["name"] == "pylint"
    assert driver["version"] == __version__
    assert driver["informationUri"] == "https://github.com/pylint-dev/pylint"

    assert len(driver["rules"]) == 1
    rule = driver["rules"][0]
    assert rule["id"] == "C0301"
    assert rule["name"] == "line-too-long"
    assert rule["shortDescription"]["text"] == "line-too-long"
    assert rule["properties"]["category"] == "convention"
    assert rule["helpUri"].endswith("/convention/line-too-long.html")

    assert len(run["results"]) == 1
    result = run["results"][0]
    assert result["ruleId"] == "C0301"
    assert result["level"] == "note"
    assert result["message"]["text"] == "Line too long (1/2)"
    assert result["properties"]["symbol"] == "line-too-long"
    assert result["properties"]["confidence"] == "HIGH"

    location = result["locations"][0]["physicalLocation"]
    assert location["artifactLocation"]["uri"] == "0123"
    assert location["region"] == {
        "startLine": 1,
        "startColumn": 1,  # pylint column 0 -> SARIF 1
        "endLine": 1,
        "endColumn": 5,  # pylint end_column 4 -> SARIF 5
    }


def test_sarif_error_level_for_error_category() -> None:
    """Errors map to SARIF level 'error'."""
    output = StringIO()
    reporter = SARIFReporter(output)
    linter = PyLinter(reporter=reporter)
    checkers.initialize(linter)
    linter.config.persistent = 0
    linter.open()
    linter.set_current_module("mod")
    linter.add_message("return-outside-function", line=2, confidence=HIGH)
    reporter.display_messages(None)
    report = json.loads(output.getvalue())
    result = report["runs"][0]["results"][0]
    assert result["ruleId"].startswith("E")
    assert result["level"] == "error"
    assert result["locations"][0]["physicalLocation"]["region"] == {
        "startLine": 2,
        "startColumn": 1,
    }


def test_sarif_empty_messages() -> None:
    """Empty run still produces valid SARIF."""
    output = StringIO()
    reporter = SARIFReporter(output)
    linter = PyLinter(reporter=reporter)
    checkers.initialize(linter)
    linter.config.persistent = 0
    reporter.display_messages(None)
    report = json.loads(output.getvalue())
    assert report["runs"][0]["results"] == []
    assert report["runs"][0]["tool"]["driver"]["rules"] == []
