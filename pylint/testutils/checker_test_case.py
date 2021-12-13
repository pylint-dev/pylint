# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import contextlib
from typing import Dict, Generator, Optional, Type

from pylint.constants import PY38_PLUS
from pylint.testutils.global_test_linter import linter
from pylint.testutils.output_line import MessageTest
from pylint.testutils.unittest_linter import UnittestLinter
from pylint.utils import ASTWalker


class CheckerTestCase:
    """A base testcase class for unit testing individual checker classes."""

    CHECKER_CLASS: Optional[Type] = None
    CONFIG: Dict = {}

    def setup_method(self):
        self.linter = UnittestLinter()
        self.checker = self.CHECKER_CLASS(self.linter)  # pylint: disable=not-callable
        for key, value in self.CONFIG.items():
            setattr(self.checker.config, key, value)
        self.checker.open()

    @contextlib.contextmanager
    def assertNoMessages(self):
        """Assert that no messages are added by the given method."""
        with self.assertAddsMessages():
            yield

    @contextlib.contextmanager
    def assertAddsMessages(self, *messages: MessageTest) -> Generator[None, None, None]:
        """Assert that exactly the given method adds the given messages.

        The list of messages must exactly match *all* the messages added by the
        method. Additionally, we check to see whether the args in each message can
        actually be substituted into the message string.
        """
        yield
        got = self.linter.release_messages()
        no_msg = "No message."
        expected = "\n".join(repr(m) for m in messages) or no_msg
        got_str = "\n".join(repr(m) for m in got) or no_msg
        msg = (
            "Expected messages did not match actual.\n"
            f"\nExpected:\n{expected}\n\nGot:\n{got_str}\n"
        )

        assert len(messages) == len(got)

        for expected_msg, gotten_msg in zip(messages, got):
            assert expected_msg.msg_id == gotten_msg.msg_id, msg
            assert expected_msg.line == gotten_msg.line, msg
            assert expected_msg.node == gotten_msg.node, msg
            assert expected_msg.args == gotten_msg.args, msg
            assert expected_msg.confidence == gotten_msg.confidence, msg
            assert expected_msg.col_offset == gotten_msg.col_offset, msg
            if PY38_PLUS:
                assert expected_msg.end_line == gotten_msg.end_line, msg
                assert expected_msg.end_col_offset == gotten_msg.end_col_offset, msg

    def walk(self, node):
        """recursive walk on the given node"""
        walker = ASTWalker(linter)
        walker.add_checker(self.checker)
        walker.walk(node)
