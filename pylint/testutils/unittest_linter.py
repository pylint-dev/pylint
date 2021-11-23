# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

from typing import Any, Optional

from astroid import nodes

from pylint.interfaces import Confidence
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
        node: Optional[nodes.NodeNG] = None,
        args: Any = None,
        confidence: Optional[Confidence] = None,
        col_offset: Optional[int] = None,
        end_lineno: Optional[int] = None,
        end_col_offset: Optional[int] = None,
    ) -> None:
        # Do not test col_offset for now since changing Message breaks everything
        # pylint: disable=fixme
        # TODO: Test end_lineno and end_col_offset :)
        self._messages.append(MessageTest(msg_id, line, node, args, confidence))

    @staticmethod
    def is_message_enabled(*unused_args, **unused_kwargs):
        return True

    @property
    def options_providers(self):
        return linter.options_providers
