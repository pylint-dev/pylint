# Copyright 2013 Google Inc.
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
import unittest

from astroid import test_utils
from pylint import utils
from pylint import interfaces
from pylint.checkers.utils import check_messages


class PyLintASTWalkerTest(unittest.TestCase):
    class MockLinter(object):
        def __init__(self, msgs):
            self._msgs = msgs

        def is_message_enabled(self, msgid):
            return self._msgs.get(msgid, True)

    class Checker(object):
        def __init__(self):
            self.called = set()

        @check_messages('first-message')
        def visit_module(self, module):
            self.called.add('module')

        @check_messages('second-message')
        def visit_callfunc(self, module):
            raise NotImplementedError

        @check_messages('second-message', 'third-message')
        def visit_assname(self, module):
            self.called.add('assname')

        @check_messages('second-message')
        def leave_assname(self, module):
            raise NotImplementedError

    def testCheckMessages(self):
        linter = self.MockLinter({'first-message': True,
                                  'second-message': False,
                                  'third-message': True})
        walker = utils.PyLintASTWalker(linter)
        checker = self.Checker()
        walker.add_checker(checker)
        walker.walk(test_utils.build_module("x = func()"))
        self.assertEqual(set(['module', 'assname']), checker.called)


if __name__ == '__main__':
    unittest.main()
