# Copyright (c) 2015 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2015-2016 Claudiu Popa <pcmanticore@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the pylint checker in :mod:`pylint.extensions.check_elif
"""

import os
import os.path as osp
import unittest

from pylint import checkers
from pylint.extensions.check_elif import ElseifUsedChecker
from pylint.lint import PyLinter
from pylint.testutils import MinimalTestReporter


class CheckElseIfUsedTC(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._linter = PyLinter()
        cls._linter.set_reporter(MinimalTestReporter())
        checkers.initialize(cls._linter)
        cls._linter.register_checker(ElseifUsedChecker(cls._linter))

    def test_elseif_message(self):
        elif_test = osp.join(osp.dirname(osp.abspath(__file__)), 'data',
                             'elif.py')
        self._linter.check([elif_test])
        msgs = self._linter.reporter.messages
        assert len(msgs) == 2
        for msg in msgs:
            assert msg.symbol == 'else-if-used'
            assert msg.msg == \
                             'Consider using "elif" instead of "else if"'
        assert msgs[0].line == 9
        assert msgs[1].line == 21


if __name__ == '__main__':
    unittest.main()
