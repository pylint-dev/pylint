# Copyright (c) 2003-2006 Sylvain Thenault (thenault@gmail.com).
# Copyright (c) 2003-2006 LOGILAB S.A. (Paris, FRANCE).
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
""" %prog [options] module_or_package

  Check that a module satisfy a coding standard (and more !).

    %prog --help
    
  Display this help message and exit.

    %prog --help-msg <msg-id>[,<msg-id>]

  Display help messages about given message identifiers and exit.
"""

__revision__ = "$Id: lint.py,v 1.115 2006-04-19 09:17:40 syt Exp $"

# import this first to avoid further builtins pollution possibilities
from pylint.checkers import utils

import sys
import os
import re
import tokenize
from os.path import dirname, basename, splitext, exists, isdir, join, normpath

from logilab.common.configuration import OptionsManagerMixIn, check_csv
from logilab.common.modutils import modpath_from_file, get_module_files, \
     file_from_modpath, load_module_from_name
from logilab.common.interface import implements
from logilab.common.textutils import get_csv
from logilab.common.fileutils import norm_open
from logilab.common.ureports import Table, Text
from logilab.common.compat import enumerate
from logilab.common.__pkginfo__ import version as common_version

from logilab.astng import ASTNGManager
from logilab.astng.__pkginfo__ import version as astng_version

from pylint.utils import UnknownMessage, MessagesHandlerMixIn, \
     ReportsHandlerMixIn, MSG_TYPES, sort_checkers
from pylint.interfaces import ILinter, IRawChecker, IASTNGChecker
from pylint.checkers import BaseRawChecker, EmptyReport, \
     table_lines_from_stats
from pylint.reporters.text import TextReporter, TextReporter2, \
     ColorizedTextReporter
from pylint.reporters.html import HTMLReporter
from pylint import config

from pylint.__pkginfo__ import version


OPTION_RGX = re.compile('\s*#*\s*pylint:(.*)')
REPORTER_OPT_MAP = {'text': TextReporter,
                    'parseable': TextReporter2,
                    'colorized': ColorizedTextReporter,
                    'html': HTMLReporter,}

# Python Linter class #########################################################
    
MSGS = {
    'F0001': ('%s',
              'Used when an error occured preventing the analyzing of a \
              module (unable to find it for instance).'),
    'F0002': ('%s: %s',
              'Used when an unexpected error occured while building the ASTNG \
              representation. This is usually accomopagned by a traceback. \
              Please report such errors !'),
    'F0003': ('ignored builtin module %s',
              'Used to indicate that the user asked to analyze a builtin module\
              which has been skipped.'),
    
    'I0001': ('Unable to run raw checkers on built-in module %s',
              'Used to inform that a built-in module has not been checked \
              using the raw checkers.'),
    
    'I0010': ('Unable to consider inline option %r',
              'Used when an inline option is either badly formatted or can\'t \
be used inside modules.'),
    
    'I0011': ('Locally disabling %s',
              'Used when an inline option disable a message or a messages \
              category.'),
    'I0012': ('Locally enabling %s',
              'Used when an inline option enable a message or a messages \
              category.'),
    
    'E0001': ('%s',
              'Used when a syntax error is raised for a module.'),

    'E0011': ('Unrecognized file option %r',
              'Used when an unknown inline option is encountered.'),
    'E0012': ('Bad option value %r',
              'Used when a bad value for an inline option is encountered.'),
    }

class PyLinter(OptionsManagerMixIn, MessagesHandlerMixIn, ReportsHandlerMixIn,
               BaseRawChecker):
    """lint Python modules using external checkers.                            
                                                                               
    This is the main checker controling the other ones and the reports         
    generation. It is itself both a raw checker and an astng checker in order  
    to:                                                                        
    * handle message activation / deactivation at the module level             
    * handle some basic but necessary stats'data (number of classes, methods...)
    """

    __implements__ = (ILinter, IRawChecker, IASTNGChecker)
    
    name = 'master'
    priority = 0
    msgs = MSGS
    may_be_disabled = False
    
    options = (('ignore',
                {'type' : 'csv', 'metavar' : '<file>',
                 'dest' : 'black_list', 'default' : ('CVS',),
                 'help' : 'Add <file or directory> to the black list. It \
should be a base name, not a path. You may set this option multiple times.'}),
               
               ('enable-checker',
                {'type' : 'csv', 'metavar': '<checker ids>',
                 'group': 'Messages control',
                 'help' : 'Enable only checker(s) with the given id(s).\
                 This option conflict with the disable-checker option'}),
            
               ('disable-checker',
                {'type' : 'csv', 'metavar': '<checker ids>',
                 'group': 'Messages control',
                 'help' : 'Enable all checker(s) except those with the \
                 given id(s).\
                 This option conflict with the disable-checker option'}),
               
               ('persistent',
                {'default': 1, 'type' : 'yn', 'metavar' : '<y_or_n>',
                 'help' : 'Pickle collected data for later comparisons.'}),
               
               ('cache-size',
                {'default': 500, 'type' : 'int', 'metavar': '<size>',
                 'help' : 'Set the cache size for astng objects.'}),
               
               ('load-plugins',
                {'type' : 'csv', 'metavar' : '<modules>', 'default' : (),
                 'help' : 'List of plugins (as comma separated values of \
python modules names) to load, usually to register additional checkers.'}),
               
               ('output-format',
                {'default': 'text', 'type': 'choice', 'metavar' : '<format>',
                 'choices': ('text', 'parseable', 'colorized', 'html'),
                 'short': 'f',
                 'group': 'Reports',
                 'help' : 'set the output format. Available formats are text,\
                 parseable, colorized and html'}),

               ('include-ids',
                {'type' : 'yn', 'metavar' : '<y_or_n>', 'default' : 0,
                 'short': 'i',
                 'group': 'Reports',
                 'help' : 'Include message\'s id in output'}),
               
               ('files-output',
                {'default': 0, 'type' : 'yn', 'metavar' : '<y_or_n>',
                 'group': 'Reports',
                 'help' : 'Put messages in a separate file for each module / \
package specified on the command line instead of printing them on stdout. \
Reports (if any) will be written in a file name "pylint_global.[txt|html]".'}),
               
               ('reports',
                {'default': 1, 'type' : 'yn', 'metavar' : '<y_or_n>',
                 'short': 'r',
                 'group': 'Reports',
                 'help' : 'Tells wether to display a full report or only the\
 messages'}),
               
               ('evaluation',
                {'type' : 'string', 'metavar' : '<python_expression>',
                 'group': 'Reports',
                 'default': '10.0 - ((float(5 * error + warning + refactor + \
convention) / statement) * 10)', 
                 'help' : 'Python expression which should return a note less \
than 10 (10 is the highest note).You have access to the variables errors \
warning, statement which respectivly contain the number of errors / warnings\
 messages and the total number of statements analyzed. This is used by the \
 global evaluation report (R0004).'}),
               
               ('comment',
                {'default': 0, 'type' : 'yn', 'metavar' : '<y_or_n>',
                 'group': 'Reports',
                 'help' : 'Add a comment according to your evaluation note. \
This is used by the global evaluation report (R0004).'}),

               ('enable-report',
                {'type' : 'csv', 'metavar': '<rpt ids>',
                 'group': 'Reports',
                 'help' : 'Enable the report(s) with the given id(s).'}),
               
               ('disable-report',
                {'type' : 'csv', 'metavar': '<rpt ids>',
                 'group': 'Reports',
                 'help' : 'Disable the report(s) with the given id(s).'}),
               
               ('enable-msg-cat',
                {'type' : 'csv', 'metavar': '<msg cats>',
                 'group': 'Messages control',
                 'help' : 'Enable all messages in the listed categories.'}),

               ('disable-msg-cat',
                {'type' : 'csv', 'metavar': '<msg cats>',
                 'group': 'Messages control',
                 'help' : 'Disable all messages in the listed categories.'}),
               
               ('enable-msg',
                {'type' : 'csv', 'metavar': '<msg ids>',
                 'group': 'Messages control',
                 'help' : 'Enable the message(s) with the given id(s).'}),
            
               ('disable-msg',
                {'type' : 'csv', 'metavar': '<msg ids>',
                 'group': 'Messages control',
                 'help' : 'Disable the message(s) with the given id(s).'}),
               )
    option_groups = (
        ('Messages control', 'Options controling analysis messages'),
        ('Reports', 'Options related to output formating and reporting'),
        )
    
    def __init__(self, options=(), reporter=None, option_groups=(),
                 pylintrc=None):
        # some stuff has to be done before ancestors initialization...
        #
        # checkers / reporter / astng manager
        self.reporter = None
        self.set_reporter(reporter or TextReporter(sys.stdout))
        self.manager = ASTNGManager()
        self._checkers = {}
        # visit variables
        self.base_name = None
        self.base_file = None
        self.current_name = None
        self.current_file = None
        self.stats = None
        # init options
        self.options = options + PyLinter.options
        self.option_groups = option_groups + PyLinter.option_groups
        self._options_methods = {
            'enable-report': self.enable_report,
            'disable-report': self.disable_report,
            'enable-msg': self.enable_message,
            'disable-msg': self.disable_message,
            'enable-msg-cat': self.enable_message_category,
            'disable-msg-cat': self.disable_message_category}
        full_version = '%%prog %s, \nastng %s, common %s\nPython %s' % (
            version, astng_version, common_version, sys.version)
        OptionsManagerMixIn.__init__(self, usage=__doc__,
                                     version=full_version,
                                     config_file=pylintrc or config.PYLINTRC)
        MessagesHandlerMixIn.__init__(self)
        ReportsHandlerMixIn.__init__(self)
        BaseRawChecker.__init__(self)
        # provided reports
        self.reports = (('R0001', 'Messages by category',
                         report_total_messages_stats),
                        ('R0002', '% errors / warnings by module',
                         report_messages_by_module_stats),
                        ('R0003', 'Messages',
                         report_messages_stats),
                        ('R0004', 'Global evaluation',
                         self.report_evaluation),
                        )
        self.register_checker(self)
        self._dynamic_plugins = []
        
    def load_plugin_modules(self, modnames):
        """take a list of module names which are pylint plugins and load
        and register them
        """
        for modname in modnames:
            if modname in self._dynamic_plugins:
                continue
            self._dynamic_plugins.append(modname)
            module = load_module_from_name(modname)
            module.register(self)
            
    def set_reporter(self, reporter):
        """set the reporter used to display messages and reports"""
        self.reporter = reporter
        reporter.linter = self
            
    def set_option(self, opt_name, value, action=None, opt_dict=None):
        """overridden from configuration.OptionsProviderMixin to handle some
        special options
        """
        if opt_name in self._options_methods:
            if value:
                meth = self._options_methods[opt_name]
                value = check_csv(None, opt_name, value)
                if isinstance(value, (list, tuple)):
                    for _id in value :
                        meth(_id)
                else :
                    meth(value)
        elif opt_name == 'cache-size':
            self.manager.set_cache_size(int(value))
        elif opt_name == 'output-format':
            self.set_reporter(REPORTER_OPT_MAP[value.lower()]())
        elif opt_name in ('enable-checker', 'disable-checker'):
            if not value:
                return
            checkerids = [v.lower() for v in check_csv(None, opt_name, value)]
            self.enable_checkers(checkerids, opt_name == 'enable-checker')
        BaseRawChecker.set_option(self, opt_name, value, action, opt_dict)

    # checkers manipulation methods ###########################################
    
    def register_checker(self, checker):
        """register a new checker

        checker is an object implementing IRawChecker or / and IASTNGChecker
        """
        assert checker.priority <= 0, 'checker priority can\'t be >= 0'
        self._checkers[checker] = 1
        if hasattr(checker, 'reports'):
            for r_id, r_title, r_cb in checker.reports:
                self.register_report(r_id, r_title, r_cb, checker)
        self.register_options_provider(checker)
        if hasattr(checker, 'msgs'):
            self.register_messages(checker)
        # XXX adim should we load_defaults() here ?: checker.load_defaults()
        
    def enable_checkers(self, listed, enabled):
        """only enable/disable checkers from the given list"""
        idmap = {}
        for checker in self._checkers.keys():
            checker.enable(not enabled)
            idmap[checker.name] = checker
        for checkerid in listed:
            try:
                checker = idmap[checkerid]
            except KeyError:
                raise Exception('no checker named %s' % checkerid)
            checker.enable(enabled)
            
    def disable_noerror_checkers(self):
        """disable all checkers without error messages, and the
        'miscellaneous' checker which can be safely deactivated in debug
        mode
        """
        for checker in self._checkers.keys():
            if checker.name == 'miscellaneous':
                checker.enable(False)
                continue
            for msgid in getattr(checker, 'msgs', {}).keys():
                if msgid[0] == 'E':
                    checker.enable(True)
                    break
            else:
                checker.enable(False)
                
    # block level option handling #############################################
    #
    # see func_block_disable_msg.py test case for expected behaviour
    
    def process_tokens(self, tokens):
        """process tokens from the current module to search for module/block
        level options
        """
        comment = tokenize.COMMENT
        newline = tokenize.NEWLINE
        #line_num = 0
        for (tok_type, _, start, _, line) in tokens:
            if tok_type not in (comment, newline):
                continue
            #if start[0] == line_num:
            #    continue
            match = OPTION_RGX.search(line)
            if match is None:
                continue
            try:
                opt, value = match.group(1).split('=', 1)
            except ValueError:
                self.add_message('I0010', args=match.group(1).strip(),
                                 line=start[0])                
                continue
            opt = opt.strip()
            #line_num = start[0]
            if opt in self._options_methods and not opt.endswith('-report'):
                meth = self._options_methods[opt]
                for msgid in get_csv(value):
                    try:
                        meth(msgid, 'module', start[0])
                    except UnknownMessage:
                        self.add_message('E0012', args=msgid, line=start[0])
            else:
                self.add_message('E0011', args=opt, line=start[0])
    
    def collect_block_lines(self, node, msg_state):
        """walk ast to collect block level options line numbers"""
        # recurse on children (depth first)
        for child in node.getChildNodes():
            self.collect_block_lines(child, msg_state)            
        for msgid, lines in msg_state.items():
            #if msg in self._module_msgs_state:
            #    continue
            for lineno, state in lines.items():
                first = node.source_line()
                last = node.last_source_line()
                if lineno >= first and lineno <= last:
                    # set state for all lines for this block
                    first, last = node.block_range(lineno)
                    for line in xrange(first, last+1):
                        # do not override existing entries
                        if not line in self._module_msgs_state.get(msgid, ()):
                            try:
                                self._module_msgs_state[msgid][line] = state
                            except KeyError:
                                self._module_msgs_state[msgid] = {line: state}
                    del lines[lineno]
                    
    
    # code checking methods ###################################################

    def check(self, files_or_modules):
        """main checking entry: check a list of files or modules from their
        name.
        """
        self.reporter.include_ids = self.config.include_ids
        if not isinstance(files_or_modules, (list, tuple)):
            files_or_modules = (files_or_modules,)
        checkers = sort_checkers(self._checkers.keys())
        rev_checkers = checkers[:]
        rev_checkers.reverse()
        # notify global begin
        for checker in checkers:
            checker.open()
        # check modules or packages        
        for something in files_or_modules:
            self.base_name = self.base_file = normpath(something)
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
                        self.set_current_module(modname)
                        self.add_message('F0003', args=modname)
                        continue
                except ImportError, ex:
                    #if __debug__:
                    #    import traceback
                    #    traceback.print_exc()
                    self.set_current_module(modname)
                    msg = str(ex).replace(os.getcwd() + os.sep, '')
                    self.add_message('F0001', args=msg)
                    continue
            if self.config.files_output:
                reportfile = 'pylint_%s.%s' % (modname, self.reporter.extension)
                self.reporter.set_output(open(reportfile, 'w'))
            self.check_file(filepath, modname, checkers)
        # notify global end
        self.set_current_module('')
        for checker in rev_checkers:
            checker.close()

    def check_file(self, filepath, modname, checkers):
        """check a module or package from its name
        if modname is a package, recurse on its subpackages / submodules
        """
        # get the given module representation
        self.base_name = modname
        self.base_file = normpath(filepath)
        # check this module
        astng = self._check_file(filepath, modname, checkers)
        if astng is None:
            return
        # recurse in package except if __init__ was explicitly given
        if not modname.endswith('.__init__') and astng.package:
            for filepath in get_module_files(dirname(filepath),
                                             self.config.black_list):
                if filepath == self.base_file:
                    continue
                modname = '.'.join(modpath_from_file(filepath))
                self._check_file(filepath, modname, checkers)

    def _check_file(self, filepath, modname, checkers):
        """check a module by building its astng representation"""
        self.set_current_module(modname, filepath)
        # get the module representation
        astng = self.get_astng(filepath, modname)
        if astng is not None:
            # set the base file if necessary
            self.base_file = self.base_file or astng.file
            # fix the current file (if the source file was not available or
            # if its actually a c extension
            self.current_file = astng.file
            # and check it
            self.check_astng_module(astng, checkers)
        return astng
        
    def set_current_module(self, modname, filepath=None):
        """set the name of the currently analyzed module and
        init statistics for it
        """
        self.current_name = modname 
        self.current_file = filepath or modname
        self.stats['by_module'][modname] = {}
        self.stats['by_module'][modname]['statement'] = 0
        for msg_cat in MSG_TYPES.values():
            self.stats['by_module'][modname][msg_cat] = 0
        # XXX hack, to be correct we need to keep module_msgs_state
        # for every analyzed module (the problem stands with localized
        # messages which are only detected in the .close step)
        if modname:
            self._module_msgs_state = {}
            self._module_msg_cats_state = {}
            
    def get_astng(self, filepath, modname):
        """return a astng representation for a module"""
        try:
            return self.manager.astng_from_file(filepath, modname)
        except SyntaxError, ex:
            self.add_message('E0001', line=ex.lineno, args=ex.msg)
        except KeyboardInterrupt:
            raise
        except Exception, ex:
            #if __debug__:
            #    import traceback
            #    traceback.print_exc()
            self.add_message('F0002', args=(ex.__class__, ex))
        

    def check_astng_module(self, astng, checkers):
        """check a module from its astng representation, real work"""
        # call raw checkers if possible
        if not astng.pure_python:
            self.add_message('I0001', args=astng.name)
        else:
            #assert astng.file.endswith('.py')
            stream = norm_open(astng.file)
            # invoke IRawChecker interface on self to fetch module/block
            # level options
            self.process_module(stream)
            # walk ast to collect line numbers
            orig_state = self._module_msgs_state.copy()
            self._module_msgs_state = {}
            self.collect_block_lines(astng, orig_state)

            for checker in checkers:
                if implements(checker, IRawChecker) and checker is not self:
                    stream.seek(0)
                    checker.process_module(stream)
        # generate events to astng checkers
        self.astng_events(astng, [checker for checker in checkers
                                  if implements(checker, IASTNGChecker)])
    
    def astng_events(self, astng, checkers, _reversed_checkers=None):
        """generate event to astng checkers according to the current astng
        node and recurse on its children
        """
        if _reversed_checkers is None:
            _reversed_checkers = checkers[:]
            _reversed_checkers.reverse()
        if astng.is_statement():
            self.stats['statement'] += 1
        # generate events for this node on each checkers
        for checker in checkers:
            checker.visit(astng)
        # recurse on children
        for child in astng.getChildNodes():
            self.astng_events(child, checkers, _reversed_checkers)
        for checker in _reversed_checkers:
            checker.leave(astng)
        

    # IASTNGChecker interface #################################################
        
    def open(self):
        """initialize counters"""
        self.stats = { 'by_module' : {},
                       'by_msg' : {},
                       'statement' : 0
                       }
        for msg_cat in MSG_TYPES.values():
            self.stats[msg_cat] = 0
    
    def close(self):
        """close the whole package /module, it's time to make reports !
        
        if persistent run, pickle results for later comparison
        """
        # load old results if any
        old_stats = config.load_results(self.base_name)
        if self.config.reports:
            self.make_reports(self.stats, old_stats)
        # save results if persistent run
        if self.config.persistent:
            config.save_results(self.stats, self.base_name)
            
    # specific reports ########################################################
        
    def report_evaluation(self, sect, stats, old_stats):
        """make the global evaluation report"""
        # check with at least check 1 statements (usually 0 when there is a
        # syntax error preventing pylint from further processing)
        if stats['statement'] == 0:
            raise EmptyReport()
        # get a global note for the code
        evaluation = self.config.evaluation
        try:
            note = eval(evaluation, {}, self.stats)
        except Exception, ex:
            msg = 'An exception occured while rating: %s' % ex
        else:
            stats['global_note'] = note
            msg = 'Your code has been rated at %.2f/10' % note
            if old_stats.has_key('global_note'):
                msg += ' (previous run: %.2f/10)' % old_stats['global_note']
            if self.config.comment:
                msg = '%s\n%s' % (msg, config.get_note_message(note))
        sect.append(Text(msg))

# some reporting functions ####################################################

def report_total_messages_stats(sect, stats, old_stats):
    """make total errors / warnings report"""
    lines = ['type', 'number', 'previous', 'difference']
    lines += table_lines_from_stats(stats, old_stats,
                                    ('convention', 'refactor',
                                     'warning', 'error'))
    sect.append(Table(children=lines, cols=4, rheaders=1))

def report_messages_stats(sect, stats, _):
    """make messages type report"""
    if not stats['by_msg']:
        # don't print this report when we didn't detected any errors
        raise EmptyReport()
    in_order = [(value, msg_id)
                for msg_id, value in stats['by_msg'].items()
                if not msg_id.startswith('I')]
    in_order.sort()
    in_order.reverse()
    lines = ('message id', 'occurences')
    for value, msg_id in in_order:
        lines += (msg_id, str(value))
    sect.append(Table(children=lines, cols=2, rheaders=1))

def report_messages_by_module_stats(sect, stats, _):
    """make errors / warnings by modules report"""
    if len(stats['by_module']) == 1:
        # don't print this report when we are analysing a single module
        raise EmptyReport()
    by_mod = {} 
    for m_type in ('fatal', 'error', 'warning', 'refactor', 'convention'):
        total = stats[m_type]
        for module in stats['by_module'].keys():
            mod_total = stats['by_module'][module][m_type]
            if total == 0:
                percent = 0
            else:
                percent = float((mod_total)*100) / total
            by_mod.setdefault(module, {})[m_type] = percent            
    sorted_result = []
    for module, mod_info in by_mod.items():
        sorted_result.append((mod_info['error'],
                              mod_info['warning'],
                              mod_info['refactor'],
                              mod_info['convention'],
                              module))
    sorted_result.sort()
    sorted_result.reverse()
    lines = ['module', 'error', 'warning', 'refactor', 'convention']
    for line in sorted_result:
        if line[0] == 0 and line[1] == 0:
            break
        lines.append(line[-1])
        for val in line[:-1]:
            lines.append('%.2f' % val)
    if len(lines) == 5:
        raise EmptyReport()
    sect.append(Table(children=lines, cols=5, rheaders=1))



# utilities ###################################################################

# this may help to import modules using gettext

try:
    __builtins__._ = str
except AttributeError:
    __builtins__['_'] = str


def preprocess_options(args, search_for):
    """look for some options (keys of <search_for>) which have to be processed
    before others
    
    values of <search_for> are callback functions to call when the option is
    found
    """
    for i, arg in enumerate(args):
        for option in search_for:
            if arg.startswith('--%s=' % option):
                search_for[option](option, arg[len(option)+3:])
                del args[i]
            elif arg == '--%s' % option:
                search_for[option](option, args[i + 1])
                del args[i:i+2]
    
class Run:
    """helper class to use as main for pylint :
    
    run(*sys.argv[1:])
    """
    option_groups = (
        ('Commands', 'Options which are actually commands. Options in this \
group are mutually exclusive.'),
        )
    
    def __init__(self, args, reporter=None, quiet=0):
        self._rcfile = None
        self._plugins = []
        preprocess_options(args, {'rcfile': self.cb_set_rcfile,
                                  'load-plugins': self.cb_add_plugins})
        self.linter = linter = PyLinter((
            ('rcfile',
             {'action' : 'callback', 'callback' : lambda *args: 1,
              'type': 'string', 'metavar': '<file>',
              'help' : 'Specify a configuration file.'}),

            ('help-msg',
             {'action' : 'callback', 'type' : 'string', 'metavar': '<msg-id>',
              'callback' : self.cb_help_message,
              'group': 'Commands',
              'help' : '''Display a help message for the given message id and \
exit. The value may be a comma separated list of message ids.'''}),

            ('list-msgs',
             {'action' : 'callback', 'metavar': '<msg-id>',
              'callback' : self.cb_list_messages,
              'group': 'Commands',
              'help' : "Generate pylint's full documentation."}),

            ('generate-rcfile',
             {'action' : 'callback', 'callback' : self.cb_generate_config,
              'group': 'Commands',
              'help' : '''Generate a sample configuration file according to \
the current configuration. You can put other options before this one to get \
them in the generated configuration.'''}),
            
            ('generate-man',
             {'action' : 'callback', 'callback' : self.cb_generate_manpage,
              'group': 'Commands',
              'help' : "Generate pylint's man page."}),
            
            ('errors-only',
             {'action' : 'callback', 'callback' : self.cb_debug_mode,
              'short': 'e', 
              'help' : '''In debug mode, checkers without error messages are \
disabled and for others, only the ERROR messages are displayed, and no reports \
are done by default'''}),
            
            ('profile',
             {'type' : 'yn', 'metavar' : '<y_or_n>',
              'default': False,
              'help' : 'Profiled execution.'}),

            ), option_groups=self.option_groups,
               reporter=reporter, pylintrc=self._rcfile)
        linter.quiet = quiet
        # register standard checkers
        from pylint import checkers
        checkers.initialize(linter)
        # load command line plugins
        linter.load_plugin_modules(self._plugins)
        # add some help section
        linter.add_help_section('Environment variables', config.ENV_HELP)
        linter.add_help_section('Output', '''
Using the default text output, the message format is :                         
        MESSAGE_TYPE: LINE_NUM:[OBJECT:] MESSAGE                               
There are 5 kind of message types :                                            
    * (C) convention, for programming standard violation                       
    * (R) refactor, for bad code smell                                         
    * (W) warning, for python specific problems                                
    * (E) error, for much probably bugs in the code                                                
    * (F) fatal, if an error occured which prevented pylint from doing further \
processing.     
        ''')
        # read configuration
        linter.load_provider_defaults()
        linter.read_config_file()
        # is there some additional plugins in the file configuration, in
        config_parser = linter._config_parser
        if config_parser.has_option('master', 'load-plugins'):
            plugins = get_csv(config_parser.get('master', 'load-plugins'))
            linter.load_plugin_modules(plugins)
        # now we can load file config and command line, plugins (which can
        # provide options) have been registered
        linter.load_config_file()
        args = linter.load_command_line_configuration(args)
        if not args:
            print linter.help()
            sys.exit(1)
        # insert current working directory to the python path to have a correct
        # behaviour
        sys.path.insert(0, os.getcwd())
        if self.linter.config.profile:
            print >> sys.stderr, '** profiled run'
            from hotshot import Profile, stats
            prof = Profile('stones.prof')
            prof.runcall(linter.check, args)
            prof.close()
            data = stats.load('stones.prof')
            data.strip_dirs()
            data.sort_stats('time', 'calls')
            data.print_stats(30)
        else:
            linter.check(args)
        sys.path.pop(0)

    def cb_set_rcfile(self, name, value):
        """callback for option preprocessing (ie before optik parsing)"""
        self._rcfile = value
        
    def cb_add_plugins(self, name, value):
        """callback for option preprocessing (ie before optik parsing)"""
        self._plugins.extend(get_csv(value))
                
    def cb_debug_mode(self, *args, **kwargs):
        """debug mode:
        * checkers without error messages are disabled 
        * for others, only the ERROR messages are displayed
        * disable reports
        * do not save execution information
        """
        self.linter.disable_noerror_checkers()
        self.linter.set_option('disable-msg-cat', ('W', 'C', 'R', 'F', 'I'))
        self.linter.set_option('reports', False)
        self.linter.set_option('persistent', False)
        
    
    def cb_generate_config(self, *args, **kwargs):
        """optik callback for sample config file generation"""
        self.linter.generate_config()
        sys.exit(0)
         
    def cb_generate_manpage(self, *args, **kwargs):
        """optik callback for sample config file generation"""
        from pylint import __pkginfo__
        self.linter.generate_manpage(__pkginfo__)
        sys.exit(0)
         
    def cb_help_message(self, option, opt_name, value, parser):
        """optik callback for printing some help about a particular message"""
        self.linter.help_message(get_csv(value))
        sys.exit(0)
        
    def cb_list_messages(self, option, opt_name, value, parser):
        """optik callback for printing available messages"""
        self.linter.list_messages()
        sys.exit(0)


if __name__ == '__main__':
    Run(sys.argv[1:])
