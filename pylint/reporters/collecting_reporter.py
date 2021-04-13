# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

from pylint.reporters.base_reporter import BaseReporter


class CollectingReporter(BaseReporter):
    """collects messages"""

    name = "collector"

    def __init__(self):
        BaseReporter.__init__(self)
        self.messages = []

    def handle_message(self, msg):
        self.messages.append(msg)

    def reset(self):
        self.messages = []

    _display = None
