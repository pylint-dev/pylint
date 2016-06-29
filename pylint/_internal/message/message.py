# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import collections
import sys
import textwrap

import six

from pylint.exceptions import UnknownMessageError, InvalidMessageDefinition
from pylint.interfaces import IRawChecker, ITokenChecker, implements
from .consts import MSG_TYPES, WarningScope


def _normalize_text(text, line_len=80, indent=''):
    """Wrap the text on the given line length."""
    return '\n'.join(textwrap.wrap(text, width=line_len, initial_indent=indent,
                                   subsequent_indent=indent))


def _checker_scope(checker):
    if implements(checker, (IRawChecker, ITokenChecker)):
        return WarningScope.LINE
    else:
        return WarningScope.NODE


_MsgBase = collections.namedtuple(
    '_MsgBase',
    ['msg_id', 'symbol', 'msg', 'C', 'category', 'confidence',
     'abspath', 'path', 'module', 'obj', 'line', 'column'])


class Message(_MsgBase):
    """This class represent a message to be issued by the reporters"""
    def __new__(cls, msg_id, symbol, location, msg, confidence):
        return _MsgBase.__new__(
            cls, msg_id, symbol, msg, msg_id[0], MSG_TYPES[msg_id[0]],
            confidence, *location)

    def format(self, template):
        """Format the message according to the given template.

        The template format is the one of the format method :
        cf. http://docs.python.org/2/library/string.html#formatstrings
        """
        # For some reason, _asdict on derived namedtuples does not work with
        # Python 3.4. Needs some investigation.
        return template.format(**dict(zip(self._fields, self)))


class MessageDefinition(object):
    def __init__(self, checker, msgid, msg, descr, symbol, scope,
                 minversion=None, maxversion=None, old_names=None):
        self.checker = checker
        assert len(msgid) == 5, 'Invalid message id %s' % msgid
        assert msgid[0] in MSG_TYPES, \
               'Bad message type %s in %r' % (msgid[0], msgid)
        self.msgid = msgid
        self.msg = msg
        self.descr = descr
        self.symbol = symbol
        self.scope = scope
        self.minversion = minversion
        self.maxversion = maxversion
        self.old_names = old_names or []

    def may_be_emitted(self):
        """return True if message may be emitted using the current interpreter"""
        if self.minversion is not None and self.minversion > sys.version_info:
            return False
        if self.maxversion is not None and self.maxversion <= sys.version_info:
            return False
        return True

    def format_help(self, checkerref=False):
        """return the help string for the given message id"""
        desc = self.descr
        if checkerref:
            desc += ' This message belongs to the %s checker.' % \
                   self.checker.name
        title = self.msg
        if self.symbol:
            msgid = '%s (%s)' % (self.symbol, self.msgid)
        else:
            msgid = self.msgid
        if self.minversion or self.maxversion:
            restr = []
            if self.minversion:
                restr.append('< %s' % '.'.join([str(n) for n in self.minversion]))
            if self.maxversion:
                restr.append('>= %s' % '.'.join([str(n) for n in self.maxversion]))
            restr = ' or '.join(restr)
            if checkerref:
                desc += " It can't be emitted when using Python %s." % restr
            else:
                desc += " This message can't be emitted when using Python %s." % restr
        desc = _normalize_text(' '.join(desc.split()), indent='  ')
        if title != '%s':
            title = title.splitlines()[0]
            return ':%s: *%s*\n%s' % (msgid, title, desc)
        return ':%s:\n%s' % (msgid, desc)

    @classmethod
    def from_message_def(cls, checker, msgid, msg_tuple):
        default_scope = _checker_scope(checker)
        options = {}
        if len(msg_tuple) > 3:
            (msg, symbol, descr, options) = msg_tuple
        elif len(msg_tuple) > 2:
            (msg, symbol, descr) = msg_tuple
        else:
            raise InvalidMessageDefinition("Message defined without a symbol.")

        options.setdefault('scope', default_scope)
        return cls(checker, msgid, msg, descr, symbol, **options)



class MessagesStore(object):
    """The messages store knows information about every possible message but has
    no particular state during analysis.
    """

    def __init__(self):
        # Primary registry for all active messages (i.e. all messages
        # that can be emitted by pylint for the underlying Python
        # version). It contains the 1:1 mapping from symbolic names
        # to message definition objects.
        self._messages = {}
        # Maps alternative names (numeric IDs, deprecated names) to
        # message definitions. May contain several names for each definition
        # object.
        self._alternative_names = {}
        self._msgs_by_category = collections.defaultdict(list)

    @property
    def messages(self):
        """The list of all active messages."""
        return six.itervalues(self._messages)

    def add_renamed_message(self, old_id, old_symbol, new_symbol):
        """Register the old ID and symbol for a warning that was renamed.

        This allows users to keep using the old ID/symbol in suppressions.
        """
        msg = self.check_message_id(new_symbol)
        msg.old_names.append((old_id, old_symbol))
        self._alternative_names[old_id] = msg
        self._alternative_names[old_symbol] = msg

    def register_messages(self, checker):
        """register a dictionary of messages

        Keys are message ids, values are a 2-uple with the message type and the
        message itself

        message ids should be a string of len 4, where the two first characters
        are the checker id and the two last the message id in this checker
        """
        chkid = None
        for msgid, msg_tuple in six.iteritems(checker.msgs):
            msg = MessageDefinition.from_message_def(checker, msgid, msg_tuple)
            assert msg.symbol not in self._messages, \
                    'Message symbol %r is already defined' % msg.symbol
            # avoid duplicate / malformed ids
            assert msg.msgid not in self._alternative_names, \
                   'Message id %r is already defined' % msgid
            assert chkid is None or chkid == msg.msgid[1:3], \
                   'Inconsistent checker part in message id %r' % msgid
            chkid = msg.msgid[1:3]
            self._messages[msg.symbol] = msg
            self._alternative_names[msg.msgid] = msg
            for old_id, old_symbol in msg.old_names:
                self._alternative_names[old_id] = msg
                self._alternative_names[old_symbol] = msg
            self._msgs_by_category[msg.msgid[0]].append(msg.msgid)

    def check_message_id(self, msgid):
        """returns the Message object for this message.

        msgid may be either a numeric or symbolic id.

        Raises UnknownMessageError if the message id is not defined.
        """
        if msgid[1:].isdigit():
            msgid = msgid.upper()
        for source in (self._alternative_names, self._messages):
            try:
                return source[msgid]
            except KeyError:
                pass
        raise UnknownMessageError('No such message id %s' % msgid)


def messages_help(message_store, msgids):
    """Display help messages for the given message identifiers"""
    for msgid in msgids:
        try:
            print(message_store.check_message_id(msgid).format_help(checkerref=True))
            print("")
        except UnknownMessageError as ex:
            print(ex)
            print("")
            continue


def list_messages(message_store):
    """output full messages list documentation in ReST format"""
    msgs = sorted(six.itervalues(message_store._messages), key=lambda msg: msg.msgid)
    for msg in msgs:
        if not msg.may_be_emitted():
            continue
        print(msg.format_help(checkerref=False))
    print("")
