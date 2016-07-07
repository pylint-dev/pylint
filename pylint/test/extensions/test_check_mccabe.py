# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the pylint checker in :mod:`pylint.extensions.check_mccabe
"""

import os.path as osp
import unittest

from pylint import checkers
from pylint.extensions.mccabe import register
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
        "'f1' is too complex. The McCabe rating is 1",
        "'f2' is too complex. The McCabe rating is 1",
        "'f3' is too complex. The McCabe rating is 3",
        "'f4' is too complex. The McCabe rating is 2",
        "'f5' is too complex. The McCabe rating is 2",
        "'f6' is too complex. The McCabe rating is 2",
        "'f7' is too complex. The McCabe rating is 3",
        "'f8' is too complex. The McCabe rating is 4",
        "'f9' is too complex. The McCabe rating is 9",
        "'method1' is too complex. The McCabe rating is 1",
        "This 'for' is too complex. The McCabe rating is 4",
        "'method3' is too complex. The McCabe rating is 2",
        "'f10' is too complex. The McCabe rating is 11",
        "'method2' is too complex. The McCabe rating is 18",
    ]

    @classmethod
    def setUpClass(cls):
        cls._linter = PyLinter()
        cls._linter.set_reporter(TestReporter())
        checkers.initialize(cls._linter)
        register(cls._linter)
        cls._linter.disable('all')
        cls._linter.enable('too-complex')

    def setUp(self):
        self.fname_mccabe_example = osp.join(
            osp.dirname(osp.abspath(__file__)), 'data', 'mccabe.py')

    def test_too_complex_message(self):
        self._linter.global_set_option('max-complexity', 0)
        self._linter.check([self.fname_mccabe_example])
        real_msgs = [message.msg for message in self._linter.reporter.messages]
        self.assertEqual(sorted(self.expected_msgs), sorted(real_msgs))

    def test_max_mccabe_rate(self):
        self._linter.global_set_option('max-complexity', 9)
        self._linter.check([self.fname_mccabe_example])
        real_msgs = [message.msg for message in self._linter.reporter.messages]
        self.assertEqual(sorted(self.expected_msgs[-2:]), sorted(real_msgs))


if __name__ == '__main__':
    unittest.main()
