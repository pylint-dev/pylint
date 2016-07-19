# Copyright (c) 2003-2016 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import os
from os.path import join, dirname, abspath
import unittest

import six

from pylint import __pkginfo__
from pylint.lint import PyLinter
from pylint import checkers
from pylint.reporters import BaseReporter
from pylint.reporters.text import TextReporter, ParseableTextReporter
from pylint.reporters.html import HTMLReporter
from pylint.reporters.ureports.nodes import Section
from pylint import testutils


HERE = abspath(dirname(__file__))
INPUTDIR = join(HERE, 'input')

class PyLinterTC(unittest.TestCase):

    def setUp(self):
        self.linter = PyLinter(reporter=TextReporter())
        self.linter.disable('I')
        self.linter.config.persistent = 0
        # register checkers
        checkers.initialize(self.linter)
        os.environ.pop('PYLINTRC', None)

    def test_template_option(self):
        output = six.StringIO()
        self.linter.reporter.set_output(output)
        self.linter.set_option('msg-template', '{msg_id}:{line:03d}')
        self.linter.open()
        self.linter.set_current_module('0123')
        self.linter.add_message('C0301', line=1, args=(1, 2))
        self.linter.add_message('line-too-long', line=2, args=(3, 4))
        self.assertMultiLineEqual(output.getvalue(),
                                  '************* Module 0123\n'
                                  'C0301:001\n'
                                  'C0301:002\n')

    def test_parseable_output_deprecated(self):
        with testutils.catch_warnings() as cm:
            ParseableTextReporter()
        
        self.assertEqual(len(cm), 1)
        self.assertIsInstance(cm[0].message, DeprecationWarning)

    def test_html_reporter_deprecated(self):
        with testutils.catch_warnings() as caught:
            HTMLReporter()

        self.assertEqual(len(caught), 1)
        self.assertIsInstance(caught[0].message, DeprecationWarning)
        self.assertEqual(str(caught[0].message),
                         'This reporter will be removed in Pylint 2.0.')

    def test_parseable_output_regression(self):
        output = six.StringIO()
        with testutils.catch_warnings():
            linter = PyLinter(reporter=ParseableTextReporter())

        checkers.initialize(linter)
        linter.config.persistent = 0
        linter.reporter.set_output(output)
        linter.set_option('output-format', 'parseable')
        linter.open()
        linter.set_current_module('0123')
        linter.add_message('line-too-long', line=1, args=(1, 2))
        self.assertMultiLineEqual(output.getvalue(),
                                  '************* Module 0123\n'
                                  '0123:1: [C0301(line-too-long), ] '
                                  'Line too long (1/2)\n')

    def test_html_reporter_msg_template(self):
        expected = '''
<html>
<body>
<div>
<div>
<h2>Messages</h2>
<table>
<tr class="header">
<th>category</th>
<th>msg_id</th>
</tr>
<tr class="even">
<td>warning</td>
<td>W0332</td>
</tr>
</table>
</div>
</div>
</body>
</html>'''.strip().splitlines()
        output = six.StringIO()
        with testutils.catch_warnings():
            linter = PyLinter(reporter=HTMLReporter())

        checkers.initialize(linter)
        linter.config.persistent = 0
        linter.reporter.set_output(output)
        linter.set_option('msg-template', '{category}{msg_id}')
        linter.open()
        linter.set_current_module('0123')
        linter.add_message('lowercase-l-suffix', line=1)
        linter.reporter.display_messages(Section())
        self.assertEqual(output.getvalue().splitlines(), expected)

    @unittest.expectedFailure
    def test_html_reporter_type(self):
        # Integration test for issue #263
        # https://bitbucket.org/logilab/pylint/issue/263/html-report-type-problems
        expected = '''<html>
<body>
<div>
<div>
<h2>Messages</h2>
<table>
<tr class="header">
<th>type</th>
<th>module</th>
<th>object</th>
<th>line</th>
<th>col_offset</th>
<th>message</th>
</tr>
<tr class="even">
<td>convention</td>
<td>0123</td>
<td>&#160;</td>
<td>1</td>
<td>0</td>
<td>Exactly one space required before comparison
a&lt; 5: print "zero"</td>
</tr>
</table>
</div>
</div>
</body>
</html>
'''
        output = six.StringIO()
        with testutils.catch_warnings():
            linter = PyLinter(reporter=HTMLReporter())

        checkers.initialize(linter)
        linter.config.persistent = 0
        linter.reporter.set_output(output)
        linter.open()
        linter.set_current_module('0123')
        linter.add_message('bad-whitespace', line=1,
                           args=('Exactly one', 'required', 'before',
                                 'comparison', 'a< 5: print "zero"'))
        linter.reporter.display_reports(Section())
        self.assertMultiLineEqual(output.getvalue(), expected)

    def test_display_results_is_renamed(self):
        class CustomReporter(TextReporter):
            def _display(self, layout):
                return None

        reporter = CustomReporter()
        if __pkginfo__.numversion >= (2, 0):
            with self.assertRaises(AttributeError):
                reporter.display_results
        else:
            with testutils.catch_warnings() as cm:
                reporter.display_results(Section())

            self.assertEqual(len(cm), 1)
            self.assertIsInstance(cm[0].message, DeprecationWarning)


if __name__ == '__main__':
    unittest.main()
