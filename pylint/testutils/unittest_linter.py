# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from typing import Any, Optional

from astroid import nodes

from pylint.interfaces import UNDEFINED, Confidence
from pylint.testutils.global_test_linter import linter
from pylint.testutils.output_line import MessageTest
from pylint.utils import LinterStats


class UnittestLinter:
    """A fake linter class to capture checker messages."""

    # pylint: disable=unused-argument

    def __init__(self):
        self._messages = []
        self.stats = LinterStats()

    def release_messages(self):
        try:
            return self._messages
        finally:
            self._messages = []

    def add_message(
        self,
        msg_id: str,
        line: Optional[int] = None,
        # pylint: disable=fixme
        # TODO: Make node non optional
        node: Optional[nodes.NodeNG] = None,
        args: Any = None,
        confidence: Optional[Confidence] = None,
        col_offset: Optional[int] = None,
        end_lineno: Optional[int] = None,
        end_col_offset: Optional[int] = None,
    ) -> None:
        """Add a MessageTest to the _messages attribute of the linter class."""
        # If confidence is None we set it to UNDEFINED as well in PyLinter
        if confidence is None:
            confidence = UNDEFINED

        # Look up "location" data of node if not yet supplied
        if node:
            if node.position:
                if not line:
                    line = node.position.lineno
                if not col_offset:
                    col_offset = node.position.col_offset
                if not end_lineno:
                    end_lineno = node.position.end_lineno
                if not end_col_offset:
                    end_col_offset = node.position.end_col_offset
            else:
                if not line:
                    line = node.fromlineno
                if not col_offset:
                    col_offset = node.col_offset
                if not end_lineno:
                    end_lineno = node.end_lineno
                if not end_col_offset:
                    end_col_offset = node.end_col_offset

        self._messages.append(
            MessageTest(
                msg_id,
                line,
                node,
                args,
                confidence,
                col_offset,
                end_lineno,
                end_col_offset,
            )
        )

    @staticmethod
    def is_message_enabled(*unused_args, **unused_kwargs):
        return True

    @property
    def options_providers(self):
        return linter.options_providers
