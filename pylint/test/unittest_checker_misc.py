# Copyright (c) 2003-2016 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the misc checker."""

import unittest

from pylint.checkers import misc
from pylint.testutils import (
    CheckerTestCase, Message,
    set_config, create_file_backed_module,
)


class FixmeTest(CheckerTestCase):
    CHECKER_CLASS = misc.EncodingChecker

    def test_fixme_with_message(self):
        with create_file_backed_module(
                """a = 1
                # FIXME message
                """) as module:
            with self.assertAddsMessages(
                    Message(msg_id='fixme', line=2, args=u'FIXME message')):
                self.checker.process_module(module)

    def test_todo_without_message(self):
        with create_file_backed_module(
                """a = 1
                # TODO
                """) as module:
            with self.assertAddsMessages(
                    Message(msg_id='fixme', line=2, args=u'TODO')):
                self.checker.process_module(module)

    def test_xxx_without_space(self):
        with create_file_backed_module(
                """a = 1
                #XXX
                """) as module:
            with self.assertAddsMessages(
                    Message(msg_id='fixme', line=2, args=u'XXX')):
                self.checker.process_module(module)

    def test_xxx_middle(self):
        with create_file_backed_module(
                """a = 1
                # midle XXX
                """) as module:
            with self.assertNoMessages():
                self.checker.process_module(module)

    def test_without_space_fixme(self):
        with create_file_backed_module(
                """a = 1
                #FIXME
                """) as module:
            with self.assertAddsMessages(
                    Message(msg_id='fixme', line=2, args=u'FIXME')):
                self.checker.process_module(module)

    @set_config(notes=[])
    def test_absent_codetag(self):
        with create_file_backed_module(
                """a = 1
                # FIXME
                # TODO
                # XXX
                """) as module:
            with self.assertNoMessages():
                self.checker.process_module(module)

    @set_config(notes=['CODETAG'])
    def test_other_present_codetag(self):
        with create_file_backed_module(
                """a = 1
                # CODETAG
                # FIXME
                """) as module:
            with self.assertAddsMessages(
                    Message(msg_id='fixme', line=2, args=u'CODETAG')):
                self.checker.process_module(module)


if __name__ == '__main__':
    unittest.main()
