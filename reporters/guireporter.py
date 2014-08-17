""" reporter used by gui.py """

import sys

from pylint.interfaces import IReporter
from pylint.reporters import BaseReporter
from pylint import utils
from logilab.common.ureports import TextWriter


class GUIReporter(BaseReporter):
    """saves messages"""

    __implements__ = IReporter
    extension = ''

    def __init__(self, gui, output=sys.stdout):
        """init"""
        BaseReporter.__init__(self, output)
        self.gui = gui

    def add_message(self, msg_id, location, msg):
        """manage message of different type and in the context of path"""
        message = utils.Message(msg_id, self.linter.msgs_store.check_message_id(msg_id).symbol, location, msg)
        self.gui.msg_queue.put(message)

    def _display(self, layout):
        """launch layouts display"""
        TextWriter().format(layout, self.out)
