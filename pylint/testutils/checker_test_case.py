# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import contextlib
from collections.abc import Generator, Iterator
from typing import Any

from astroid import nodes

from pylint.testutils.global_test_linter import linter
from pylint.testutils.output_line import MessageTest
from pylint.testutils.unittest_linter import UnittestLinter
from pylint.utils import ASTWalker


class CheckerTestCase:
    """A base testcase class for unit testing individual checker classes."""

    # TODO: Figure out way to type this as type[BaseChecker] while also
    # setting self.checker correctly.
    CHECKER_CLASS: Any
    CONFIG: dict[str, Any] = {}

    def setup_method(self) -> None:
        self.linter = UnittestLinter()
        self.checker = self.CHECKER_CLASS(self.linter)
        for key, value in self.CONFIG.items():
            setattr(self.checker.linter.config, key, value)
        self.checker.open()

    @contextlib.contextmanager
    def assertNoMessages(self) -> Iterator[None]:
        """Assert that no messages are added by the given method."""
        with self.assertAddsMessages():
            yield

    @contextlib.contextmanager
    def assertDoesNotAddMessages(
        self, *messages: MessageTest, ignore_position: bool = False
    ) -> Generator[None]:
        """Assert that the given messages are not added by the given method.

        This is different from ``assertNoMessages`` which asserts that no
        messages at all are added. ``assertDoesNotAddMessages`` checks that
        none of the *specific* messages passed as arguments are emitted, while
        other messages may still be present.
        """
        if not messages:
            raise TypeError(
                "assertDoesNotAddMessages requires at least one MessageTest argument"
            )
        try:
            yield
        except Exception:
            self.linter.release_messages()
            raise
        else:
            got = self.linter.release_messages()
            for unwanted in messages:
                for gotten_msg in got:
                    if not self._messages_match(unwanted, gotten_msg, ignore_position):
                        continue
                    got_str = "\n".join(repr(m) for m in got)
                    msg = (
                        "Expected the following message to not be raised:\n"
                        f"\n  {unwanted!r}\n\n"
                        f"but it was found among the actual messages:\n\n{got_str}\n"
                    )
                    raise AssertionError(msg)

    @staticmethod
    def _messages_match(
        expected: MessageTest, actual: MessageTest, ignore_position: bool
    ) -> bool:
        if expected.msg_id != actual.msg_id:
            return False
        if expected.node != actual.node:
            return False
        if expected.args != actual.args:
            return False
        if expected.confidence != actual.confidence:
            return False
        if not ignore_position:
            if expected.line != actual.line:
                return False
            if expected.col_offset != actual.col_offset:
                return False
            if expected.end_line != actual.end_line:
                return False
            if expected.end_col_offset != actual.end_col_offset:
                return False
        return True

    @contextlib.contextmanager
    def assertAddsMessages(
        self, *messages: MessageTest, ignore_position: bool = False
    ) -> Generator[None]:
        """Assert that exactly the given method adds the given messages.

        The list of messages must exactly match *all* the messages added by the
        method. Additionally, we check to see whether the args in each message can
        actually be substituted into the message string.

        Using the keyword argument `ignore_position`, all checks for position
        arguments (line, col_offset, ...) will be skipped. This can be used to
        just test messages for the correct node.
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

        assert len(messages) == len(got), msg

        for expected_msg, gotten_msg in zip(messages, got):
            assert expected_msg.msg_id == gotten_msg.msg_id, msg
            assert expected_msg.node == gotten_msg.node, msg
            assert expected_msg.args == gotten_msg.args, msg
            assert expected_msg.confidence == gotten_msg.confidence, msg

            if ignore_position:
                # Do not check for line, col_offset etc...
                continue

            assert expected_msg.line == gotten_msg.line, msg
            assert expected_msg.col_offset == gotten_msg.col_offset, msg
            assert expected_msg.end_line == gotten_msg.end_line, msg
            assert expected_msg.end_col_offset == gotten_msg.end_col_offset, msg

    def walk(self, node: nodes.NodeNG) -> None:
        """Recursive walk on the given node."""
        walker = ASTWalker(linter)
        walker.add_checker(self.checker)
        walker.walk(node)
