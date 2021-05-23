# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE


import os

from pylint.interfaces import IReporter


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

    def __init__(self, sub_reporters, close_output_files, output=None):
        self._sub_reporters = sub_reporters
        self.close_output_files = close_output_files

        self._path_strip_prefix = os.getcwd() + os.sep
        self._linter = None

        self.set_output(output)

    def __del__(self):
        self.close_output_files()

    @property
    def path_strip_prefix(self):
        return self._path_strip_prefix

    @path_strip_prefix.setter
    def path_strip_prefix(self, value):
        self._path_strip_prefix = value
        for rep in self._sub_reporters:
            rep.path_strip_prefix = value

    @property
    def linter(self):
        return self._linter

    @linter.setter
    def linter(self, value):
        self._linter = value
        for rep in self._sub_reporters:
            rep.linter = value

    def handle_message(self, msg):
        """Handle a new message triggered on the current file."""
        for rep in self._sub_reporters:
            rep.handle_message(msg)

    # pylint: disable=no-self-use
    def set_output(self, output=None):
        """set output stream"""
        if output is not None:
            raise NotImplementedError("MultiReporter does not support direct output.")

    def writeln(self, string=""):
        """write a line in the output buffer"""
        for rep in self._sub_reporters:
            rep.writeln(string)

    def display_reports(self, layout):
        """display results encapsulated in the layout tree"""
        for rep in self._sub_reporters:
            rep.display_reports(layout)

    def display_messages(self, layout):
        """hook for displaying the messages of the reporter"""
        for rep in self._sub_reporters:
            rep.display_messages(layout)

    def on_set_current_module(self, module, filepath):
        """hook called when a module starts to be analysed"""
        for rep in self._sub_reporters:
            rep.on_set_current_module(module, filepath)

    def on_close(self, stats, previous_stats):
        """hook called when a module finished analyzing"""
        for rep in self._sub_reporters:
            rep.on_close(stats, previous_stats)
