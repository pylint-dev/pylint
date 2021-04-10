# Copyright (c) 2014 Vlad Temian <vladtemian@gmail.com>
# Copyright (c) 2015-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2017 guillaume2 <guillaume.peillex@gmail.col>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Test for the JSON reporter."""

import json
from io import StringIO

from pylint import checkers
from pylint.lint import PyLinter
from pylint.reporters import JSONReporter
from pylint.reporters.ureports.nodes import EvaluationSection

expected_score_message = "Expected score message"
expected_result = [
    [
        ("column", 0),
        ("line", 1),
        ("message", "Line too long (1/2)"),
        ("message-id", "C0301"),
        ("module", "0123"),
        ("obj", ""),
        ("path", "0123"),
        ("symbol", "line-too-long"),
        ("type", "convention"),
    ]
]


def test_simple_json_output_no_score():
    report = get_linter_result(score=False)
    assert len(report) == 1
    report_result = [sorted(report[0].items(), key=lambda item: item[0])]
    assert report_result == expected_result


def get_linter_result(score):
    output = StringIO()
    reporter = JSONReporter(output)
    linter = PyLinter(reporter=reporter)
    checkers.initialize(linter)
    linter.config.persistent = 0
    linter.config.score = score
    linter.open()
    linter.set_current_module("0123")
    linter.add_message("line-too-long", line=1, args=(1, 2))
    # we call those methods because we didn't actually run the checkers
    if score:
        reporter.display_reports(EvaluationSection(expected_score_message))
    reporter.display_messages(None)
    report_result = json.loads(output.getvalue())
    return report_result
