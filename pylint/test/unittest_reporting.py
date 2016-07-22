# Copyright (c) 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014-2016 Claudiu Popa <pcmanticore@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import os
from os.path import join, dirname, abspath
import unittest
import warnings

import six

from pylint import __pkginfo__
from pylint.lint import PyLinter
from pylint import checkers
from pylint.reporters import BaseReporter
from pylint.reporters.text import TextReporter, ParseableTextReporter
from pylint.reporters.ureports.nodes import Section


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
        with warnings.catch_warnings(record=True) as cm:
            warnings.simplefilter("always")
            ParseableTextReporter()
        
        self.assertEqual(len(cm), 1)
        self.assertIsInstance(cm[0].message, DeprecationWarning)

    def test_parseable_output_regression(self):
        output = six.StringIO()
        with warnings.catch_warnings(record=True):
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

    def test_display_results_is_renamed(self):
        class CustomReporter(TextReporter):
            def _display(self, layout):
                return None

        reporter = CustomReporter()
        with self.assertRaises(AttributeError):
            reporter.display_results


if __name__ == '__main__':
    unittest.main()
