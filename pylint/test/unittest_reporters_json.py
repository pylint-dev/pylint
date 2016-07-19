# Copyright (c) 2003-2016 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Test for the JSON reporter."""

import json
import unittest

import six

from pylint.lint import PyLinter
from pylint import checkers
from pylint.reporters.json import JSONReporter


class TestJSONReporter(unittest.TestCase):

    def test_simple_json_output(self):
        output = six.StringIO()

        reporter = JSONReporter()
        linter = PyLinter(reporter=reporter)
        checkers.initialize(linter)

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
            ("module", "0123"),
            ("obj", ""),
            ("path", "0123"),
            ("symbol", "line-too-long"),
            ("type", "convention"),
        ]]
        report_result = json.loads(output.getvalue())
        report_result = [sorted(report_result[0].items(),
                                key=lambda item: item[0])]
        self.assertEqual(report_result, expected_result)


if __name__ == '__main__':
    unittest.main()
