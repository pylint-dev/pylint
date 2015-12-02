"""Tests for the pylint checker in :mod:`pylint.extensions.check_elif
"""

import os
import os.path as osp
import unittest

from pylint import checkers
from pylint.extensions.check_elif import ElseifUsedChecker
from pylint.lint import PyLinter
from pylint.reporters import BaseReporter


class TestReporter(BaseReporter):

    def handle_message(self, msg):
        self.messages.append(msg)

    def on_set_current_module(self, module, filepath):
        self.messages = []


class CheckElseIfUsedTC(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._linter = PyLinter()
        cls._linter.set_reporter(TestReporter())
        checkers.initialize(cls._linter)
        cls._linter.register_checker(ElseifUsedChecker(cls._linter))

    def test_elseif_message(self):
        elif_test = osp.join(osp.dirname(osp.abspath(__file__)), 'data',
                             'elif.py')
        self._linter.check([elif_test])
        msgs = self._linter.reporter.messages
        self.assertEqual(len(msgs), 2)
        for msg in msgs:
            self.assertEqual(msg.symbol, 'else-if-used')
            self.assertEqual(msg.msg,
                             'Consider using "elif" instead of "else if"')
        self.assertEqual(msgs[0].line, 9)
        self.assertEqual(msgs[1].line, 21)


if __name__ == '__main__':
    unittest.main()
