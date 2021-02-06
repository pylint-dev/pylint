# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import contextlib
from typing import Dict, Optional, Type

from pylint.testutils.global_test_linter import linter
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
    def assertAddsMessages(self, *messages):
        """Assert that exactly the given method adds the given messages.

        The list of messages must exactly match *all* the messages added by the
        method. Additionally, we check to see whether the args in each message can
        actually be substituted into the message string.
        """
        yield
        got = self.linter.release_messages()
        msg = "Expected messages did not match actual.\n" "Expected:\n%s\nGot:\n%s" % (
            "\n".join(repr(m) for m in messages),
            "\n".join(repr(m) for m in got),
        )
        assert list(messages) == got, msg

    def walk(self, node):
        """recursive walk on the given node"""
        walker = ASTWalker(linter)
        walker.add_checker(self.checker)
        walker.walk(node)
