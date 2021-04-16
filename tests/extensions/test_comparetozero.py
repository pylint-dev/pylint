# Copyright (c) 2016 Alexander Todorov <atodorov@otb.bg>
# Copyright (c) 2016 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2017-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""Tests for the pylint checker in :mod:`pylint.extensions.emptystring"""

import os
import unittest

from pylint import checkers
from pylint.extensions.comparetozero import CompareToZeroChecker
from pylint.lint import PyLinter
from pylint.reporters import BaseReporter


class CompareToZeroTestReporter(BaseReporter):
    def handle_message(self, msg):
        self.messages.append(msg)

    def on_set_current_module(self, module, filepath):
        self.messages = []

    def _display(self, layout):
        pass


class CompareToZeroUsedTC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._linter = PyLinter()
        cls._linter.set_reporter(CompareToZeroTestReporter())
        checkers.initialize(cls._linter)
        cls._linter.register_checker(CompareToZeroChecker(cls._linter))
        cls._linter.disable("I")

    def test_comparetozero_message(self):
        elif_test = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data", "compare_to_zero.py"
        )
        self._linter.check([elif_test])
        msgs = self._linter.reporter.messages
        self.assertEqual(len(msgs), 4)
        for msg in msgs:
            self.assertEqual(msg.symbol, "compare-to-zero")
            self.assertEqual(msg.msg, "Avoid comparisons to zero")
        self.assertEqual(msgs[0].line, 6)
        self.assertEqual(msgs[1].line, 9)
        self.assertEqual(msgs[2].line, 12)
        self.assertEqual(msgs[3].line, 15)
