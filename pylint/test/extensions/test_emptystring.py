# Copyright (c) 2016 Alexander Todorov <atodorov@MrSenko.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the pylint checker in :mod:`pylint.extensions.emptystring
"""

import os
import os.path as osp
import unittest

from pylint import checkers
from pylint.extensions.emptystring import CompareToEmptyStringChecker
from pylint.lint import PyLinter
from pylint.reporters import BaseReporter


class EmptyStringTestReporter(BaseReporter):

    def handle_message(self, msg):
        self.messages.append(msg)

    def on_set_current_module(self, module, filepath):
        self.messages = []


class CheckEmptyStringUsedTC(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._linter = PyLinter()
        cls._linter.set_reporter(EmptyStringTestReporter())
        checkers.initialize(cls._linter)
        cls._linter.register_checker(CompareToEmptyStringChecker(cls._linter))
        cls._linter.disable('I')

    def test_emptystring_message(self):
        elif_test = osp.join(osp.dirname(osp.abspath(__file__)), 'data',
                             'empty_string_comparison.py')
        self._linter.check([elif_test])
        msgs = self._linter.reporter.messages
        self.assertEqual(len(msgs), 4)
        for msg in msgs:
            self.assertEqual(msg.symbol, 'compare-to-empty-string')
            self.assertEqual(msg.msg, 'Avoid comparisons to empty string')
        self.assertEqual(msgs[0].line, 6)
        self.assertEqual(msgs[1].line, 9)
        self.assertEqual(msgs[2].line, 12)
        self.assertEqual(msgs[3].line, 15)


if __name__ == '__main__':
    unittest.main()
