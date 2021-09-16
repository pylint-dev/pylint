# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

from io import StringIO
from os import getcwd, linesep, sep
from typing import TYPE_CHECKING, Dict, List, Optional

from pylint import interfaces
from pylint.message import Message
from pylint.reporters import BaseReporter

if TYPE_CHECKING:
    from pylint.reporters.ureports.nodes import Section


class GenericTestReporter(BaseReporter):
    """reporter storing plain text messages"""

    __implements__ = interfaces.IReporter

    def __init__(
        self,
    ):  # pylint: disable=super-init-not-called # See https://github.com/PyCQA/pylint/issues/4941
        self.reset()

    def reset(self):
        self.message_ids: Dict = {}
        self.out = StringIO()
        self.path_strip_prefix: str = getcwd() + sep
        self.messages: List[str] = []

    def handle_message(self, msg: Message) -> None:
        """manage message of different type and in the context of path"""
        obj = msg.obj
        line = msg.line
        msg_id = msg.msg_id
        str_message: str = msg.msg
        self.message_ids[msg_id] = 1
        if obj:
            obj = f":{obj}"
        sigle = msg_id[0]
        if linesep != "\n":
            # 2to3 writes os.linesep instead of using
            # the previously used line separators
            str_message = str_message.replace("\r\n", "\n")
        self.messages.append(f"{sigle}:{line:>3}{obj}: {str_message}")

    def finalize(self):
        self.messages.sort()
        for msg in self.messages:
            print(msg, file=self.out)
        result = self.out.getvalue()
        self.reset()
        return result

    # pylint: disable=unused-argument
    def on_set_current_module(self, module: str, filepath: Optional[str]) -> None:
        pass

    # pylint: enable=unused-argument

    def display_reports(self, layout: "Section") -> None:
        """ignore layouts"""

    def _display(self, layout: "Section") -> None:
        pass


class MinimalTestReporter(BaseReporter):
    def on_set_current_module(self, module: str, filepath: Optional[str]) -> None:
        self.messages = []

    def _display(self, layout: "Section") -> None:
        pass


class FunctionalTestReporter(BaseReporter):
    def on_set_current_module(self, module: str, filepath: Optional[str]) -> None:
        self.messages = []

    def display_reports(self, layout: "Section") -> None:
        """Ignore layouts and don't call self._display()."""

    def _display(self, layout: "Section") -> None:
        pass
