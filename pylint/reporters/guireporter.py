# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

""" reporter used by gui.py """

import sys

from pylint.interfaces import IReporter
from pylint.reporters import BaseReporter
from pylint.reporters.ureports.text_writer import TextWriter


class GUIReporter(BaseReporter):
    """saves messages"""

    __implements__ = IReporter
    extension = ''

    def __init__(self, gui, output=sys.stdout):
        """init"""
        BaseReporter.__init__(self, output)
        self.gui = gui

    def handle_message(self, msg):
        """manage message of different type and in the context of path"""
        self.gui.msg_queue.put(msg)

    def _display(self, layout):
        """launch layouts display"""
        TextWriter().format(layout, self.out)
