# Copyright (c) 2013-2014, 2016-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2016 glegoux <gilles.legoux@gmail.com>
# Copyright (c) 2018 Rogalski, Lukasz <lukasz.rogalski@intel.com>
# Copyright (c) 2018 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Tests for the misc checker."""

from pylint.checkers import misc
from pylint.testutils import CheckerTestCase, MessageTest, _tokenize_str, set_config


class TestFixme(CheckerTestCase):
    CHECKER_CLASS = misc.EncodingChecker

    def test_fixme_with_message(self) -> None:
        code = """a = 1
                # FIXME message
                """
        with self.assertAddsMessages(
            MessageTest(msg_id="fixme", line=2, args="FIXME message", col_offset=17)
        ):
            self.checker.process_tokens(_tokenize_str(code))

    def test_todo_without_message(self) -> None:
        code = """a = 1
                # TODO
                """
        with self.assertAddsMessages(
            MessageTest(msg_id="fixme", line=2, args="TODO", col_offset=17)
        ):
            self.checker.process_tokens(_tokenize_str(code))

    def test_xxx_without_space(self) -> None:
        code = """a = 1
                #XXX
                """
        with self.assertAddsMessages(
            MessageTest(msg_id="fixme", line=2, args="XXX", col_offset=17)
        ):
            self.checker.process_tokens(_tokenize_str(code))

    def test_xxx_middle(self) -> None:
        code = """a = 1
                # midle XXX
                """
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str(code))

    def test_without_space_fixme(self) -> None:
        code = """a = 1
                #FIXME
                """
        with self.assertAddsMessages(
            MessageTest(msg_id="fixme", line=2, args="FIXME", col_offset=17)
        ):
            self.checker.process_tokens(_tokenize_str(code))

    @set_config(notes=[])
    def test_absent_codetag(self) -> None:
        code = """a = 1
                # FIXME	                # FIXME
                # TODO	                # TODO
                # XXX	                # XXX
                """
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str(code))

    @set_config(notes=["CODETAG"])
    def test_other_present_codetag(self) -> None:
        code = """a = 1
                # CODETAG
                # FIXME
                """
        with self.assertAddsMessages(
            MessageTest(msg_id="fixme", line=2, args="CODETAG", col_offset=17)
        ):
            self.checker.process_tokens(_tokenize_str(code))

    def test_issue_2321_should_not_trigger(self) -> None:
        code = 'print("# TODO this should not trigger a fixme")'
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str(code))

    def test_issue_2321_should_trigger(self) -> None:
        code = "# TODO this should not trigger a fixme"
        with self.assertAddsMessages(
            MessageTest(
                msg_id="fixme",
                line=1,
                args="TODO this should not trigger a fixme",
                col_offset=1,
            )
        ):
            self.checker.process_tokens(_tokenize_str(code))

    def test_dont_trigger_on_todoist(self) -> None:
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
