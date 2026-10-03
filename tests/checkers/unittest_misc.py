# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

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
                # middle XXX
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

    @set_config(notes=["???"])
    def test_non_alphanumeric_codetag(self) -> None:
        code = """a = 1
                #???
                """
        with self.assertAddsMessages(
            MessageTest(msg_id="fixme", line=2, args="???", col_offset=17)
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
