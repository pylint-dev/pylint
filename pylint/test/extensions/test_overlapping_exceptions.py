# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the pylint checker in :mod:`pylint.extensions.overlapping_exceptions
"""

from sys import version_info
import os
from os.path import join, dirname
import unittest

from pylint import checkers
from pylint.lint import PyLinter
from pylint.reporters import BaseReporter
from pylint.extensions.overlapping_exceptions import OverlappingExceptionsChecker

class TestReporter(BaseReporter):

    def handle_message(self, msg):
        self.messages.append(msg)

    def on_set_current_module(self, module, filepath):
        self.messages = []


class CheckOverlappingExceptions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._linter = PyLinter()
        cls._linter.set_reporter(TestReporter())
        checkers.initialize(cls._linter)
        cls._linter.register_checker(OverlappingExceptionsChecker(cls._linter))
        cls._linter.disable('I')

    def test_overlapping_exceptions(self):
        test = join(dirname(__file__), 'data', 'overlapping_exceptions.py')
        self._linter.check([test])
        msgs = self._linter.reporter.messages

        expected = [
            (13, 'Overlapping exceptions (SomeException and SomeException are the same)'),
            (18, 'Overlapping exceptions (SomeException is an ancestor class of SubclassException)'),
            (23, 'Overlapping exceptions (SomeException and AliasException are the same)'),
            (28, 'Overlapping exceptions (AliasException is an ancestor class of SubclassException)'),
            (34, 'Overlapping exceptions (SomeException and AliasException are the same)'),
            (34, 'Overlapping exceptions (SomeException is an ancestor class of SubclassException)'),
            (34, 'Overlapping exceptions (AliasException is an ancestor class of SubclassException)'),
            (39, 'Overlapping exceptions (ArithmeticError is an ancestor class of FloatingPointError)'),
            (44, 'Overlapping exceptions (ValueError is an ancestor class of UnicodeDecodeError)')
        ]
        
        self.assertEqual(len(msgs), len(expected))
        for msg, exp in zip(msgs, expected):
            self.assertEqual(msg.msg_id, 'W0714')
            self.assertEqual(msg.symbol, 'overlapping-except')
            self.assertEqual(msg.category, 'warning')
            self.assertEqual((msg.line, msg.msg), exp)

    @unittest.skipIf(version_info < (3, 3), "not relevant to Python version")
    def test_overlapping_exceptions_py33(self):
        """From Python 3.3 both IOError and socket.error are aliases for OSError."""
        test = join(dirname(__file__), 'data', 'overlapping_exceptions_py33.py')
        self._linter.check([test])
        msgs = self._linter.reporter.messages

        expected = [
            (7,  'Overlapping exceptions (IOError and OSError are the same)'),
            (12, 'Overlapping exceptions (socket.error and OSError are the same)'),
            (17, 'Overlapping exceptions (socket.error is an ancestor class of ConnectionError)'),
        ]

        self.assertEqual(len(msgs), len(expected))
        for msg, exp in zip(msgs, expected):
            self.assertEqual(msg.msg_id, 'W0714')
            self.assertEqual(msg.symbol, 'overlapping-except')
            self.assertEqual(msg.category, 'warning')
            self.assertEqual((msg.line, msg.msg), exp)

            
if __name__ == '__main__':
    unittest.main()
