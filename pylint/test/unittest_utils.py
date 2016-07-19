# Copyright (c) 2003-2016 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import re
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


class RegexBlacklistTest(unittest.TestCase):
    def test__basename_in_blacklist_re_match(self):
        patterns = [re.compile(".*enchilada.*"), re.compile("unittest_.*")]
        self.assertTrue(utils._basename_in_blacklist_re("unittest_utils.py", patterns))
        self.assertTrue(utils._basename_in_blacklist_re("cheese_enchiladas.xml", patterns))

    def test__basename_in_blacklist_re_nomatch(self):
        patterns = [re.compile(".*enchilada.*"), re.compile("unittest_.*")]
        self.assertFalse(utils._basename_in_blacklist_re("test_utils.py", patterns))
        self.assertFalse(utils._basename_in_blacklist_re("enchilad.py", patterns))

if __name__ == '__main__':
    unittest.main()
