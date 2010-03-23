# Copyright (c) 2003-2010 Sylvain Thenault (thenault@gmail.com).
# Copyright (c) 2003-2010 LOGILAB S.A. (Paris, FRANCE).
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
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""some various utilities and helper classes, most of them used in the
main pylint class
"""

import sys
from os import linesep

from logilab.common.textutils import normalize_text
from logilab.common.configuration import rest_format_section
from logilab.common.ureports import Section

from logilab.astng import Module

from pylint.checkers import EmptyReport

class UnknownMessage(Exception):
    """raised when a unregistered message id is encountered"""


MSG_TYPES = {
    'I' : 'info',
    'C' : 'convention',
    'R' : 'refactor',
    'W' : 'warning',
    'E' : 'error',
    'F' : 'fatal'
    }
MSG_TYPES_STATUS = {
    'I' : 0,
    'C' : 16,
    'R' : 8,
    'W' : 4,
    'E' : 2,
    'F' : 1
    }

def sort_checkers(checkers):
    """return a list of enabled checker sorted by priority"""
    checkers = [checker for checker in checkers if checker.is_enabled()]
    checkers.sort(lambda x, y: cmp(-x.priority, -y.priority) )
    return checkers

def sort_msgs(msg_ids):
    """sort message identifiers according to their category first"""
    msg_order = 'EWRCIF'
    def cmp_func(msgid1, msgid2):
        """comparison function for two message identifiers"""
        if msgid1[0] != msgid2[0]:
            return cmp(msg_order.index(msgid1[0]), msg_order.index(msgid2[0]))
        else:
            return cmp(msgid1, msgid2)
    msg_ids.sort(cmp_func)
    return msg_ids

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


class Message:
    def __init__(self, checker, msgid, msg, descr):
        assert len(msgid) == 5, 'Invalid message id %s' % msgid
        assert msgid[0] in MSG_TYPES, \
               'Bad message type %s in %r' % (msgid[0], msgid)
        self.msgid = msgid
        self.msg = msg
        self.descr = descr
        self.checker = checker

class MessagesHandlerMixIn:
    """a mix-in class containing all the messages related methods for the main
    lint class
    """

    def __init__(self):
        # dictionary of registered messages
        self._messages = {}
        self._msgs_state = {}
        self._module_msgs_state = {} # None
        self._msg_cats_state = {}
        self._module_msg_cats_state = None
        self.msg_status = 0

    def register_messages(self, checker):
        """register a dictionary of messages

        Keys are message ids, values are a 2-uple with the message type and the
        message itself

        message ids should be a string of len 4, where the to first characters
        are the checker id and the two last the message id in this checker
        """
        msgs_dict = checker.msgs
        chkid = None
        for msgid, (msg, msgdescr) in msgs_dict.items():
            # avoid duplicate / malformed ids
            assert not self._messages.has_key(msgid), \
                   'Message id %r is already defined' % msgid
            assert chkid is None or chkid == msgid[1:3], \
                   'Inconsistent checker part in message id %r' % msgid
            chkid = msgid[1:3]
            self._messages[msgid] = Message(checker, msgid, msg, msgdescr)

    def get_message_help(self, msg_id, checkerref=False):
        """return the help string for the given message id"""
        msg = self.check_message_id(msg_id)
        desc = normalize_text(' '.join(msg.descr.split()), indent='  ')
        if checkerref:
            desc += ' This message belongs to the %s checker.' % \
                   msg.checker.name
        title = msg.msg
        if title != '%s':
            title = title.splitlines()[0]
            return ':%s: *%s*\n%s' % (msg.msgid, title, desc)
        return ':%s:\n%s' % (msg.msgid, desc)

    def disable_message(self, msg_id, scope='package', line=None):
        """don't output message of the given id"""
        assert scope in ('package', 'module')
        msg = self.check_message_id(msg_id)
        if scope == 'module':
            assert line > 0
            try:
                self._module_msgs_state[msg.msgid][line] = False
            except KeyError:
                self._module_msgs_state[msg.msgid] = {line: False}
                if msg_id != 'I0011':
                    self.add_message('I0011', line=line, args=msg.msgid)

        else:
            msgs = self._msgs_state
            msgs[msg.msgid] = False
            # sync configuration object
            self.config.disable_msg = [mid for mid, val in msgs.items()
                                       if not val]

    def enable_message(self, msg_id, scope='package', line=None):
        """reenable message of the given id"""
        assert scope in ('package', 'module')
        msg = self.check_message_id(msg_id)
        msg.checker.enabled = True # ensure the related checker is enabled
        if scope == 'module':
            assert line > 0
            try:
                self._module_msgs_state[msg.msgid][line] = True
            except KeyError:
                self._module_msgs_state[msg.msgid] = {line: True}
                self.add_message('I0012', line=line, args=msg.msgid)
        else:
            msgs = self._msgs_state
            msgs[msg.msgid] = True
            # sync configuration object
            self.config.enable_msg = [mid for mid, val in msgs.items() if val]

    def _cat_ids(self, categories):
        for catid in categories:
            catid = catid.upper()
            if not catid in MSG_TYPES:
                raise Exception('Unknown category identifier %s' % catid)
            yield catid

    def disable_message_category(self, categories, scope='package', line=None):
        """don't output message in the given category"""
        assert scope in ('package', 'module')
        for catid in self._cat_ids(categories):
            if scope == 'module':
                self.add_message('I0011', line=line, args=catid)
                self._module_msg_cats_state[catid] = False
            else:
                self._msg_cats_state[catid] = False

    def enable_message_category(self, categories, scope='package', line=None):
        """reenable message of the given category"""
        assert scope in ('package', 'module')
        for catid in self._cat_ids(categories):
            if scope == 'module':
                self.add_message('I0012', line=line, args=catid)
                self._module_msg_cats_state[catid] = True
            else:
                self._msg_cats_state[catid] = True

    def check_message_id(self, msg_id):
        """raise UnknownMessage if the message id is not defined"""
        msg_id = msg_id.upper()
        try:
            return self._messages[msg_id]
        except KeyError:
            raise UnknownMessage('No such message id %s' % msg_id)

    def is_message_enabled(self, msg_id, line=None):
        """return true if the message associated to the given message id is
        enabled
        """
        try:
            if not self._module_msg_cats_state[msg_id[0]]:
                return False
        except (KeyError, TypeError):
            if not self._msg_cats_state.get(msg_id[0], True):
                return False
        if line is None:
            return self._msgs_state.get(msg_id, True)
        try:
            return self._module_msgs_state[msg_id][line]
        except (KeyError, TypeError):
            return self._msgs_state.get(msg_id, True)

    def add_message(self, msg_id, line=None, node=None, args=None):
        """add the message corresponding to the given id.

        If provided, msg is expanded using args

        astng checkers should provide the node argument, raw checkers should
        provide the line argument.
        """
        if line is None and node is not None:
            line = node.fromlineno
        # should this message be displayed
        if not self.is_message_enabled(msg_id, line):
            return
        # update stats
        msg_cat = MSG_TYPES[msg_id[0]]
        self.msg_status |= MSG_TYPES_STATUS[msg_id[0]]
        self.stats[msg_cat] += 1
        self.stats['by_module'][self.current_name][msg_cat] += 1
        try:
            self.stats['by_msg'][msg_id] += 1
        except KeyError:
            self.stats['by_msg'][msg_id] = 1
        msg = self._messages[msg_id].msg
        # expand message ?
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
        self.reporter.add_message(msg_id, (path, module, obj, line or 1), msg)

    def help_message(self, msgids):
        """display help messages for the given message identifiers"""
        for msg_id in msgids:
            try:
                print self.get_message_help(msg_id, True)
                print
            except UnknownMessage, ex:
                print ex
                print
                continue

    def list_checkers_messages(self, checker):
        """print checker's messages in reST format"""
        for msg_id in sort_msgs(checker.msgs.keys()):
            print self.get_message_help(msg_id, False)

    def print_full_documentation(self):
        """output a full documentation in ReST format"""
        for checker in sort_checkers(self._checkers.values()):
            if checker.name == 'master':
                prefix = 'Main '
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
                prefix = ''
                title = '%s checker' % checker.name.capitalize()
                print title
                print '-' * len(title)
                if checker.__doc__: # __doc__ is None with -OO
                    print linesep.join([l.strip()
                                        for l in checker.__doc__.splitlines()])
                if checker.options:
                    title = 'Options'
                    print title
                    print '~' * len(title)
                    for section, options in checker.options_by_section():
                        rest_format_section(sys.stdout, section, options)
                        print
            if checker.msgs:
                title = ('%smessages' % prefix).capitalize()
                print title
                print '~' * len(title)
                self.list_checkers_messages( checker)
                print
            if getattr(checker, 'reports', None):
                title = ('%sreports' % prefix).capitalize()
                print title
                print '~' * len(title)
                for report in checker.reports:
                    print ':%s: %s' % report[:2]
                print
            print

    def list_messages(self):
        """output full messages list documentation in ReST format"""
        for checker in sort_checkers(self._checkers.values()):
            if checker.msgs:
                self.list_checkers_messages( checker)
        print

    def list_sorted_messages(self):
        """output full sorted messages list in ReST format"""
        msg_ids = []
        for checker in self._checkers.values():
            for msg_id in checker.msgs.keys():
                msg_ids.append(msg_id)
        msg_ids.sort()
        for msg_id in msg_ids:
            print self.get_message_help(msg_id, False)
        print


class ReportsHandlerMixIn:
    """a mix-in class containing all the reports and stats manipulation
    related methods for the main lint class
    """
    def __init__(self):
        self._reports = {}
        self._reports_state = {}

    def register_report(self, r_id, r_title, r_cb, checker):
        """register a report

        r_id is the unique identifier for the report
        r_title the report's title
        r_cb the method to call to make the report
        checker is the checker defining the report
        """
        r_id = r_id.upper()
        self._reports.setdefault(checker, []).append( (r_id, r_title, r_cb) )

    def enable_report(self, r_id):
        """disable the report of the given id"""
        r_id = r_id.upper()
        self._reports_state[r_id] = True

    def disable_report(self, r_id):
        """disable the report of the given id"""
        r_id = r_id.upper()
        self._reports_state[r_id] = False

    def is_report_enabled(self, r_id):
        """return true if the report associated to the given identifier is
        enabled
        """
        return self._reports_state.get(r_id, True)

    def make_reports(self, stats, old_stats):
        """render registered reports"""
        if self.config.files_output:
            filename = 'pylint_global.' + self.reporter.extension
            self.reporter.set_output(open(filename, 'w'))
        sect = Section('Report',
                       '%s statements analysed.'% (self.stats['statement']))
        checkers = sort_checkers(self._reports.keys())
        checkers.reverse()
        for checker in checkers:
            for r_id, r_title, r_cb in self._reports[checker]:
                if not self.is_report_enabled(r_id):
                    continue
                report_sect = Section(r_title)
                try:
                    r_cb(report_sect, stats, old_stats)
                except EmptyReport:
                    continue
                report_sect.report_id = r_id
                sect.append(report_sect)
        self.reporter.display_results(sect)

    def add_stats(self, **kwargs):
        """add some stats entries to the statistic dictionary
        raise an AssertionError if there is a key conflict
        """
        for key, value in kwargs.items():
            if key[-1] == '_':
                key = key[:-1]
            assert not self.stats.has_key(key)
            self.stats[key] = value
        return self.stats

###     ###     - - - -   import utils    - - - -     ###     ###

from os.path import dirname, basename, splitext, exists, isdir, join, normpath
from logilab.common.modutils import modpath_from_file, get_module_files, \
                                    file_from_modpath

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
                    errors.append( {'key' : 'F0003', 'mod': modname} )
                    continue
            except ImportError, ex:
                errors.append( {'key': 'F0001', 'mod': modname, 'ex': ex} )
                continue
        filepath = normpath(filepath)
        result.append( {'path': filepath, 'name': modname,
                        'basepath': filepath, 'basename': modname} )
        if not (modname.endswith('.__init__') or modname == '__init__') \
                and '__init__.py' in filepath:
            for subfilepath in get_module_files(dirname(filepath), black_list):
                if filepath == subfilepath:
                    continue
                submodname = '.'.join(modpath_from_file(subfilepath))
                result.append( {'path': subfilepath, 'name': submodname,
                                'basepath': filepath, 'basename': modname} )
    return result, errors
