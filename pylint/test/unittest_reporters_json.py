# Copyright (c) 2014 Vlad Temian <vladtemian@gmail.com>
# Copyright (c) 2015-2016 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2017 guillaume2 <guillaume.peillex@gmail.col>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Test for the JSON reporter."""

import json

import six

import pylint.config
from pylint.lint import PluginRegistry, PyLinter
from pylint import checkers
from pylint.reporters.json import JSONReporter


def test_simple_json_output():
    output = six.StringIO()

    reporter = JSONReporter()
    global_config = pylint.config.Configuration()
    linter = PyLinter(global_config)
    registry = PluginRegistry(linter, register_options=global_config.add_options)
    checkers.initialize(registry)
    linter.set_reporter(reporter)

    linter.config.persistent = 0
    linter.reporter.set_output(output)
    linter.open()
    linter.set_current_module('0123')
    linter.add_message('line-too-long', line=1, args=(1, 2))

    # we call this method because we didn't actually run the checkers
    reporter.display_messages(None)

    expected_result = [[
        ("column", 0),
        ("line", 1),
        ("message", "Line too long (1/2)"),
        ("message-id", "C0301"),
        ("module", "0123"),
        ("obj", ""),
        ("path", "0123"),
        ("symbol", "line-too-long"),
        ("type", "convention"),
    ]]
    report_result = json.loads(output.getvalue())
    report_result = [sorted(report_result[0].items(),
                            key=lambda item: item[0])]
    assert report_result == expected_result
