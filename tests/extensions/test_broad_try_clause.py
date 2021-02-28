# Copyright (c) 2019-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2019-2020 Tyler Thieding <tyler@thieding.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Damien Baty <damien.baty@polyconseil.fr>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the pylint checker in :mod:`pylint.extensions.broad_try_clause`"""
import unittest
from os import path as osp

from pylint import checkers
from pylint.extensions.broad_try_clause import BroadTryClauseChecker
from pylint.lint import PyLinter
from pylint.reporters import BaseReporter


class BroadTryClauseTestReporter(BaseReporter):
    def handle_message(self, msg):
        self.messages.append(msg)

    def on_set_current_module(self, module, filepath):
        self.messages = []

    def _display(self, layout):
        pass


class BroadTryClauseTC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._linter = PyLinter()
        cls._linter.set_reporter(BroadTryClauseTestReporter())
        checkers.initialize(cls._linter)
        cls._linter.register_checker(BroadTryClauseChecker(cls._linter))
        cls._linter.disable("I")

    def test_broad_try_clause_message(self):
        broad_try_clause_test = osp.join(
            osp.dirname(osp.abspath(__file__)), "data", "broad_try_clause.py"
        )
        self._linter.check([broad_try_clause_test])
        msgs = self._linter.reporter.messages
        self.assertEqual(len(msgs), 4)

        self.assertEqual(msgs[0].symbol, "too-many-try-statements")
        self.assertEqual(
            msgs[0].msg, "try clause contains 3 statements, expected at most 1"
        )
        self.assertEqual(msgs[0].line, 5)

        self.assertEqual(msgs[1].symbol, "too-many-try-statements")
        self.assertEqual(
            msgs[1].msg, "try clause contains 3 statements, expected at most 1"
        )
        self.assertEqual(msgs[1].line, 12)

        self.assertEqual(msgs[2].symbol, "too-many-try-statements")
        self.assertEqual(
            msgs[2].msg, "try clause contains 4 statements, expected at most 1"
        )
        self.assertEqual(msgs[2].line, 19)

        self.assertEqual(msgs[3].symbol, "too-many-try-statements")
        self.assertEqual(
            msgs[3].msg, "try clause contains 7 statements, expected at most 1"
        )
        self.assertEqual(msgs[3].line, 29)
