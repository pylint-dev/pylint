# Copyright (c) 2014 Vlad Temian <vladtemian@gmail.com>
# Copyright (c) 2015-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2017 guillaume2 <guillaume.peillex@gmail.col>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Test for the JSON reporter."""

import json
from io import StringIO
from typing import Any, Dict, List

from pylint import checkers
from pylint.lint import PyLinter
from pylint.reporters import JSONReporter
from pylint.reporters.ureports.nodes import EvaluationSection

expected_score_message = "Expected score message"


def test_simple_json_output_no_score() -> None:
    """Test JSON reporter with no score"""
    message = {
        "msg": "line-too-long",
        "line": 1,
        "args": (1, 2),
        "end_line": None,
        "end_column": None,
    }
    expected = [
        {
            "type": "convention",
            "module": "0123",
            "obj": "",
            "line": 1,
            "column": 0,
            "endLine": None,
            "endColumn": None,
            "path": "0123",
            "symbol": "line-too-long",
            "message": "Line too long (1/2)",
            "message-id": "C0301",
        }
    ]
    report = get_linter_result(score=False, message=message)
    assert len(report) == 1
    assert json.dumps(report) == json.dumps(expected)


def test_simple_json_output_no_score_with_end_line() -> None:
    """Test JSON reporter with no score with end_line and end_column"""
    message = {
        "msg": "line-too-long",
        "line": 1,
        "args": (1, 2),
        "end_line": 1,
        "end_column": 4,
    }
    expected = [
        {
            "type": "convention",
            "module": "0123",
            "obj": "",
            "line": 1,
            "column": 0,
            "endLine": 1,
            "endColumn": 4,
            "path": "0123",
            "symbol": "line-too-long",
            "message": "Line too long (1/2)",
            "message-id": "C0301",
        }
    ]
    report = get_linter_result(score=False, message=message)
    assert len(report) == 1
    assert json.dumps(report) == json.dumps(expected)


def get_linter_result(score: bool, message: Dict[str, Any]) -> List[Dict[str, Any]]:
    output = StringIO()
    reporter = JSONReporter(output)
    linter = PyLinter(reporter=reporter)
    checkers.initialize(linter)
    linter.config.persistent = 0
    linter.config.score = score
    linter.open()
    linter.set_current_module("0123")
    linter.add_message(
        message["msg"],
        line=message["line"],
        args=message["args"],
        end_lineno=message["end_line"],
        end_col_offset=message["end_column"],
    )
    # we call those methods because we didn't actually run the checkers
    if score:
        reporter.display_reports(EvaluationSection(expected_score_message))
    reporter.display_messages(None)
    report_result = json.loads(output.getvalue())
    return report_result
