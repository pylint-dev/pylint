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
import warnings

import astroid

from pylint import __pkginfo__
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
        def visit_call(self, module):
            raise NotImplementedError

        @check_messages('second-message', 'third-message')
        def visit_assignname(self, module):
            self.called.add('assname')

        @check_messages('second-message')
        def leave_assignname(self, module):
            raise NotImplementedError

    def test_check_messages(self):
        linter = self.MockLinter({'first-message': True,
                                  'second-message': False,
                                  'third-message': True})
        walker = utils.PyLintASTWalker(linter)
        checker = self.Checker()
        walker.add_checker(checker)
        walker.walk(astroid.parse("x = func()"))
        self.assertEqual(set(['module', 'assname']), checker.called)

    def test_deprecated_methods(self):
        class Checker(object):
            def __init__(self):
                self.called = False

            @check_messages('first-message')
            def visit_assname(self, node):
                self.called = True

        linter = self.MockLinter({'first-message': True})
        walker = utils.PyLintASTWalker(linter)
        checker = Checker()
        walker.add_checker(checker)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            walker.walk(astroid.parse("x = 1"))

        if __pkginfo__.numversion < (2, 0):
            expected = ('Implemented method visit_assname instead of '
                        'visit_assignname. This will be supported until '
                        'Pylint 2.0.')
            self.assertEqual(len(w), 1)
            self.assertIsInstance(w[0].message, PendingDeprecationWarning)
            self.assertEqual(str(w[0].message), expected)
            self.assertTrue(checker.called)
        else:
            self.assertNotEqual(len(w), 1)
            self.assertFalse(checker.called)


if __name__ == '__main__':
    unittest.main()
