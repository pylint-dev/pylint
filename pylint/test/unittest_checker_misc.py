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
from pylint.testutils import CheckerTestCase, Message, set_config, _tokenize_str


class TestFixme(CheckerTestCase):
    CHECKER_CLASS = misc.EncodingChecker

    def test_fixme_with_message(self):
        code = """a = 1
                # FIXME message
                """
        with self.assertAddsMessages(
            Message(msg_id="fixme", line=2, args="FIXME message")
        ):
            self.checker.process_tokens(_tokenize_str(code))

    def test_todo_without_message(self):
        code = """a = 1
                # TODO
                """
        with self.assertAddsMessages(Message(msg_id="fixme", line=2, args="TODO")):
            self.checker.process_tokens(_tokenize_str(code))

    def test_xxx_without_space(self):
        code = """a = 1
                #XXX
                """
        with self.assertAddsMessages(Message(msg_id="fixme", line=2, args="XXX")):
            self.checker.process_tokens(_tokenize_str(code))

    def test_xxx_middle(self):
        code = """a = 1
                # midle XXX
                """
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str(code))

    def test_without_space_fixme(self):
        code = """a = 1
                #FIXME
                """
        with self.assertAddsMessages(Message(msg_id="fixme", line=2, args="FIXME")):
            self.checker.process_tokens(_tokenize_str(code))

    @set_config(notes=[])
    def test_absent_codetag(self):
        code = """a = 1
                # FIXME	                # FIXME
                # TODO	                # TODO
                # XXX	                # XXX
                """
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str(code))

    @set_config(notes=["CODETAG"])
    def test_other_present_codetag(self):
        code = """a = 1
                # CODETAG
                # FIXME
                """
        with self.assertAddsMessages(Message(msg_id="fixme", line=2, args="CODETAG")):
            self.checker.process_tokens(_tokenize_str(code))

    def test_issue_2321_should_not_trigger(self):
        code = 'print("# TODO this should not trigger a fixme")'
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str(code))

    def test_issue_2321_should_trigger(self):
        code = "# TODO this should not trigger a fixme"
        with self.assertAddsMessages(
            Message(msg_id="fixme", line=1, args="TODO this should not trigger a fixme")
        ):
            self.checker.process_tokens(_tokenize_str(code))

    def test_dont_trigger_on_todoist(self):
        code = """
        # Todoist API: What is this task about?
        # Todoist API: Look up a task's due date
        # Todoist API: Look up a Project/Label/Task ID
        # Todoist API: Fetch all labels
        # Todoist API: "Name" value
        # Todoist API: Get a task's priority
        # Todoist API: Look up the Project ID a Task belongs to
        # Todoist API: Fetch all Projects
        # Todoist API: Fetch all Tasks
        """
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str(code))
