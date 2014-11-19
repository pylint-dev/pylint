""" reporter used by gui.py """

import sys

from pylint.interfaces import IReporter
from pylint.reporters import BaseReporter
from logilab.common.ureports import TextWriter


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
