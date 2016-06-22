# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

from __future__ import print_function

import six

import astroid
from pylint.exceptions import UnknownMessageError
from pylint.interfaces import UNDEFINED
from .consts import (
    MSG_TYPES,
    MSG_TYPES_LONG,
    MSG_STATE_CONFIDENCE,
    MSG_STATE_SCOPE_MODULE,
    MSG_STATE_SCOPE_CONFIG,
    WarningScope,
)
from .message import Message


# The line/node distinction does not apply to fatal errors and reports.
_SCOPE_EXEMPT = 'FR'
MSG_TYPES_STATUS = {
    'I' : 0,
    'C' : 16,
    'R' : 8,
    'W' : 4,
    'E' : 2,
    'F' : 1
    }


class MessagesHandlerMixin(object):
    """a mix-in class containing all the messages related methods for the main
    lint class
    """

    def __init__(self):
        self._msgs_state = {}
        self.msg_status = 0

    def _checker_messages(self, checker):
        for checker in self._checkers[checker.lower()]:
            for msgid in checker.msgs:
                yield msgid

    def disable(self, msgid, scope='package', line=None, ignore_unknown=False):
        """don't output message of the given id"""
        assert scope in ('package', 'module')
        # handle disable=all by disabling all categories
        if msgid == 'all':
            for msgid in MSG_TYPES:
                self.disable(msgid, scope, line)
            return
        # msgid is a category?
        catid = _category_id(msgid)
        if catid is not None:
            for _msgid in self.msgs_store._msgs_by_category.get(catid):
                self.disable(_msgid, scope, line)
            return
        # msgid is a checker name?
        if msgid.lower() in self._checkers:
            msgs_store = self.msgs_store
            for checker in self._checkers[msgid.lower()]:
                for _msgid in checker.msgs:
                    if _msgid in msgs_store._alternative_names:
                        self.disable(_msgid, scope, line)
            return
        # msgid is report id?
        if msgid.lower().startswith('rp'):
            self.disable_report(msgid)
            return

        try:
            # msgid is a symbolic or numeric msgid.
            msg = self.msgs_store.check_message_id(msgid)
        except UnknownMessageError:
            if ignore_unknown:
                return
            raise

        if scope == 'module':
            self.file_state.set_msg_status(msg, line, False)
            if msg.symbol != 'locally-disabled':
                self.add_message('locally-disabled', line=line,
                                 args=(msg.symbol, msg.msgid))

        else:
            msgs = self._msgs_state
            msgs[msg.msgid] = False
            # sync configuration object
            self.config.disable = [self._message_symbol(mid)
                                   for mid, val in six.iteritems(msgs)
                                   if not val]

    def _message_symbol(self, msgid):
        """Get the message symbol of the given message id

        Return the original message id if the message does not
        exist.
        """
        try:
            return self.msgs_store.check_message_id(msgid).symbol
        except UnknownMessageError:
            return msgid

    def enable(self, msgid, scope='package', line=None, ignore_unknown=False):
        """reenable message of the given id"""
        assert scope in ('package', 'module')
        if msgid == 'all':
            for msgid_ in MSG_TYPES:
                self.enable(msgid_, scope=scope, line=line)
            if not self._python3_porting_mode:
                # Don't activate the python 3 porting checker if it
                # wasn't activated explicitly.
                self.disable('python3')
            return
        catid = _category_id(msgid)
        # msgid is a category?
        if catid is not None:
            for msgid in self.msgs_store._msgs_by_category.get(catid):
                self.enable(msgid, scope, line)
            return
        # msgid is a checker name?
        if msgid.lower() in self._checkers:
            for checker in self._checkers[msgid.lower()]:
                for msgid_ in checker.msgs:
                    self.enable(msgid_, scope, line)
            return
        # msgid is report id?
        if msgid.lower().startswith('rp'):
            self.enable_report(msgid)
            return

        try:
            # msgid is a symbolic or numeric msgid.
            msg = self.msgs_store.check_message_id(msgid)
        except UnknownMessageError:
            if ignore_unknown:
                return
            raise

        if scope == 'module':
            self.file_state.set_msg_status(msg, line, True)
            self.add_message('locally-enabled', line=line, args=(msg.symbol, msg.msgid))
        else:
            msgs = self._msgs_state
            msgs[msg.msgid] = True
            # sync configuration object
            self.config.enable = [mid for mid, val in six.iteritems(msgs) if val]

    def get_message_state_scope(self, msgid, line=None, confidence=UNDEFINED):
        """Returns the scope at which a message was enabled/disabled."""
        if self.config.confidence and confidence.name not in self.config.confidence:
            return MSG_STATE_CONFIDENCE
        try:
            if line in self.file_state._module_msgs_state[msgid]:
                return MSG_STATE_SCOPE_MODULE
        except (KeyError, TypeError):
            return MSG_STATE_SCOPE_CONFIG

    def is_message_enabled(self, msg_descr, line=None, confidence=None):
        """return true if the message associated to the given message id is
        enabled

        msgid may be either a numeric or symbolic message id.
        """
        if self.config.confidence and confidence:
            if confidence.name not in self.config.confidence:
                return False
        try:
            msgid = self.msgs_store.check_message_id(msg_descr).msgid
        except UnknownMessageError:
            # The linter checks for messages that are not registered
            # due to version mismatch, just treat them as message IDs
            # for now.
            msgid = msg_descr
        if line is None:
            return self._msgs_state.get(msgid, True)
        try:
            return self.file_state._module_msgs_state[msgid][line]
        except KeyError:
            return self._msgs_state.get(msgid, True)

    def add_message(self, msg_descr, line=None, node=None, args=None, confidence=UNDEFINED):
        """Adds a message given by ID or name.

        If provided, the message string is expanded using args

        AST checkers should must the node argument (but may optionally
        provide line if the line number is different), raw and token checkers
        must provide the line argument.
        """
        msg_info = self.msgs_store.check_message_id(msg_descr)
        msgid = msg_info.msgid
        # backward compatibility, message may not have a symbol
        symbol = msg_info.symbol or msgid
        # Fatal messages and reports are special, the node/scope distinction
        # does not apply to them.
        if msgid[0] not in _SCOPE_EXEMPT:
            if msg_info.scope == WarningScope.LINE:
                assert node is None and line is not None, (
                    'Message %s must only provide line, got line=%s, node=%s' % (msgid, line, node))
            elif msg_info.scope == WarningScope.NODE:
                # Node-based warnings may provide an override line.
                assert node is not None, 'Message %s must provide Node, got None'

        if line is None and node is not None:
            line = node.fromlineno
        if hasattr(node, 'col_offset'):
            col_offset = node.col_offset # XXX measured in bytes for utf-8, divide by two for chars?
        else:
            col_offset = None
        # should this message be displayed
        if not self.is_message_enabled(msgid, line, confidence):
            self.file_state.handle_ignored_message(
                self.get_message_state_scope(msgid, line, confidence),
                msgid, line, node, args, confidence)
            return
        # update stats
        msg_cat = MSG_TYPES[msgid[0]]
        self.msg_status |= MSG_TYPES_STATUS[msgid[0]]
        self.stats[msg_cat] += 1
        self.stats['by_module'][self.current_name][msg_cat] += 1
        try:
            self.stats['by_msg'][symbol] += 1
        except KeyError:
            self.stats['by_msg'][symbol] = 1
        # expand message ?
        msg = msg_info.msg
        if args:
            msg %= args
        # get module and object
        if node is None:
            module, obj = self.current_name, ''
            abspath = self.current_file
        else:
            module, obj = _module_and_frameid(node)
            abspath = node.root().file
        path = abspath.replace(self.reporter.path_strip_prefix, '')
        # add the message
        self.reporter.handle_message(
            Message(msgid, symbol,
                    (abspath, path, module, obj, line or 1, col_offset or 0), msg, confidence))


def _category_id(cid):
    cid = cid.upper()
    if cid in MSG_TYPES:
        return cid
    return MSG_TYPES_LONG.get(cid)


def _module_and_frameid(node):
    """return the module name and the frame id in the module"""
    frame = node.frame()
    module, obj = '', []
    while frame:
        if isinstance(frame, astroid.Module):
            module = frame.name
        else:
            obj.append(getattr(frame, 'name', '<lambda>'))
        try:
            frame = frame.parent.frame()
        except AttributeError:
            frame = None
    obj.reverse()
    return module, '.'.join(obj)
