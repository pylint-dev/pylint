# Copyright (c) 2003-2013 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""some various utilities and helper classes, most of them used in the
main pylint class
"""

import re
import sys
import tokenize
import os
from warnings import warn
from os.path import dirname, basename, splitext, exists, isdir, join, normpath

from logilab.common.interface import implements
from logilab.common.modutils import modpath_from_file, get_module_files, \
                                    file_from_modpath, load_module_from_file
from logilab.common.textutils import normalize_text
from logilab.common.configuration import rest_format_section
from logilab.common.ureports import Section

from astroid import nodes, Module

from pylint.interfaces import IRawChecker, ITokenChecker


class UnknownMessage(Exception):
    """raised when a unregistered message id is encountered"""

class EmptyReport(Exception):
    """raised when a report is empty and so should not be displayed"""


MSG_TYPES = {
    'I' : 'info',
    'C' : 'convention',
    'R' : 'refactor',
    'W' : 'warning',
    'E' : 'error',
    'F' : 'fatal'
    }
MSG_TYPES_LONG = dict([(v, k) for k, v in MSG_TYPES.iteritems()])

MSG_TYPES_STATUS = {
    'I' : 0,
    'C' : 16,
    'R' : 8,
    'W' : 4,
    'E' : 2,
    'F' : 1
    }

_MSG_ORDER = 'EWRCIF'
MSG_STATE_SCOPE_CONFIG = 0
MSG_STATE_SCOPE_MODULE = 1

OPTION_RGX = re.compile(r'\s*#.*\bpylint:(.*)')

# The line/node distinction does not apply to fatal errors and reports.
_SCOPE_EXEMPT = 'FR'

class WarningScope(object):
    LINE = 'line-based-msg'
    NODE = 'node-based-msg'


def get_module_and_frameid(node):
    """return the module name and the frame id in the module"""
    frame = node.frame()
    module, obj = '', []
    while frame:
        if isinstance(frame, Module):
            module = frame.name
        else:
            obj.append(getattr(frame, 'name', '<lambda>'))
        try:
            frame = frame.parent.frame()
        except AttributeError:
            frame = None
    obj.reverse()
    return module, '.'.join(obj)

def category_id(id):
    id = id.upper()
    if id in MSG_TYPES:
        return id
    return MSG_TYPES_LONG.get(id)


def tokenize_module(module):
    stream = module.file_stream
    stream.seek(0)
    readline = stream.readline
    if sys.version_info < (3, 0):
        if module.file_encoding is not None:
            readline = lambda: stream.readline().decode(module.file_encoding,
                                                    'replace')
        return list(tokenize.generate_tokens(readline))
    return list(tokenize.tokenize(readline))

def build_message_def(checker, msgid, msg_tuple):
    if implements(checker, (IRawChecker, ITokenChecker)):
        default_scope = WarningScope.LINE
    else:
        default_scope = WarningScope.NODE
    options = {}
    if len(msg_tuple) > 3:
        (msg, symbol, descr, options) = msg_tuple
    elif len(msg_tuple) > 2:
        (msg, symbol, descr) = msg_tuple[:3]
    else:
        # messages should have a symbol, but for backward compatibility
        # they may not.
        (msg, descr) = msg_tuple
        warn("[pylint 0.26] description of message %s doesn't include "
             "a symbolic name" % msgid, DeprecationWarning)
        symbol = None
    options.setdefault('scope', default_scope)
    return MessageDefinition(checker, msgid, msg, descr, symbol, **options)


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
        desc = normalize_text(' '.join(desc.split()), indent='  ')
        if title != '%s':
            title = title.splitlines()[0]
            return ':%s: *%s*\n%s' % (msgid, title, desc)
        return ':%s:\n%s' % (msgid, desc)


class MessagesHandlerMixIn(object):
    """a mix-in class containing all the messages related methods for the main
    lint class
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
        self._msgs_state = {}
        self._module_msgs_state = {} # None
        self._raw_module_msgs_state = {}
        self._msgs_by_category = {}
        self.msg_status = 0
        self._ignored_msgs = {}
        self._suppression_mapping = {}

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
        for msgid, msg_tuple in checker.msgs.iteritems():
            msg = build_message_def(checker, msgid, msg_tuple)
            assert msg.symbol not in self._messages, \
                    'Message symbol %r is already defined' % msg.symbol
            # avoid duplicate / malformed ids
            assert msg.msgid not in self._alternative_names, \
                   'Message id %r is already defined' % msgid
            assert chkid is None or chkid == msg.msgid[1:3], \
                   'Inconsistent checker part in message id %r' % msgid
            chkid = msg.msgid[1:3]
            if not msg.may_be_emitted():
                self._msgs_state[msg.msgid] = False
            self._messages[msg.symbol] = msg
            self._alternative_names[msg.msgid] = msg
            for old_id, old_symbol in msg.old_names:
                self._alternative_names[old_id] = msg
                self._alternative_names[old_symbol] = msg
            self._msgs_by_category.setdefault(msg.msgid[0], []).append(msg.msgid)

    def disable(self, msgid, scope='package', line=None, ignore_unknown=False):
        """don't output message of the given id"""
        assert scope in ('package', 'module')
        # handle disable=all by disabling all categories
        if msgid == 'all':
            for msgid in MSG_TYPES:
                self.disable(msgid, scope, line)
            return
        # msgid is a category?
        catid = category_id(msgid)
        if catid is not None:
            for _msgid in self._msgs_by_category.get(catid):
                self.disable(_msgid, scope, line)
            return
        # msgid is a checker name?
        if msgid.lower() in self._checkers:
            for checker in self._checkers[msgid.lower()]:
                for _msgid in checker.msgs:
                    if _msgid in self._alternative_names:
                        self.disable(_msgid, scope, line)
            return
        # msgid is report id?
        if msgid.lower().startswith('rp'):
            self.disable_report(msgid)
            return

        try:
            # msgid is a symbolic or numeric msgid.
            msg = self.check_message_id(msgid)
        except UnknownMessage:
            if ignore_unknown:
                return
            raise

        if scope == 'module':
            assert line > 0
            try:
                self._module_msgs_state[msg.msgid][line] = False
            except KeyError:
                self._module_msgs_state[msg.msgid] = {line: False}
                if msg.symbol != 'locally-disabled':
                    self.add_message('locally-disabled', line=line, 
                                     args=(msg.symbol, msg.msgid))

        else:
            msgs = self._msgs_state
            msgs[msg.msgid] = False
            # sync configuration object
            self.config.disable_msg = [mid for mid, val in msgs.iteritems()
                                       if not val]

    def enable(self, msgid, scope='package', line=None, ignore_unknown=False):
        """reenable message of the given id"""
        assert scope in ('package', 'module')
        catid = category_id(msgid)
        # msgid is a category?
        if catid is not None:
            for msgid in self._msgs_by_category.get(catid):
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
            msg = self.check_message_id(msgid)
        except UnknownMessage:
            if ignore_unknown:
                return
            raise

        if scope == 'module':
            assert line > 0
            try:
                self._module_msgs_state[msg.msgid][line] = True
            except KeyError:
                self._module_msgs_state[msg.msgid] = {line: True}
                self.add_message('locally-enabled', line=line, args=(msg.symbol, msg.msgid))
        else:
            msgs = self._msgs_state
            msgs[msg.msgid] = True
            # sync configuration object
            self.config.enable = [mid for mid, val in msgs.iteritems() if val]

    def check_message_id(self, msgid):
        """returns the Message object for this message.

        msgid may be either a numeric or symbolic id.

        Raises UnknownMessage if the message id is not defined.
        """
        if msgid[1:].isdigit():
            msgid = msgid.upper()
        for source in (self._alternative_names, self._messages):
            try:
                return source[msgid]
            except KeyError:
                pass
        raise UnknownMessage('No such message id %s' % msgid)

    def get_msg_display_string(self, msgid):
        """Generates a user-consumable representation of a message.

        Can be just the message ID or the ID and the symbol.
        """
        return repr(self.check_message_id(msgid).symbol)

    def get_message_state_scope(self, msgid, line=None):
        """Returns the scope at which a message was enabled/disabled."""
        try:
            if line in self._module_msgs_state[msgid]:
                return MSG_STATE_SCOPE_MODULE
        except (KeyError, TypeError):
            return MSG_STATE_SCOPE_CONFIG

    def is_message_enabled(self, msg_descr, line=None):
        """return true if the message associated to the given message id is
        enabled

        msgid may be either a numeric or symbolic message id.
        """
        try:
            msgid = self.check_message_id(msg_descr).msgid
        except UnknownMessage:
            # The linter checks for messages that are not registered
            # due to version mismatch, just treat them as message IDs
            # for now.
            msgid = msg_descr
        if line is None:
            return self._msgs_state.get(msgid, True)
        try:
            return self._module_msgs_state[msgid][line]
        except (KeyError, TypeError):
            return self._msgs_state.get(msgid, True)

    def handle_ignored_message(self, state_scope, msgid, line, node, args):
        """Report an ignored message.

        state_scope is either MSG_STATE_SCOPE_MODULE or MSG_STATE_SCOPE_CONFIG,
        depending on whether the message was disabled locally in the module,
        or globally. The other arguments are the same as for add_message.
        """
        if state_scope == MSG_STATE_SCOPE_MODULE:
            try:
                orig_line = self._suppression_mapping[(msgid, line)]
                self._ignored_msgs.setdefault((msgid, orig_line), set()).add(line)
            except KeyError:
                pass

    def add_message(self, msg_descr, line=None, node=None, args=None):
        """Adds a message given by ID or name.

        If provided, the message string is expanded using args

        AST checkers should must the node argument (but may optionally
        provide line if the line number is different), raw and token checkers
        must provide the line argument.
        """
        msg_info = self.check_message_id(msg_descr)
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
        if not self.is_message_enabled(msgid, line):
            self.handle_ignored_message(
                self.get_message_state_scope(msgid, line), msgid, line, node, args)
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
            path = self.current_file
        else:
            module, obj = get_module_and_frameid(node)
            path = node.root().file
        # add the message
        self.reporter.add_message(msgid, (path, module, obj, line or 1, col_offset or 0), msg)

    def help_message(self, msgids):
        """display help messages for the given message identifiers"""
        for msgid in msgids:
            try:
                print self.check_message_id(msgid).format_help(checkerref=True)
                print
            except UnknownMessage, ex:
                print ex
                print
                continue

    def print_full_documentation(self):
        """output a full documentation in ReST format"""
        by_checker = {}
        for checker in self.get_checkers():
            if checker.name == 'master':
                prefix = 'Main '
                print "Options"
                print '-------\n'
                if checker.options:
                    for section, options in checker.options_by_section():
                        if section is None:
                            title = 'General options'
                        else:
                            title = '%s options' % section.capitalize()
                        print title
                        print '~' * len(title)
                        rest_format_section(sys.stdout, None, options)
                        print
            else:
                try:
                    by_checker[checker.name][0] += checker.options_and_values()
                    by_checker[checker.name][1].update(checker.msgs)
                    by_checker[checker.name][2] += checker.reports
                except KeyError:
                    by_checker[checker.name] = [list(checker.options_and_values()),
                                                dict(checker.msgs),
                                                list(checker.reports)]
        for checker, (options, msgs, reports) in by_checker.iteritems():
            prefix = ''
            title = '%s checker' % checker
            print title
            print '-' * len(title)
            print
            if options:
                title = 'Options'
                print title
                print '~' * len(title)
                rest_format_section(sys.stdout, None, options)
                print
            if msgs:
                title = ('%smessages' % prefix).capitalize()
                print title
                print '~' * len(title)
                for msgid, msg in sorted(msgs.iteritems(),
                                         key=lambda (k, v): (_MSG_ORDER.index(k[0]), k)):
                    msg = build_message_def(checker, msgid, msg)
                    print msg.format_help(checkerref=False)
                print
            if reports:
                title = ('%sreports' % prefix).capitalize()
                print title
                print '~' * len(title)
                for report in reports:
                    print ':%s: %s' % report[:2]
                print
            print

    @property
    def messages(self):
        """The list of all active messages."""
        return self._messages.itervalues()

    def list_messages(self):
        """output full messages list documentation in ReST format"""
        msgs = sorted(self._messages.itervalues(), key=lambda msg: msg.msgid)
        for msg in msgs:
            if not msg.may_be_emitted():
                continue
            print msg.format_help(checkerref=False)
        print


class ReportsHandlerMixIn(object):
    """a mix-in class containing all the reports and stats manipulation
    related methods for the main lint class
    """
    def __init__(self):
        self._reports = {}
        self._reports_state = {}

    def register_report(self, reportid, r_title, r_cb, checker):
        """register a report

        reportid is the unique identifier for the report
        r_title the report's title
        r_cb the method to call to make the report
        checker is the checker defining the report
        """
        reportid = reportid.upper()
        self._reports.setdefault(checker, []).append((reportid, r_title, r_cb))

    def enable_report(self, reportid):
        """disable the report of the given id"""
        reportid = reportid.upper()
        self._reports_state[reportid] = True

    def disable_report(self, reportid):
        """disable the report of the given id"""
        reportid = reportid.upper()
        self._reports_state[reportid] = False

    def report_is_enabled(self, reportid):
        """return true if the report associated to the given identifier is
        enabled
        """
        return self._reports_state.get(reportid, True)

    def make_reports(self, stats, old_stats):
        """render registered reports"""
        sect = Section('Report',
                       '%s statements analysed.'% (self.stats['statement']))
        for checker in self._reports:
            for reportid, r_title, r_cb in self._reports[checker]:
                if not self.report_is_enabled(reportid):
                    continue
                report_sect = Section(r_title)
                try:
                    r_cb(report_sect, stats, old_stats)
                except EmptyReport:
                    continue
                report_sect.report_id = reportid
                sect.append(report_sect)
        return sect

    def add_stats(self, **kwargs):
        """add some stats entries to the statistic dictionary
        raise an AssertionError if there is a key conflict
        """
        for key, value in kwargs.iteritems():
            if key[-1] == '_':
                key = key[:-1]
            assert key not in self.stats
            self.stats[key] = value
        return self.stats


def expand_modules(files_or_modules, black_list):
    """take a list of files/modules/packages and return the list of tuple
    (file, module name) which have to be actually checked
    """
    result = []
    errors = []
    for something in files_or_modules:
        if exists(something):
            # this is a file or a directory
            try:
                modname = '.'.join(modpath_from_file(something))
            except ImportError:
                modname = splitext(basename(something))[0]
            if isdir(something):
                filepath = join(something, '__init__.py')
            else:
                filepath = something
        else:
            # suppose it's a module or package
            modname = something
            try:
                filepath = file_from_modpath(modname.split('.'))
                if filepath is None:
                    errors.append({'key' : 'ignored-builtin-module', 'mod': modname})
                    continue
            except (ImportError, SyntaxError), ex:
                # FIXME p3k : the SyntaxError is a Python bug and should be
                # removed as soon as possible http://bugs.python.org/issue10588
                errors.append({'key': 'fatal', 'mod': modname, 'ex': ex})
                continue
        filepath = normpath(filepath)
        result.append({'path': filepath, 'name': modname, 'isarg': True,
                       'basepath': filepath, 'basename': modname})
        if not (modname.endswith('.__init__') or modname == '__init__') \
                and '__init__.py' in filepath:
            for subfilepath in get_module_files(dirname(filepath), black_list):
                if filepath == subfilepath:
                    continue
                submodname = '.'.join(modpath_from_file(subfilepath))
                result.append({'path': subfilepath, 'name': submodname,
                               'isarg': False,
                               'basepath': filepath, 'basename': modname})
    return result, errors


class PyLintASTWalker(object):

    def __init__(self, linter):
        # callbacks per node types
        self.nbstatements = 1
        self.visit_events = {}
        self.leave_events = {}
        self.linter = linter

    def _is_method_enabled(self, method):
        if not hasattr(method, 'checks_msgs'):
            return True
        for msg_desc in method.checks_msgs:
            if self.linter.is_message_enabled(msg_desc):
                return True
        return False

    def add_checker(self, checker):
        """walk to the checker's dir and collect visit and leave methods"""
        # XXX : should be possible to merge needed_checkers and add_checker
        vcids = set()
        lcids = set()
        visits = self.visit_events
        leaves = self.leave_events
        for member in dir(checker):
            cid = member[6:]
            if cid == 'default':
                continue
            if member.startswith('visit_'):
                v_meth = getattr(checker, member)
                # don't use visit_methods with no activated message:
                if self._is_method_enabled(v_meth):
                    visits.setdefault(cid, []).append(v_meth)
                    vcids.add(cid)
            elif member.startswith('leave_'):
                l_meth = getattr(checker, member)
                # don't use leave_methods with no activated message:
                if self._is_method_enabled(l_meth):
                    leaves.setdefault(cid, []).append(l_meth)
                    lcids.add(cid)
        visit_default = getattr(checker, 'visit_default', None)
        if visit_default:
            for cls in nodes.ALL_NODE_CLASSES:
                cid = cls.__name__.lower()
                if cid not in vcids:
                    visits.setdefault(cid, []).append(visit_default)
        # for now we have no "leave_default" method in Pylint

    def walk(self, astroid):
        """call visit events of astroid checkers for the given node, recurse on
        its children, then leave events.
        """
        cid = astroid.__class__.__name__.lower()
        if astroid.is_statement:
            self.nbstatements += 1
        # generate events for this node on each checker
        for cb in self.visit_events.get(cid, ()):
            cb(astroid)
        # recurse on children
        for child in astroid.get_children():
            self.walk(child)
        for cb in self.leave_events.get(cid, ()):
            cb(astroid)


PY_EXTS = ('.py', '.pyc', '.pyo', '.pyw', '.so', '.dll')

def register_plugins(linter, directory):
    """load all module and package in the given directory, looking for a
    'register' function in each one, used to register pylint checkers
    """
    imported = {}
    for filename in os.listdir(directory):
        base, extension = splitext(filename)
        if base in imported or base == '__pycache__':
            continue
        if extension in PY_EXTS and base != '__init__' or (
             not extension and isdir(join(directory, base))):
            try:
                module = load_module_from_file(join(directory, filename))
            except ValueError:
                # empty module name (usually emacs auto-save files)
                continue
            except ImportError, exc:
                print >> sys.stderr, "Problem importing module %s: %s" % (filename, exc)
            else:
                if hasattr(module, 'register'):
                    module.register(linter)
                    imported[base] = 1

