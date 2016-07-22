# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2015 Aru Sahni <arusahni@gmail.com>
# Copyright (c) 2015-2016 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016 Glenn Matthews <glenn@e-dad.net>

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
from pylint.exceptions import InvalidMessageError


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
        with warnings.catch_warnings(record=True):
            warnings.simplefilter('always')
            walker.walk(astroid.parse("x = 1"))

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


class MessagesStoreRegisterMessagesTest(unittest.TestCase):
    def setUp(self):
        self.store = utils.MessagesStore()

    def test_register_error_inconsistent_checker_id(self):
        class Checker(object):
            name = 'checker'
            msgs = {
                'W1234': ('message one', 'msg-symbol-one', 'msg description'),
                'W4321': ('message two', 'msg-symbol-two', 'msg description'),
            }
        with self.assertRaises(InvalidMessageError) as cm:
            self.store.register_messages(Checker())
        self.assertEqual(str(cm.exception),
                         r"Inconsistent checker part in message id 'W4321' (expected 'x12xx')")

    def test_register_error_new_id_duplicate_of_new(self):
        class CheckerOne(object):
            name = 'checker_one'
            msgs = {
                'W1234': ('message one', 'msg-symbol-one', 'msg description.'),
                }
        class CheckerTwo(object):
            name = 'checker_two'
            msgs = {
                'W1234': ('message two', 'msg-symbol-two', 'another msg description.'),
                }
        self.store.register_messages(CheckerOne())
        with self.assertRaises(InvalidMessageError) as cm:
            self.store.register_messages(CheckerTwo())
        self.assertEqual(str(cm.exception),
                         "Message id 'W1234' is already defined")

    def test_register_error_new_id_duplicate_of_old(self):
        class Checker(object):
            name = 'checker'
            msgs = {
                'W1233': ('message two', 'msg-symbol-two', 'msg description',
                          {'old_names': [('W1234', 'old-symbol')]}),
                'W1234': ('message one', 'msg-symbol-one', 'msg description'),
            }
        with self.assertRaises(InvalidMessageError) as cm:
            self.store.register_messages(Checker())
        self.assertEqual(str(cm.exception),
                         "Message id 'W1234' is already defined")

    def test_register_error_old_id_duplicate_of_new(self):
        class Checker(object):
            name = 'checker'
            msgs = {
                'W1234': ('message one', 'msg-symbol-one', 'msg description'),
                'W1235': ('message two', 'msg-symbol-two', 'msg description',
                          {'old_names': [('W1234', 'old-symbol')]}),
            }
        with self.assertRaises(InvalidMessageError) as cm:
            self.store.register_messages(Checker())
        self.assertEqual(str(cm.exception),
                         "Message id 'W1234' is already defined")

    def test_register_error_old_id_duplicate_of_old(self):
        class Checker(object):
            name = 'checker'
            msgs = {
                'W1234': ('message one', 'msg-symbol-one', 'msg description',
                          {'old_names': [('W1201', 'old-symbol-one')]}),
                'W1235': ('message two', 'msg-symbol-two', 'msg description',
                          {'old_names': [('W1201', 'old-symbol-two')]}),
            }
        with self.assertRaises(InvalidMessageError) as cm:
            self.store.register_messages(Checker())
        self.assertEqual(str(cm.exception),
                         "Message id 'W1201' is already defined")


    def test_register_error_new_symbol_duplicate_of_new(self):
        class Checker(object):
            name = 'checker'
            msgs = {
                'W1234': ('message one', 'msg-symbol', 'msg description'),
                'W1235': ('message two', 'msg-symbol', 'msg description'),
            }
        with self.assertRaises(InvalidMessageError) as cm:
            self.store.register_messages(Checker())
        self.assertEqual(str(cm.exception),
                         "Message symbol 'msg-symbol' is already defined")

    def test_register_error_new_symbol_duplicate_of_old(self):
        class Checker(object):
            name = 'checker'
            msgs = {
                'W1233': ('message two', 'msg-symbol-two', 'msg description',
                          {'old_names': [('W1230', 'msg-symbol-one')]}),
                'W1234': ('message one', 'msg-symbol-one', 'msg description'),
            }
        with self.assertRaises(InvalidMessageError) as cm:
            self.store.register_messages(Checker())
        self.assertEqual(str(cm.exception),
                         "Message symbol 'msg-symbol-one' is already defined")

    def test_register_error_old_symbol_duplicate_of_new(self):
        class Checker(object):
            name = 'checker'
            msgs = {
                'W1234': ('message one', 'msg-symbol-one', 'msg description'),
                'W1235': ('message two', 'msg-symbol-two', 'msg description',
                          {'old_names': [('W1230', 'msg-symbol-one')]}),
            }
        with self.assertRaises(InvalidMessageError) as cm:
            self.store.register_messages(Checker())
        self.assertEqual(str(cm.exception),
                         "Message symbol 'msg-symbol-one' is already defined")

    def test_register_error_old_symbol_duplicate_of_old(self):
        class Checker(object):
            name = 'checker'
            msgs = {
                'W1234': ('message one', 'msg-symbol-one', 'msg description',
                          {'old_names': [('W1230', 'old-symbol-one')]}),
                'W1235': ('message two', 'msg-symbol-two', 'msg description',
                          {'old_names': [('W1231', 'old-symbol-one')]}),
            }
        with self.assertRaises(InvalidMessageError) as cm:
            self.store.register_messages(Checker())
        self.assertEqual(str(cm.exception),
                         "Message alternate name 'old-symbol-one' is already defined")

class MessageDefinitionTest(unittest.TestCase):
    def test_create_invalid_msgid(self):
        with self.assertRaises(InvalidMessageError) as cm:
            utils.MessageDefinition('checker', 'W12345',
                                    'msg', 'descr', 'symbol', 'scope')
        self.assertEqual(str(cm.exception),
                         "Invalid message id 'W12345'")

    def test_create_invalid_message_type(self):
        with self.assertRaises(InvalidMessageError) as cm:
            utils.MessageDefinition('checker', 'Q1234',
                                    'msg', 'descr', 'symbol', 'scope')
        self.assertEqual(str(cm.exception),
                         "Bad message type Q in 'Q1234'")

if __name__ == '__main__':
    unittest.main()
