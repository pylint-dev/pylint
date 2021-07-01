# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE


import os
from typing import IO, Any, AnyStr, Callable, List, Mapping, Optional, Union

from pylint.interfaces import IReporter
from pylint.message import Message
from pylint.reporters.base_reporter import BaseReporter
from pylint.reporters.ureports.nodes import BaseLayout

AnyFile = IO[AnyStr]
AnyPath = Union[str, bytes, os.PathLike]
PyLinter = Any


class MultiReporter:
    """Reports messages and layouts in plain text"""

    __implements__ = IReporter
    name = "_internal_multi_reporter"
    # Note: do not register this reporter with linter.register_reporter as it is
    #       not intended to be used directly like a regular reporter, but is
    #       instead used to implement the
    #       `--output-format=json:somefile.json,colorized`
    #       multiple output formats feature

    extension = ""

    def __init__(
        self,
        sub_reporters: List[BaseReporter],
        close_output_files: Callable[[], None],
        output: Optional[AnyFile] = None,
    ):
        self._sub_reporters = sub_reporters
        self.close_output_files = close_output_files

        self._path_strip_prefix = os.getcwd() + os.sep
        self._linter: Optional[PyLinter] = None

        self.set_output(output)

    def __del__(self):
        self.close_output_files()

    @property
    def path_strip_prefix(self) -> str:
        return self._path_strip_prefix

    @property
    def linter(self) -> Optional[PyLinter]:
        return self._linter

    @linter.setter
    def linter(self, value: PyLinter) -> None:
        self._linter = value
        for rep in self._sub_reporters:
            rep.linter = value

    def handle_message(self, msg: Message) -> None:
        """Handle a new message triggered on the current file."""
        for rep in self._sub_reporters:
            rep.handle_message(msg)

    # pylint: disable=no-self-use
    def set_output(self, output: Optional[AnyFile] = None) -> None:
        """set output stream"""
        # MultiReporter doesn't have it's own output. This method is only
        # provided for API parity with BaseReporter and should not be called
        # with non-None values for 'output'.
        if output is not None:
            raise NotImplementedError("MultiReporter does not support direct output.")

    def writeln(self, string: str = "") -> None:
        """write a line in the output buffer"""
        for rep in self._sub_reporters:
            rep.writeln(string)

    def display_reports(self, layout: BaseLayout) -> None:
        """display results encapsulated in the layout tree"""
        for rep in self._sub_reporters:
            rep.display_reports(layout)

    def display_messages(self, layout: BaseLayout) -> None:
        """hook for displaying the messages of the reporter"""
        for rep in self._sub_reporters:
            rep.display_messages(layout)

    def on_set_current_module(self, module: str, filepath: Optional[AnyPath]) -> None:
        """hook called when a module starts to be analysed"""
        for rep in self._sub_reporters:
            rep.on_set_current_module(module, filepath)

    def on_close(
        self,
        stats: Mapping[Any, Any],
        previous_stats: Mapping[Any, Any],
    ) -> None:
        """hook called when a module finished analyzing"""
        for rep in self._sub_reporters:
            rep.on_close(stats, previous_stats)
