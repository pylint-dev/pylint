# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

from io import StringIO
from os import getcwd, linesep, sep

from pylint import interfaces
from pylint.reporters import BaseReporter


class GenericTestReporter(BaseReporter):
    """reporter storing plain text messages"""

    __implements__ = interfaces.IReporter

    def __init__(self):  # pylint: disable=super-init-not-called

        self.message_ids = {}
        self.reset()
        self.path_strip_prefix = getcwd() + sep

    def reset(self):
        self.out = StringIO()
        self.messages = []

    def handle_message(self, msg):
        """manage message of different type and in the context of path"""
        obj = msg.obj
        line = msg.line
        msg_id = msg.msg_id
        msg = msg.msg
        self.message_ids[msg_id] = 1
        if obj:
            obj = ":%s" % obj
        sigle = msg_id[0]
        if linesep != "\n":
            # 2to3 writes os.linesep instead of using
            # the previously used line separators
            msg = msg.replace("\r\n", "\n")
        self.messages.append(f"{sigle}:{line:>3}{obj}: {msg}")

    def finalize(self):
        self.messages.sort()
        for msg in self.messages:
            print(msg, file=self.out)
        result = self.out.getvalue()
        self.reset()
        return result

    # pylint: disable=unused-argument
    def on_set_current_module(self, module, filepath):
        pass

    # pylint: enable=unused-argument

    def display_reports(self, layout):
        """ignore layouts"""

    _display = None


class MinimalTestReporter(BaseReporter):
    def handle_message(self, msg):
        self.messages.append(msg)

    def on_set_current_module(self, module, filepath):
        self.messages = []

    _display = None


class FunctionalTestReporter(BaseReporter):  # pylint: disable=abstract-method
    def handle_message(self, msg):
        self.messages.append(msg)

    def on_set_current_module(self, module, filepath):
        self.messages = []

    def display_reports(self, layout):
        """Ignore layouts and don't call self._display()."""
