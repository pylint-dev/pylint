# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2015-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Alan Chan <achan961117@gmail.com>
# Copyright (c) 2019-2020 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2019 Svet <svet@hyperscience.com>
# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""Unittest for the logging checker."""
import sys

import astroid
import pytest

from pylint.checkers import logging
from pylint.interfaces import UNDEFINED
from pylint.testutils import CheckerTestCase, Message, set_config


class TestLoggingModuleDetection(CheckerTestCase):
    CHECKER_CLASS = logging.LoggingChecker

    def test_detects_standard_logging_module(self):
        stmts = astroid.extract_node(
            """
        import logging #@
        logging.warn('%s' % '%s')  #@
        """
        )
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        with self.assertAddsMessages(
            Message("logging-not-lazy", node=stmts[1], args=("lazy %",))
        ):
            self.checker.visit_call(stmts[1])

    def test_dont_crash_on_invalid_format_string(self):
        node = astroid.parse(
            """
        import logging
        logging.error('0} - {1}'.format(1, 2))
        """
        )
        self.walk(node)

    def test_detects_renamed_standard_logging_module(self):
        stmts = astroid.extract_node(
            """
        import logging as blogging #@
        blogging.warn('%s' % '%s')  #@
        """
        )
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        with self.assertAddsMessages(
            Message("logging-not-lazy", node=stmts[1], args=("lazy %",))
        ):
            self.checker.visit_call(stmts[1])

    @set_config(logging_modules=["logging", "my.logging"])
    def test_nonstandard_logging_module(self):
        stmts = astroid.extract_node(
            """
        from my import logging as blogging #@
        blogging.warn('%s' % '%s')  #@
        """
        )
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        with self.assertAddsMessages(
            Message("logging-not-lazy", node=stmts[1], args=("lazy %",))
        ):
            self.checker.visit_call(stmts[1])

    def _assert_logging_format_no_messages(self, stmt):
        stmts = astroid.extract_node(
            """
        import logging #@
        logging.error<placeholder> #@
        """.replace(
                "<placeholder>", stmt
            )
        )
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        with self.assertNoMessages():
            self.checker.visit_call(stmts[1])

    def _assert_logging_format_message(self, msg, stmt, args=None, with_too_many=False):
        stmts = astroid.extract_node(
            """
        import logging #@
        logging.error<placeholder> #@
        """.replace(
                "<placeholder>", stmt
            )
        )
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        messages = [Message(msg, node=stmts[1], args=args, confidence=UNDEFINED)]
        if with_too_many:
            messages.append(
                Message("logging-too-many-args", node=stmts[1], confidence=UNDEFINED)
            )
        with self.assertAddsMessages(*messages):
            self.checker.visit_call(stmts[1])

    def _assert_logging_format_too_few_args(self, stmt):
        self._assert_logging_format_message("logging-too-few-args", stmt)

    def _assert_logging_format_too_many_args(self, stmt):
        self._assert_logging_format_message("logging-too-many-args", stmt)

    @set_config(logging_format_style="new")
    def test_brace_format_style_matching_arguments(self):
        self._assert_logging_format_no_messages("('constant string')")
        self._assert_logging_format_no_messages("('{}')")
        self._assert_logging_format_no_messages("('{}', 1)")
        self._assert_logging_format_no_messages("('{0}', 1)")
        self._assert_logging_format_no_messages("('{named}', {'named': 1})")
        self._assert_logging_format_no_messages("('{} {named}', 1, {'named': 1})")
        self._assert_logging_format_no_messages("('{0} {named}', 1, {'named': 1})")

    @set_config(logging_format_style="new")
    def test_brace_format_style_too_few_args(self):
        self._assert_logging_format_too_few_args("('{}, {}', 1)")
        self._assert_logging_format_too_few_args("('{0}, {1}', 1)")
        self._assert_logging_format_too_few_args(
            "('{named1}, {named2}', {'named1': 1})"
        )
        self._assert_logging_format_too_few_args("('{0}, {named}', 1)")
        self._assert_logging_format_too_few_args("('{}, {named}', {'named': 1})")
        self._assert_logging_format_too_few_args("('{0}, {named}', {'named': 1})")

    @set_config(logging_format_style="new")
    def test_brace_format_style_not_enough_arguments(self):
        self._assert_logging_format_too_many_args("('constant string', 1, 2)")
        self._assert_logging_format_too_many_args("('{}', 1, 2)")
        self._assert_logging_format_too_many_args("('{0}', 1, 2)")
        self._assert_logging_format_too_many_args("('{}, {named}', 1, 2, {'named': 1})")
        self._assert_logging_format_too_many_args(
            "('{0}, {named}', 1, 2, {'named': 1})"
        )

    @pytest.mark.skipif(sys.version_info < (3, 6), reason="F-string require >=3.6")
    @set_config(logging_format_style="new")
    def test_fstr_not_new_format_style_matching_arguments(self):
        msg = "logging-fstring-interpolation"
        args = ("lazy %",)
        self._assert_logging_format_message(msg, "(f'{named}')", args)
