# -*- coding: utf-8 -*-
# Copyright (c) 2019 Tyler N. Thieding <python@thieding.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the pylint checker in :mod:`pylint.extensions.broad_try_clause
"""

import os.path as osp
import unittest

from pylint import checkers
from pylint.extensions.broad_try_clause import BroadTryClauseChecker
from pylint.lint import PyLinter
from pylint.reporters import BaseReporter


class BroadTryClauseTestReporter(BaseReporter):
    def handle_message(self, msg):
        self.messages.append(msg)

    def on_set_current_module(self, module, filepath):
        self.messages = []


class BroadTryClauseTC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._linter = PyLinter()
        cls._linter.set_reporter(BroadTryClauseTestReporter())
        checkers.initialize(cls._linter)
        cls._linter.register_checker(BroadTryClauseChecker(cls._linter))
        cls._linter.disable("I")

    def test_broad_try_clause_message(self):
        elif_test = osp.join(
            osp.dirname(osp.abspath(__file__)), "data", "broad_try_clause.py"
        )
        self._linter.check([elif_test])
        msgs = self._linter.reporter.messages
        self.assertEqual(len(msgs), 1)

        self.assertEqual(msgs[0].symbol, "too-many-try-statements")
        self.assertEqual(
            msgs[0].msg, "try clause contains 2 statements, expected at most 1"
        )
        self.assertEqual(msgs[0].line, 5)


if __name__ == "__main__":
    unittest.main()
