# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the pylint checker in :mod:`pylint.extensions.check_docstring
"""

import os.path as osp
import unittest

from pylint import checkers
from pylint.extensions.docstyle import DocStringStyleChecker
from pylint.lint import PyLinter
from pylint.reporters import BaseReporter


class TestReporter(BaseReporter):

    def handle_message(self, msg):
        self.messages.append(msg)

    def on_set_current_module(self, module, filepath):
        self.messages = []


class CheckDocStringStyleTest(unittest.TestCase):

    expected_msg = [
        'First line empty in function docstring',
        'First line empty in class docstring',
        'First line empty in method docstring',
        'Bad docstring quotes in method, expected """, given \'\'\'',
        'Bad docstring quotes in method, expected """, given "',
        'Bad docstring quotes in method, expected """, given \'',
        'Bad docstring quotes in method, expected """, given \'',
    ]
    expected_symbol = [
        'docstring-first-line-empty',
        'docstring-first-line-empty',
        'docstring-first-line-empty',
        'bad-docstring-quotes',
        'bad-docstring-quotes',
        'bad-docstring-quotes',
        'bad-docstring-quotes',
    ]

    @classmethod
    def setUpClass(cls):
        cls._linter = PyLinter()
        cls._linter.set_reporter(TestReporter())
        checkers.initialize(cls._linter)
        cls._linter.register_checker(DocStringStyleChecker(cls._linter))

    def test_docstring_message(self):
        docstring_test = osp.join(osp.dirname(osp.abspath(__file__)), 'data',
                                  'docstring.py')
        self._linter.check([docstring_test])
        msgs = self._linter.reporter.messages
        self.assertEqual(len(msgs), 7)
        for msg, expected_symbol, expected_msg in zip(msgs,
                                                      self.expected_symbol,
                                                      self.expected_msg):
            self.assertEqual(msg.symbol, expected_symbol)
            self.assertEqual(msg.msg, expected_msg)


if __name__ == '__main__':
    unittest.main()
