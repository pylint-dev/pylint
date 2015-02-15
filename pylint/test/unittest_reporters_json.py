# Copyright (c) 2003-2015 LOGILAB S.A. (Paris, FRANCE).
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

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
        reporter.display_results(None)
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
