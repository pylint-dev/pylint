# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

from typing import Any, Optional

from astroid import nodes

from pylint.interfaces import Confidence
from pylint.testutils.global_test_linter import linter
from pylint.testutils.output_line import MessageTest
from pylint.typing import CheckerStats


class UnittestLinter:
    """A fake linter class to capture checker messages."""

    # pylint: disable=unused-argument, no-self-use

    def __init__(self):
        self._messages = []
        self.stats: CheckerStats = {}

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
    ) -> None:
        # Do not test col_offset for now since changing Message breaks everything
        self._messages.append(MessageTest(msg_id, line, node, args, confidence))

    @staticmethod
    def is_message_enabled(*unused_args, **unused_kwargs):
        return True

    def add_stats(self, **kwargs):
        for name, value in kwargs.items():
            self.stats[name] = value
        return self.stats

    @property
    def options_providers(self):
        return linter.options_providers
