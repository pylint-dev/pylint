# Copyright (c) 2013-2014, 2016-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2016 glegoux <gilles.legoux@gmail.com>
# Copyright (c) 2018 Anthony Sottile <asottile@umich.edu>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the misc checker."""

from pylint.checkers import misc
from pylint.testutils import (
    CheckerTestCase, Message,
    set_config, _create_file_backed_module,
)


class TestFixme(CheckerTestCase):
    CHECKER_CLASS = misc.EncodingChecker

    def test_fixme_with_message(self):
        with _create_file_backed_module(
                """a = 1
                # FIXME message
                """) as module:
            with self.assertAddsMessages(
                    Message(msg_id='fixme', line=2, args='FIXME message')):
                self.checker.process_module(module)

    def test_todo_without_message(self):
        with _create_file_backed_module(
                """a = 1
                # TODO
                """) as module:
            with self.assertAddsMessages(
                    Message(msg_id='fixme', line=2, args='TODO')):
                self.checker.process_module(module)

    def test_xxx_without_space(self):
        with _create_file_backed_module(
                """a = 1
                #XXX
                """) as module:
            with self.assertAddsMessages(
                    Message(msg_id='fixme', line=2, args='XXX')):
                self.checker.process_module(module)

    def test_xxx_middle(self):
        with _create_file_backed_module(
                """a = 1
                # midle XXX
                """) as module:
            with self.assertNoMessages():
                self.checker.process_module(module)

    def test_without_space_fixme(self):
        with _create_file_backed_module(
                """a = 1
                #FIXME
                """) as module:
            with self.assertAddsMessages(
                    Message(msg_id='fixme', line=2, args='FIXME')):
                self.checker.process_module(module)

    @set_config(notes=[])
    def test_absent_codetag(self):
        with _create_file_backed_module(
                """a = 1
                # FIXME
                # TODO
                # XXX
                """) as module:
            with self.assertNoMessages():
                self.checker.process_module(module)

    @set_config(notes=['CODETAG'])
    def test_other_present_codetag(self):
        with _create_file_backed_module(
                """a = 1
                # CODETAG
                # FIXME
                """) as module:
            with self.assertAddsMessages(
                    Message(msg_id='fixme', line=2, args='CODETAG')):
                self.checker.process_module(module)
