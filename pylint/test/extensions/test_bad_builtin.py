# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the pylint checker in :mod:`pylint.extensions.bad_builtin
"""

import os
import os.path as osp
import unittest

from pylint import checkers
from pylint.extensions.bad_builtin import BadBuiltinChecker
from pylint.lint import PyLinter, fix_import_path
from pylint.reporters import BaseReporter


class TestReporter(BaseReporter):

    def handle_message(self, msg):
        self.messages.append(msg)

    def on_set_current_module(self, module, filepath):
        self.messages = []


class BadBuiltinTestCase(unittest.TestCase):

    expected = [
    ]


    @classmethod
    def setUpClass(cls):
        cls._linter = PyLinter()
        cls._linter.set_reporter(TestReporter())
        checkers.initialize(cls._linter)
        cls._linter.register_checker(BadBuiltinChecker(cls._linter))
        cls._linter.disable('I')

    def test_types_redefined(self):
        elif_test = osp.join(osp.dirname(osp.abspath(__file__)), 'data',
                             'bad_builtin.py')
        with fix_import_path([elif_test]):
            self._linter.check([elif_test])
        msgs = sorted(self._linter.reporter.messages, key=lambda item: item.line)
        self.assertEqual(len(msgs), 2)
        for msg, expected in zip(msgs, self.expected):
            self.assertEqual(msg.symbol, 'bad-builtin')
            self.assertEqual(msg.msg, expected)


if __name__ == '__main__':
    unittest.main()
