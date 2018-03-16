# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2015-2016 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unittest for the logging checker."""
import astroid

from pylint.checkers import logging
from pylint.testutils import CheckerTestCase, Message, set_config


class TestLoggingModuleDetection(CheckerTestCase):
    CHECKER_CLASS = logging.LoggingChecker

    def test_detects_standard_logging_module(self):
        stmts = astroid.extract_node("""
        import logging #@
        logging.warn('%s' % '%s')  #@
        """)
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        with self.assertAddsMessages(Message('logging-not-lazy', node=stmts[1])):
            self.checker.visit_call(stmts[1])

    def test_dont_crash_on_invalid_format_string(self):
        node = astroid.parse('''
        import logging
        logging.error('0} - {1}'.format(1, 2))
        ''')
        self.walk(node)

    def test_detects_renamed_standard_logging_module(self):
        stmts = astroid.extract_node("""
        import logging as blogging #@
        blogging.warn('%s' % '%s')  #@
        """)
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        with self.assertAddsMessages(Message('logging-not-lazy', node=stmts[1])):
            self.checker.visit_call(stmts[1])

    @set_config(logging_modules=['logging', 'my.logging'])
    def test_nonstandard_logging_module(self):
        stmts = astroid.extract_node("""
        from my import logging as blogging #@
        blogging.warn('%s' % '%s')  #@
        """)
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        with self.assertAddsMessages(Message('logging-not-lazy', node=stmts[1])):
            self.checker.visit_call(stmts[1])
