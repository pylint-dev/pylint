"""Tests for the pylint checker in :mod:`pylint.extensions.check_mccabe
"""

import os.path as osp
import unittest

from pylint import checkers
from pylint.extensions.check_mccabe import McCabeMethodChecker
from pylint.lint import PyLinter
from pylint.reporters import BaseReporter


class TestReporter(BaseReporter):

    def handle_message(self, msg):
        self.messages.append(msg)

    def on_set_current_module(self, module, filepath):
        self.messages = []


class TestMcCabeMethodChecker(unittest.TestCase):
    """Test McCabe Method Checker"""

    expected_msgs = [
        'f1 is too complex. The McCabe rating is 1',
        'f2 is too complex. The McCabe rating is 1',
        'f3 is too complex. The McCabe rating is 3',
        'f4 is too complex. The McCabe rating is 2',
        'f5 is too complex. The McCabe rating is 2',
        'f6 is too complex. The McCabe rating is 2',
        'f7 is too complex. The McCabe rating is 3',
        'f8 is too complex. The McCabe rating is 4',
        'f9 is too complex. The McCabe rating is 9',
        'f10 is too complex. The McCabe rating is 11',
        'method1 is too complex. The McCabe rating is 1',
        "'For 131' is too complex. The McCabe rating is 4",
    ]

    @classmethod
    def setUpClass(cls):
        cls._linter = PyLinter()
        cls._linter.set_reporter(TestReporter())
        checkers.initialize(cls._linter)
        cls._linter.register_checker(McCabeMethodChecker(cls._linter))
        cls._linter.disable('all')
        cls._linter.enable('too-complex')
        cls._linter.global_set_option('max-complexity', 0)

    def test_too_complex_message(self):
        mccabe_test = osp.join(
            osp.dirname(osp.abspath(__file__)), 'data', 'mccabe.py')
        self._linter.check([mccabe_test])
        real_msgs = [message.msg for message in self._linter.reporter.messages]
        self.assertEqual(sorted(self.expected_msgs), sorted(real_msgs))


if __name__ == '__main__':
    unittest.main()
