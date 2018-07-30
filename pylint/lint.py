# -*- coding: utf-8 -*-
# Copyright (c) 2006-2015 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2008 Fabrice Douchant <Fabrice.Douchant@logilab.fr>
# Copyright (c) 2009 Vincent
# Copyright (c) 2009 Mads Kiilerich <mads@kiilerich.com>
# Copyright (c) 2011-2014 Google, Inc.
# Copyright (c) 2012 David Pursehouse <david.pursehouse@sonymobile.com>
# Copyright (c) 2012 Kevin Jing Qiu <kevin.jing.qiu@gmail.com>
# Copyright (c) 2012 FELD Boris <lothiraldan@gmail.com>
# Copyright (c) 2012 JT Olds <jtolds@xnet5.com>
# Copyright (c) 2014-2018 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014-2015 Michal Nowikowski <godfryd@gmail.com>
# Copyright (c) 2014 Brett Cannon <brett@python.org>
# Copyright (c) 2014 Alexandru Coman <fcoman@bitdefender.com>
# Copyright (c) 2014 Daniel Harding <dharding@living180.net>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2014 Dan Goldsmith <djgoldsmith@googlemail.com>
# Copyright (c) 2015-2016 Florian Bruhin <me@the-compiler.org>
# Copyright (c) 2015 Aru Sahni <arusahni@gmail.com>
# Copyright (c) 2015 Steven Myint <hg@stevenmyint.com>
# Copyright (c) 2015 Simu Toni <simutoni@gmail.com>
# Copyright (c) 2015 Mihai Balint <balint.mihai@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016-2017 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2016 Glenn Matthews <glenn@e-dad.net>
# Copyright (c) 2016 Alan Evangelista <alanoe@linux.vnet.ibm.com>
# Copyright (c) 2017-2018 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2017-2018 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2017 Daniel Miller <millerdev@gmail.com>
# Copyright (c) 2017 Roman Ivanov <me@roivanov.com>
# Copyright (c) 2017 Ned Batchelder <ned@nedbatchelder.com>
# Copyright (c) 2018 Randall Leeds <randall@bleeds.info>
# Copyright (c) 2018 Mike Frysinger <vapier@gmail.com>
# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
# Copyright (c) 2018 Ville Skyttä <ville.skytta@upcloud.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2018 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2018 Jason Owen <jason.a.owen@gmail.com>
# Copyright (c) 2018 Gary Tyler McLeod <mail@garytyler.com>
# Copyright (c) 2018 Yuval Langer <yuvallanger@mail.tau.ac.il>
# Copyright (c) 2018 Nick Drozd <nicholasdrozd@gmail.com>
# Copyright (c) 2018 kapsh <kapsh@kap.sh>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

# pylint: disable=broad-except

""" %prog [options] modules_or_packages

  Check that module(s) satisfy a coding standard (and more !).

    %prog --help

  Display this help message and exit.

    %prog --help-msg <msg-id>[,<msg-id>]

  Display help messages about given message identifiers and exit.
"""
from __future__ import print_function

import argparse
import collections
import contextlib
import operator
import os
import sys
import tokenize
import warnings

import astroid
from astroid.__pkginfo__ import version as astroid_version
from astroid import modutils
from pylint import checkers
from pylint import interfaces
from pylint import reporters
from pylint import exceptions
from pylint import utils
from pylint import config
from pylint.__pkginfo__ import version
from pylint.reporters.ureports import nodes as report_nodes


FULL_VERSION = '%%(prog)s %s\nastroid %s\nPython %s' % (
    version, astroid_version, sys.version)

MANAGER = astroid.MANAGER


def _get_python_path(filepath):
    dirname = os.path.realpath(os.path.expanduser(filepath))
    if not os.path.isdir(dirname):
        dirname = os.path.dirname(dirname)
    while True:
        if not os.path.exists(os.path.join(dirname, "__init__.py")):
            return dirname
        old_dirname = dirname
        dirname = os.path.dirname(dirname)
        if old_dirname == dirname:
            return os.getcwd()
    return None


def _merge_stats(stats):
    merged = {}
    by_msg = collections.Counter()
    nested_keys = set()
    for stat in stats:
        message_stats = stat.pop('by_msg', {})
        by_msg.update(message_stats)

        for key, item in stat.items():
            if key not in merged:
                merged[key] = item
            else:
                if isinstance(item, dict):
                    nested_keys.add(key)
                elif isinstance(item, set):
                    merged[key].update(item)
                else:
                    merged[key] = merged[key] + item

    for key in nested_keys:
        merged[key] = _merge_stats(stat.get(key, {}) for stat in stats)

    if by_msg:
        merged['by_msg'] = by_msg
    return merged


@contextlib.contextmanager
def _patch_sysmodules():
    # Context manager that permits running pylint, on Windows, with -m switch
    # and with --jobs, as in 'python -2 -m pylint .. --jobs'.
    # For more details why this is needed,
    # see Python issue http://bugs.python.org/issue10845.

    mock_main = __name__ != '__main__' # -m switch
    if mock_main:
        sys.modules['__main__'] = sys.modules[__name__]

    try:
        yield
    finally:
        if mock_main:
            sys.modules.pop('__main__')


# some reporting functions ####################################################

def report_total_messages_stats(sect, stats, previous_stats):
    """make total errors / warnings report"""
    lines = ['type', 'number', 'previous', 'difference']
    lines += checkers.table_lines_from_stats(stats, previous_stats,
                                             ('convention', 'refactor',
                                              'warning', 'error'))
    sect.append(report_nodes.Table(children=lines, cols=4, rheaders=1))

def report_messages_stats(sect, stats, _):
    """make messages type report"""
    if not stats['by_msg']:
        # don't print this report when we didn't detected any errors
        raise exceptions.EmptyReportError()
    in_order = sorted([(value, msg_id)
                       for msg_id, value in six.iteritems(stats['by_msg'])
                       if not msg_id.startswith('I')])
    in_order.reverse()
    lines = ('message id', 'occurrences')
    for value, msg_id in in_order:
        lines += (msg_id, str(value))
    sect.append(report_nodes.Table(children=lines, cols=2, rheaders=1))

def report_messages_by_module_stats(sect, stats, _):
    """make errors / warnings by modules report"""
    if len(stats['by_module']) == 1:
        # don't print this report when we are analysing a single module
        raise exceptions.EmptyReportError()
    by_mod = collections.defaultdict(dict)
    for m_type in ('fatal', 'error', 'warning', 'refactor', 'convention'):
        total = stats[m_type]
        for module in six.iterkeys(stats['by_module']):
            mod_total = stats['by_module'][module][m_type]
            if total == 0:
                percent = 0
            else:
                percent = float((mod_total)*100) / total
            by_mod[module][m_type] = percent
    sorted_result = []
    for module, mod_info in six.iteritems(by_mod):
        sorted_result.append((mod_info['error'],
                              mod_info['warning'],
                              mod_info['refactor'],
                              mod_info['convention'],
                              module))
    sorted_result.sort()
    sorted_result.reverse()
    lines = ['module', 'error', 'warning', 'refactor', 'convention']
    for line in sorted_result:
        # Don't report clean modules.
        if all(entry == 0 for entry in line[:-1]):
            continue
        lines.append(line[-1])
        for val in line[:-1]:
            lines.append('%.2f' % val)
    if len(lines) == 5:
        raise exceptions.EmptyReportError()
    sect.append(report_nodes.Table(children=lines, cols=5, rheaders=1))


# Python Linter class #########################################################

MSGS = {
    'F0001': ('%s',
              'fatal',
              'Used when an error occurred preventing the analysis of a \
              module (unable to find it for instance).'),
    'F0002': ('%s: %s',
              'astroid-error',
              'Used when an unexpected error occurred while building the '
              'Astroid  representation. This is usually accompanied by a '
              'traceback. Please report such errors !'),
    'F0010': ('error while code parsing: %s',
              'parse-error',
              'Used when an exception occurred while building the Astroid '
              'representation which could be handled by astroid.'),

    'I0001': ('Unable to run raw checkers on built-in module %s',
              'raw-checker-failed',
              'Used to inform that a built-in module has not been checked '
              'using the raw checkers.'),

    'I0010': ('Unable to consider inline option %r',
              'bad-inline-option',
              'Used when an inline option is either badly formatted or can\'t '
              'be used inside modules.'),

    'I0011': ('Locally disabling %s (%s)',
              'locally-disabled',
              'Used when an inline option disables a message or a messages '
              'category.'),
    'I0012': ('Locally enabling %s (%s)',
              'locally-enabled',
              'Used when an inline option enables a message or a messages '
              'category.'),
    'I0013': ('Ignoring entire file',
              'file-ignored',
              'Used to inform that the file will not be checked'),
    'I0020': ('Suppressed %s (from line %d)',
              'suppressed-message',
              'A message was triggered on a line, but suppressed explicitly '
              'by a disable= comment in the file. This message is not '
              'generated for messages that are ignored due to configuration '
              'settings.'),
    'I0021': ('Useless suppression of %s',
              'useless-suppression',
              'Reported when a message is explicitly disabled for a line or '
              'a block of code, but never triggered.'),
    'I0022': ('Pragma "%s" is deprecated, use "%s" instead',
              'deprecated-pragma',
              'Some inline pylint options have been renamed or reworked, '
              'only the most recent form should be used. '
              'NOTE:skip-all is only available with pylint >= 0.26',
              {'old_names': [('I0014', 'deprecated-disable-all')]}),

    'E0001': ('%s',
              'syntax-error',
              'Used when a syntax error is raised for a module.'),

    'E0011': ('Unrecognized file option %r',
              'unrecognized-inline-option',
              'Used when an unknown inline option is encountered.'),
    'E0012': ('Bad option value %r',
              'bad-option-value',
              'Used when a bad value for an inline option is encountered.'),
    }


# pylint: disable=too-many-instance-attributes
class PyLinter(utils.MessagesHandlerMixIn,
               checkers.BaseTokenChecker):
    """lint Python modules using external checkers.

    This is the main checker controlling the other ones and the reports
    generation. It is itself both a raw checker and an astroid checker in order
    to:
    * handle message activation / deactivation at the module level
    * handle some basic but necessary stats'data (number of classes, methods...)

    IDE plugin developers: you may have to call
    `astroid.builder.MANAGER.astroid_cache.clear()` across runs if you want
    to ensure the latest code version is actually checked.
    """

    __implements__ = (interfaces.ITokenChecker, )

    name = 'master'
    priority = 0
    level = 0
    msgs = MSGS

    options = (
        ('ignore',
         {'type' : 'csv', 'metavar' : '<file>,...',
          'dest' : 'black_list', 'default' : ('CVS',),
          'help' : 'Add files or directories to the blacklist. '
          'They should be base names, not paths.'}),

        ('ignore-patterns',
         {'type' : 'regexp_csv', 'metavar' : '<pattern>,...',
          'dest' : 'black_list_re', 'default' : (),
          'help' : 'Add files or directories matching the regex patterns to the'
          ' blacklist. The regex matches against base names, not paths.'}),

        ('persistent',
         {'default': True, 'type' : 'yn', 'metavar' : '<y_or_n>',
          'level': 1,
          'help' : 'Pickle collected data for later comparisons.'}),

        ('load-plugins',
         {'type' : 'csv', 'metavar' : '<modules>', 'default' : (),
          'level': 1,
          'help' : 'List of plugins (as comma separated values of '
          'python modules names) to load, usually to register '
          'additional checkers.'}),

        ('output-format',
         {'default': 'text', 'type': 'string', 'metavar' : '<format>',
          'short': 'f',
          'group': 'Reports',
          'help' : 'Set the output format. Available formats are text,'
          ' parseable, colorized, json and msvs (visual studio).'
          ' You can also give a reporter class, e.g. mypackage.mymodule.'
          'MyReporterClass.'}),

        ('reports',
         {'default': False, 'type' : 'yn', 'metavar' : '<y_or_n>',
          'short': 'r',
          'group': 'Reports',
          'help' : 'Tells whether to display a full report or only the '
          'messages'}),

        ('evaluation',
         {'type' : 'string', 'metavar' : '<python_expression>',
          'group': 'Reports', 'level': 1,
          'default': '10.0 - ((float(5 * error + warning + refactor + '
          'convention) / statement) * 10)',
          'help' : 'Python expression which should return a note less '
          'than 10 (10 is the highest note). You have access '
          'to the variables errors warning, statement which '
          'respectively contain the number of errors / '
          'warnings messages and the total number of '
          'statements analyzed. This is used by the global '
          'evaluation report (RP0004).'}),
    ('score',
     {'default': True, 'type': 'yn', 'metavar': '<y_or_n>',
      'short': 's',
      'group': 'Reports',
      'help': 'Activate the evaluation score.'}),

    ('confidence',
     {'type' : 'multiple_choice', 'metavar': '<levels>',
      'default': '',
      'choices': [c.name for c in interfaces.CONFIDENCE_LEVELS],
      'group': 'Messages control',
      'help' : 'Only show warnings with the listed confidence levels.'
      ' Leave empty to show all. Valid levels: %s' % (
          ', '.join(c.name for c in interfaces.CONFIDENCE_LEVELS),)}),

    ('enable',
     {'type' : '_msg_on', 'metavar': '<msg ids>',
      'dest': 'msg_toggles', 'action': 'append',
      'short': 'e', 'default': [],
      'group': 'Messages control',
      'help' : 'Enable the message, report, category or checker with the '
      'given id(s). You can either give multiple identifiers '
      'separated by comma (,) or put this option multiple times '
      '(only on the command line, not in the configuration file '
      'where it should appear only once). '
      'See also the "--disable" option for examples. '}),

    ('disable',
     {'type' : '_msg_off', 'metavar': '<msg ids>',
      'dest': 'msg_toggles', 'action': 'append',
      'short': 'd', 'default': [],
      'group': 'Messages control',
      'help' : 'Disable the message, report, category or checker '
      'with the given id(s). You can either give multiple identifiers'
      ' separated by comma (,) or put this option multiple times '
      '(only on the command line, not in the configuration file '
      'where it should appear only once).'
      'You can also use "--disable=all" to disable everything first '
      'and then reenable specific checks. For example, if you want '
      'to run only the similarities checker, you can use '
      '"--disable=all --enable=similarities". '
      'If you want to run only the classes checker, but have no '
      'Warning level messages displayed, use'
      '"--disable=all --enable=classes --disable=W"'}),

    ('msg-template',
     {'type' : 'string', 'metavar': '<template>', 'default': '',
      'group': 'Reports',
      'help' : ('Template used to display messages. '
                'This is a python new-style format string '
                'used to format the message information. '
                'See doc for all details')
      }),

    ('jobs',
     {'type' : 'int', 'metavar': '<n-processes>',
      'short': 'j',
      'default': 1,
      'help' : '''Use multiple processes to speed up Pylint.''',
      }),

    ('unsafe-load-any-extension',
     {'type': 'yn', 'metavar': '<yn>', 'default': False, 'hide': True,
      'help': ('Allow loading of arbitrary C extensions. Extensions'
               ' are imported into the active Python interpreter and'
               ' may run arbitrary code.')}),

    ('limit-inference-results',
     {'type': 'int', 'metavar': '<number-of-results>', 'default': 100,
      'help': ('Control the amount of potential inferred values when inferring '
               'a single object. This can help the performance when dealing with '
               'large functions or complex, nested conditions. ')}),

    ('extension-pkg-whitelist',
     {'type': 'csv', 'metavar': '<pkg>,...', 'default': [],
      'help': ('A comma-separated list of package or module names'
               ' from where C extensions may be loaded. Extensions are'
               ' loading into the active Python interpreter and may run'
               ' arbitrary code')}),
    ('suggestion-mode',
     {'type': 'yn', 'metavar': '<yn>', 'default': True,
      'help': ('When enabled, pylint would attempt to guess common '
               'misconfiguration and emit user-friendly hints instead '
               'of false-positive error messages')}),
    ('exit-zero',
     {'type': 'yn', 'default': False,
      'help': ('Always return a 0 (non-error) status code, even if '
               'lint errors are found. This is primarily useful in '
               'continuous integration scripts.')}),
    )

    option_groups = (
        ('Messages control', 'Options controlling analysis messages'),
        ('Reports', 'Options related to output formatting and reporting'),
        )

    reports = (
        ('RP0001', 'Messages by category',
         report_total_messages_stats),
        ('RP0002', '% errors / warnings by module',
         report_messages_by_module_stats),
        ('RP0003', 'Messages',
         report_messages_stats),
    )

    def __init__(self, config=None):
        # some stuff has to be done before ancestors initialization...
        #
        # messages store / checkers / reporter / astroid manager
        self.config = config
        self._checkers = collections.defaultdict(list)
        self._pragma_lineno = {}
        self._ignore_file = False
        # visit variables
        self.current_name = None
        self.current_file = None

        super().__init__(config)
        # provided reports
        self._dynamic_plugins = set()

    def disable(self, msgid, scope='module', line=None, ignore_unknown=False):
        """Do not output messages that have the given ID.

        :param msgid: The ID of the message to disable.
            This can also be "all" to disable all messages,
            the ID of a category to disable all messages of that category,
            or the name of a checker to disable all messages from the checker.
        :type msgid: str

        :param scope: Must be "module". Provided for backwards compatibility.
        :type scope: str.

        :param line: The line number that the message is disabled on.
        :type line: int

        :param ignore_unknown: If this is False,
            an :exc:`UnknownMessageError` is raised when a message with the
            given ID cannot be found.
            If this is True, the exception is not raised.
        :param ignore_unknown: bool

        :raises ValueError: If `scope` is anything other than "module".
        """
        self._set_msg_status(
            msgid,
            enable=False,
            scope=scope,
            line=line,
            ignore_unknown=ignore_unknown,
        )

    def enable(self, msgid, scope='module', line=None, ignore_unknown=False):
        """Enable outputting messages that have the given ID.

        :param msgid: The ID of the message to enable.
            This can also be "all" to enable all messages,
            the ID of a category to enable all messages of that category,
            or the name of a checker to enable all messages from the checker.
        :type msgid: str

        :param scope: Must be "module". Provided for backwards compatibility.
        :type scope: str.

        :param line: The line number that the message is enabled on.
        :type line: int

        :param ignore_unknown: If this is False,
            an :exc:`UnknownMessageError` is raised when a message with the
            given ID cannot be found.
            If this is True, the exception is not raised.
        :param ignore_unknown: bool
        """
        self._set_msg_status(
            msgid,
            enable=True,
            scope=scope,
            line=line,
            ignore_unknown=ignore_unknown,
        )

    # block level option handling #############################################
    #
    # see func_block_disable_msg.py test case for expected behaviour

    def process_tokens(self, tokens):
        """process tokens from the current module to search for module/block
        level options
        """
        options_methods = {
            'enable': self.enable,
            'disable': self.disable,
        }
        control_pragmas = {'disable', 'enable'}
        for (tok_type, content, start, _, _) in tokens:
            if tok_type != tokenize.COMMENT:
                continue
            match = utils.OPTION_RGX.search(content)
            if match is None:
                continue
            if match.group(1).strip() == "disable-all" or \
                    match.group(1).strip() == 'skip-file':
                if match.group(1).strip() == "disable-all":
                    self.add_message('deprecated-pragma', line=start[0],
                                     args=('disable-all', 'skip-file'))
                self.add_message('file-ignored', line=start[0])
                self._ignore_file = True
                return
            try:
                opt, value = match.group(1).split('=', 1)
            except ValueError:
                self.add_message('bad-inline-option', args=match.group(1).strip(),
                                 line=start[0])
                continue
            opt = opt.strip()
            if opt in options_methods:
                meth = options_methods[opt]
                for msgid in utils._splitstrip(value):
                    # Add the line where a control pragma was encountered.
                    if opt in control_pragmas:
                        self._pragma_lineno[msgid] = start[0]

                    try:
                        if (opt, msgid) == ('disable', 'all'):
                            self.add_message('deprecated-pragma', line=start[0],
                                             args=('disable=all', 'skip-file'))
                            self.add_message('file-ignored', line=start[0])
                            self._ignore_file = True
                            return
                        comments_sharp_sep = content.split('#')[1:]
                        first_comment = "#" + comments_sharp_sep[0]
                        first_comment_match_disable = utils.OPTION_RGX.search(first_comment)
                        # Deactivate msg emission for whole module only if
                        # we are sure the disable directive is the first comment.
                        # If not then it refers to the comment before
                        # and not to the module itself.
                        if first_comment_match_disable:
                            meth(msgid, 'module', start[0])
                    except exceptions.UnknownMessageError:
                        self.add_message('bad-option-value', args=msgid, line=start[0])
            else:
                self.add_message('unrecognized-inline-option', args=opt, line=start[0])


    # code checking methods ###################################################

    def check(self, module_desc, walker, rawcheckers, tokencheckers):
        modname = module_desc.name
        filepath = module_desc.path
        self.set_current_module(modname, filepath)
        # get the module representation
        ast_node = self.get_ast(filepath, modname)
        if ast_node is None:
            return
        # XXX to be correct we need to keep module_msgs_state for every
        # analyzed module (the problem stands with localized messages which
        # are only detected in the .close step)
        self.file_state = utils.FileState(module_desc.basename)
        self._ignore_file = False
        # fix the current file (if the source file was not available or
        # if it's actually a c extension)
        self.current_file = ast_node.file # pylint: disable=maybe-no-member
        self.check_astroid_module(ast_node, walker, rawcheckers, tokencheckers)
        # warn about spurious inline messages handling
        spurious_messages = self.file_state.iter_spurious_suppression_messages(self.msgs_store)
        for msgid, line, args in spurious_messages:
            self.add_message(msgid, line, None, args)

    def set_current_module(self, modname, filepath=None):
        """set the name of the currently analyzed module and
        init statistics for it
        """
        if not modname and filepath is None:
            return
        self.reporter.on_set_current_module(modname, filepath)
        self.current_name = modname
        self.current_file = filepath or modname
        self.stats['by_module'][modname] = {}
        self.stats['by_module'][modname]['statement'] = 0
        for msg_cat in utils.MSG_TYPES.values():
            self.stats['by_module'][modname][msg_cat] = 0

    def get_ast(self, filepath, modname):
        """return an ast(roid) representation for a module"""
        try:
            return MANAGER.ast_from_file(filepath, modname, source=True)
        except astroid.AstroidSyntaxError as ex:
            # pylint: disable=no-member
            self.add_message('syntax-error',
                             line=getattr(ex.error, 'lineno', 0),
                             args=str(ex.error))
        except astroid.AstroidBuildingException as ex:
            self.add_message('parse-error', args=ex)
        except Exception as ex:
            import traceback
            traceback.print_exc()
            self.add_message('astroid-error', args=(ex.__class__, ex))

    def check_astroid_module(self, ast_node, walker,
                             rawcheckers, tokencheckers):
        """Check a module from its astroid representation."""
        try:
            tokens = utils.tokenize_module(ast_node)
        except tokenize.TokenError as ex:
            self.add_message('syntax-error', line=ex.args[1][0], args=ex.args[0])
            return None

        if not ast_node.pure_python:
            self.add_message('raw-checker-failed', args=ast_node.name)
        else:
            #assert astroid.file.endswith('.py')
            # invoke ITokenChecker interface on self to fetch module/block
            # level options
            self.process_tokens(tokens)
            if self._ignore_file:
                return False
            # walk ast to collect line numbers
            self.file_state.collect_block_lines(self.msgs_store, ast_node)
            # run raw and tokens checkers
            for checker in rawcheckers:
                checker.process_module(ast_node)
            for checker in tokencheckers:
                checker.process_tokens(tokens)
        # generate events to astroid checkers
        walker.walk(ast_node)
        return True

    def open(self):
        self._init_msg_states()

    def add_stats(self, **kwargs):
        """add some stats entries to the statistic dictionary
        raise an AssertionError if there is a key conflict
        """
        for key, value in kwargs.items():
            if key[-1] == '_':
                key = key[:-1]
            assert key not in self.stats
            self.stats[key] = value
        return self.stats


# utilities ###################################################################


@contextlib.contextmanager
def fix_import_path(args):
    """Prepare sys.path for running the linter checks.
    Within this context, each of the given arguments is importable.
    Paths are added to sys.path in corresponding order to the arguments.
    We avoid adding duplicate directories to sys.path.
    `sys.path` is reset to its original value upon exiting this context.
    """
    orig = list(sys.path)
    changes = []
    for arg in args:
        path = _get_python_path(arg)
        if path in changes:
            continue
        else:
            changes.append(path)
    sys.path[:] = changes + ["."] + sys.path
    try:
        yield
    finally:
        sys.path[:] = orig


def guess_lint_path(args):
    """Attempt to determine the file being linted from a list of arguments.

    :param args: The list of command line arguments to guess from.
    :type args: list(str)

    :returns: The path to file being linted if it can be guessed.
        None otherwise.
    :rtype: str or None
    """
    value = None

    # We only care if it's a path. If it's a module,
    # we can't get a config from it
    if args and os.path.exists(args[-1]):
        value = args[-1]

    return value


class ReportRegistry:

    def __init__(self):
        self.reports = collections.defaultdict(list)
        self._reports_state = {}
        super().__init__()

    def register_report(self, reportid, r_title, r_cb, checker):
        """Register a report

        :param reportid: The unique identifier for the report.
        :type reportid: str
        :param r_title: The report's title.
        :type r_title: str
        :param r_cb: The method to call to make the report.
        :type r_cb: callable
        :param checker: The checker defining the report.
        :type checker: BaseChecker
        """
        reportid = reportid.upper()
        self.reports[checker].append((reportid, r_title, r_cb))

    def enable_report(self, reportid):
        """Enable the report of the given id.

        :param reportid: The unique identifier of the report to enable.
        :type reportid: str
        """
        reportid = reportid.upper()
        self._reports_state[reportid] = True

    def disable_report(self, reportid):
        """Disable the report of the given id.

        :param reportid: The unique identifier of the report to disable.
        :type reportid: str
        """
        reportid = reportid.upper()
        self._reports_state[reportid] = False

    def disable_reporters(self):
        """Disable all reporters."""
        for _reporters in self.reports.values():
            for report_id, _, _ in _reporters:
                self.disable_report(report_id)

    def report_is_enabled(self, reportid):
        """Check if the report with the given id is enabled.

        :param reportid: The unique identifier of the report to check.
        :type reportid: str

        :returns: True if the report is enabled, False otherwise.
        :rtype: bool
        """
        return self._reports_state.get(reportid, True)


class PluginRegistry(utils.MessagesHandlerMixIn, ReportRegistry):
    """A class to register checkers to."""

    def __init__(self, config, register_options=(lambda options: None)):
        super().__init__(config)
        self.register_options = register_options
        self._checkers = collections.defaultdict(list)
        self._reporters = {}

        self._python3_porting_mode = False
        self._error_mode = False

        for r_id, r_title, r_cb in PyLinter.reports:
            self.register_report(r_id, r_title, r_cb, PyLinter)

        self.register_options(PyLinter.options)

        self.msgs_store.register_messages(PyLinter)

    def for_all_checkers(self):
        """Loop through all registered checkers.

        :returns: Each registered checker.
        :rtype: iterable(BaseChecker)
        """
        for checkers in self._checkers.values():
            yield from checkers

    def register_checker(self, checker):
        """Register a checker.

        :param checker: The checker to register.
        :type checker: BaseChecker

        :raises InvalidCheckerError: If the priority of the checker is
            invalid.
        """
        # Allow instances to be passed for backwards compatibility
        if isinstance(checker, checkers.BaseChecker):
            checker = checker.__class__

        existing_checker_types = set(
            existing_checker
            for name_checkers in self._checkers.values()
            for existing_checker in name_checkers
        )
        if checker in existing_checker_types:
            msg_fmt = (
                'Not registering checker {}. A checker of type {} has '
                'already been registered.'
            )
            msg = msg_fmt.format(checker.name, checker.__name__)
            warnings.warn(msg)
            return

        if checker.priority > 0:
             msg = '{}.priority must be <= 0'.format(checker.__class__)
             raise exceptions.InvalidCheckerError(msg)

        self._checkers[checker.name].append(checker)

        for r_id, r_title, r_cb in checker.reports:
            self.register_report(r_id, r_title, r_cb, checker)

        self.register_options(checker.options)

        if hasattr(checker, 'msgs'):
            self.msgs_store.register_messages(checker)

        # Register the checker, but disable all of its messages.
        # TODO(cpopa): we should have a better API for this.
        if not getattr(checker, 'enabled', True):
            self.disable(checker.name)

    def register_reporter(self, reporter_class):
        if reporter_class.name in self._reporters:
            # TODO: Raise if classes are the same
            duplicate = self._reporters[reporter_class.name]
            msg = 'A reporter called {} has already been registered ({}).'
            msg = msg.format(reporter.name, duplicate.__class__)
            warnings.warn(msg)

        self._reporters[reporter_class.name] = reporter_class

    def disable(self, msgid, scope='package', line=None, ignore_unknown=False):
        """Do not output messages that have the given ID.

        :param msgid: The ID of the message to disable.
            This can also be "all" to disable all messages,
            the ID of a category to disable all messages of that category,
            or the name of a checker to disable all messages from the checker.
        :type msgid: str

        :param scope: Must be "package". Provided for backwards compatibility.
        :type scope: str.

        :param line: The line number that the message is disabled on.
            This is not used and is provided for backwards compatibility only.
        :type line: int

        :param ignore_unknown: If this is False,
            an :exc:`UnknownMessageError` is raised when a message with the
            given ID cannot be found.
            If this is True, the exception is not raised.
        :param ignore_unknown: bool

        :raises ValueError: If `scope` is anything other than "package".
        """
        self._set_msg_status(
            msgid,
            enable=False,
            scope=scope,
            line=line,
            ignore_unknown=ignore_unknown,
        )

    def enable(self, msgid, scope='package', line=None, ignore_unknown=False):
        """Enable outputting messages that have the given ID.

        :param msgid: The ID of the message to enable.
            This can also be "all" to enable all messages,
            the ID of a category to enable all messages of that category,
            or the name of a checker to enable all messages from the checker.
        :type msgid: str

        :param scope: Must be "package". Provided for backwards compatibility.
        :type scope: str.

        :param line: The line number that the message is enabled on.
            This is not used and is provided for backwards compatibility only.
        :type line: int

        :param ignore_unknown: If this is False,
            an :exc:`UnknownMessageError` is raised when a message with the
            given ID cannot be found.
            If this is True, the exception is not raised.
        :param ignore_unknown: bool

        :raises ValueError: If `scope` is anything other than "package".
        """
        self._set_msg_status(
            msgid,
            enable=True,
            scope=scope,
            line=line,
            ignore_unknown=ignore_unknown,
        )

    def error_mode(self):
        """Enable only errors; no reports, no persistent"""
        self._error_mode = True
        self.disable_noerror_messages()
        self.disable('miscellaneous')
        if self._python3_porting_mode:
            self.disable('all')
            for msg_id in self._checker_messages('python3'):
                if msg_id.startswith('E'):
                    self.enable(msg_id)
        else:
            self.disable('python3')

    def python3_porting_mode(self):
        """Disable all other checkers and enable Python 3 warnings."""
        self.disable('all')
        self.enable('python3')
        if self._error_mode:
            # The error mode was activated, using the -E flag.
            # So we'll need to enable only the errors from the
            # Python 3 porting checker.
            for msg_id in self._checker_messages('python3'):
                if msg_id.startswith('E'):
                    self.enable(msg_id)
                else:
                    self.disable(msg_id)
        self._python3_porting_mode = True


class Runner(object):
    """A class to manager how the linter runs."""

    option_definitions = ()
    """The runner specific configuration options.

    :type: set(OptionDefinition)
    """


class CLIRunner(Runner):
    option_definitions = (
        ('module_or_package',
         {'positional': True,
          'nargs': argparse.REMAINDER}),

        ('rcfile',
         {'type': 'string', 'metavar': '<file>',
          'help' : 'Specify a configuration file.'}),

        ('init-hook',
         {'type' : 'string', 'metavar': '<code>',
          'level': 1,
          'help' : 'Python code to execute, usually for sys.path '
          'manipulation such as pygtk.require().'}),

        ('help-msg',
         {'type' : 'string', 'metavar': '<msg-id>',
          'group': 'Commands', 'default': None,
          'help' : 'Display a help message for the given message id and '
          'exit. The value may be a comma separated list of message ids.'}),

        ('list-msgs',
         {'group': 'Commands', 'level': 1,
          'action': 'store_true', 'default': False,
          'help' : "Generate pylint's messages."}),

        ('list-conf-levels',
         {'group': 'Commands', 'level': 1,
          'action': 'store_true', 'default': False,
          'help' : "Generate pylint's confidence levels."}),

        ('full-documentation',
         {'metavar': '<msg-id>', 'default': None,
          'group': 'Commands', 'level': 1,
          'help' : "Generate pylint's full documentation."}),

        ('generate-rcfile',
         {'group': 'Commands', 'action': 'store_true', 'default': False,
          'help' : 'Generate a sample configuration file according to '
          'the current configuration. You can put other options '
          'before this one to get them in the generated '
          'configuration.'}),

        ('generate-man',
         {'group': 'Commands', 'action': 'store_true', 'default': False,
          'help' : "Generate pylint's man page.", 'hide': True}),

        ('errors-only',
         {'short': 'E', 'action': 'store_true', 'default': False,
          'help' : 'In error mode, checkers without error messages are '
          'disabled and for others, only the ERROR messages are '
          'displayed, and no reports are done by default'''}),

        ('py3k',
         {'action': 'store_true', 'default': False,
          'help' : 'In Python 3 porting mode, all checkers will be '
          'disabled and only messages emitted by the porting '
          'checker will be displayed'}),

        ('version',
         {'group': 'Commands', 'action': 'version', 'version': FULL_VERSION,
          'help': 'Print the version of pylint and important '
          'dependencies'}),
    )

    option_groups = (
        ('Commands', 'Options which are actually commands. Options in this \
group are mutually exclusive.'),
        )

    description = (
        'pylint [options] module_or_package\n'
        '\n'
        '  Check that a module satisfies a coding standard (and more !).\n'
        '\n'
        '    pylint --help\n'
        '\n'
        '  Display this help message and exit.\n'
        '\n'
        '    pylint --help-msg <msg-id>[,<msg-id>]\n'
        '\n'
        '  Display help messages about given message identifiers and exit.\n'
    )

    def __init__(self):
        super().__init__()
        self._global_config = config.Configuration()
        self._plugin_registry = PluginRegistry(self._global_config)
        self._loaded_plugins = set()
        self._reporter = None
        self._config_parsers = []

    def run(self, args):
        # Phase 1: Preprocessing
        option_definitions = self.option_definitions + PyLinter.options
        parser = config.CLIParser(self.description)
        parser.add_option_definitions(option_definitions)
        parser.add_help_section('Environment variables', config.ENV_HELP, level=1)
        # pylint: disable=bad-continuation
        parser.add_help_section('Output',
'Using the default text output, the message format is :                          \n'
'                                                                                \n'
'        MESSAGE_TYPE: LINE_NUM:[OBJECT:] MESSAGE                                \n'
'                                                                                \n'
'There are 5 kind of message types :                                             \n'
'    * (C) convention, for programming standard violation                        \n'
'    * (R) refactor, for bad code smell                                          \n'
'    * (W) warning, for python specific problems                                 \n'
'    * (E) error, for probable bugs in the code                                  \n'
'    * (F) fatal, if an error occurred which prevented pylint from doing further\n'
'processing.\n'
                                , level=1)
        parser.add_help_section('Output status code',
'Pylint should leave with following status code:                                 \n'
'    * 0 if everything went fine                                                 \n'
'    * 1 if a fatal message was issued                                           \n'
'    * 2 if an error message was issued                                          \n'
'    * 4 if a warning message was issued                                         \n'
'    * 8 if a refactor message was issued                                        \n'
'    * 16 if a convention message was issued                                     \n'
'    * 32 on usage error                                                         \n'
'                                                                                \n'
'status 1 to 16 will be bit-ORed so you can know which different categories has\n'
'been issued by analysing pylint output status code\n',
                                level=1)

        self._global_config.add_options(option_definitions)

        parsed = parser.preprocess(
            args,
            'init_hook',
            'rcfile',
            'load_plugins',
        )

        # Call init-hook
        if parsed.init_hook:
            exec(parsed.init_hook)

        # Load rcfile, else system rcfile
        file_parser = config.IniFileParser()
        file_parser.add_option_definitions(PyLinter.options)
        rcfile = parsed.rcfile or config.PYLINTRC
        if rcfile:
            file_parsed = file_parser.preprocess(
                rcfile, 'init_hook', 'load_plugins',
            )
            if file_parsed.init_hook:
                exec(file_parsed.init_hook)
            if file_parsed.load_plugins:
                old_value = getattr(parsed, 'load_plugins', [])
                parsed.load_plugins = old_value + file_parsed.load_plugins

        def register_options(options):
            self._global_config.add_options(options)
            parser.add_option_definitions(options)
            file_parser.add_option_definitions(options)
        self._plugin_registry.register_options = register_options
        self._file_parser = file_parser
        self._cli_parser = parser

        checkers.initialize(self._plugin_registry)

        # Load plugins from CLI
        plugins = parsed.load_plugins or []
        for plugin in plugins:
            self.load_plugin(plugin)

        # TODO: This is for per directory config support (#618)
        # Phase 2: Discover more plugins found in config files
        # Walk and discover config files, watching for blacklists as we go

        # Load plugins from config files

        # Phase 3: Full load
        # Fully load config files
        if rcfile:
            file_parser.parse(rcfile, self._global_config)
        # Fully load CLI into global config
        self._cli_config = config.Configuration()
        parser.parse(args, self._cli_config)
        self._global_config += self._cli_config

        if self._global_config.generate_rcfile:
            file_parser.write()
            sys.exit(0)

        # TODO: if global_config.generate_man

        if self._global_config.errors_only:
            self._plugin_registry.error_mode()
            if file_parser.has_option('MESSAGES CONTROL', 'disable'):
                value = file_parser.get('MESSAGES CONTROL', 'disable')
                self.config.set_option('disable', value)
            self._global_config.reports = False
            self._global_config.persistent = False
            self._global_config.score = False

        if self._global_config.py3k:
            self._plugin_registry.python3_porting_mode()
            if file_parser.has_option('MESSAGES CONTROL', 'disable'):
                value = file_parser.get('MESSAGES CONTROL', 'disable')
                self._global_config.set_option('disable', value)

        if self._global_config.full_documentation:
            self._plugin_registry.print_full_documentation()
            sys.exit(0)

        if self._global_config.list_conf_levels:
            for level in interfaces.CONFIDENCE_LEVELS:
                print('%-18s: %s' % level)
            sys.exit(0)

        if self._global_config.list_msgs:
            self._plugin_registry.msgs_store.list_messages()
            sys.exit(0)

        if self._global_config.help_msg:
            msg = utils._splitstrip(self._global_config.help_msg)
            self._plugin_registry.msgs_store.help_message(msg)
            sys.exit(0)

        self.load_default_plugins()

        self._plugin_registry.disable('I')
        self._plugin_registry.enable('c-extension-no-member')

        for checker in self._plugin_registry.for_all_checkers():
            checker.config = self._global_config

        if not self._global_config.reports:
            self._plugin_registry.disable_reporters()

        with fix_import_path(self._global_config.module_or_package):
            assert self._global_config.jobs == 1
            base_name, status_code = self.check(
                self._global_config.module_or_package,
            )

            self.generate_reports(base_name)

        if self._global_config.exit_zero:
            sys.exit(0)
        else:
            sys.exit(status_code)

    def load_plugin(self, module_name):
        if module_name in self._loaded_plugins:
            msg = 'Already loaded plugin {0}. Ignoring'.format(module_name)
            warnings.warn(msg)
        else:
            module = astroid.modutils.load_module_from_name(module_name)
            module.register(self._plugin_registry)

    def load_plugins(self, module_names):
        """Load a plugin.

        Args:
            module_names (list(str)): The name of plugin modules to load.
        """
        for module_name in module_names:
            self.load_plugin(module_name)

    def load_default_plugins(self):
        """Load all of the default plugins."""
        reporters.initialize(self._plugin_registry)
        # Make sure to load the default reporter, because
        # the option has been set before the plugins had been loaded.
        if not self._reporter:
            self.load_reporter()

    def load_reporter(self):
        name = self._global_config.output_format.lower()
        if name in self._plugin_registry._reporters:
            self._reporter = self._plugin_registry._reporters[name](
                config=self._global_config,
            )
            self._plugin_registry.reporter = self._reporter
        else:
            try:
                reporter_class = self._load_reporter_class()
            except (ImportError, AttributeError):
                raise exceptions.InvalidReporterError(name)
            else:
                self._reporter = reporter_class(config=self._global_config)
                self._plugin_registry.reporter = self._reporter

    def _load_reporter_class(self):
        qname = self._global_config.output_format
        module = modutils.load_module_from_name(
            modutils.get_module_part(qname)
        )
        class_name = qname.split('.')[-1]
        reporter_class = getattr(module, class_name)
        return reporter_class

    def generate_reports(self, base_name):
        """close the whole package /module, it's time to make reports !

        if persistent run, pickle results for later comparison
        """
        # Display whatever messages are left on the reporter.
        self._reporter.display_messages(report_nodes.Section())

        if base_name is not None:
            # load previous results if any
            previous_stats = config.load_results(base_name)
            # XXX code below needs refactoring to be more reporter agnostic
            self._reporter.on_close(self._plugin_registry.stats, previous_stats)
            if self._global_config.reports:
                sect = self.make_reports(self._plugin_registry.stats, previous_stats)
            else:
                sect = report_nodes.Section()

            if self._global_config.reports:
                self._reporter.display_reports(sect)
            self._report_evaluation(base_name)
            # save results if persistent run
            if self._global_config.persistent:
                config.save_results(self._plugin_registry.stats, base_name)
        else:
            self._reporter.on_close(self._plugin_registry.stats, {})

    def report_order(self):
        """A list of reports, sorted in the order in which they must be called.

        :returns: The list of reports.
        :rtype: list(BaseChecker or object)
        """
        reports = self._plugin_registry.reports
        reports = sorted(reports, key=lambda x: getattr(x, 'name', ''))
        try:
            reports.remove(PyLinter)
        except ValueError:
            pass
        else:
            reports.append(PyLinter)
        return reports

    def make_reports(self, stats, old_stats):
        """Render the registered reports.

        :param stats: The statistics dictionary for this run.
        :type stats: dict
        :param old_stats: The statistics dictionary for the previous run.
        :type old_stats: dict

        :returns: The complete report.
        :rtype: pylint.reporters.ureports.nodes.Section
        """
        sect = report_nodes.Section('Report',
                       '%s statements analysed.'% (stats['statement']))
        for checker in self.report_order():
            for reportid, r_title, r_cb in self._plugin_registry.reports[checker]:
                if not self.report_is_enabled(reportid):
                    continue
                report_sect = report_nodes.Section(r_title)
                try:
                    r_cb(report_sect, stats, old_stats)
                except EmptyReportError:
                    continue
                report_sect.report_id = reportid
                sect.append(report_sect)
        return sect

    def _report_evaluation(self, base_name):
        """make the global evaluation report"""
        # check with at least check 1 statements (usually 0 when there is a
        # syntax error preventing pylint from further processing)
        previous_stats = config.load_results(base_name)
        if self._plugin_registry.stats['statement'] == 0:
            return

        # get a global note for the code
        evaluation = self._global_config.evaluation
        try:
            note = eval(evaluation, {}, self._plugin_registry.stats) # pylint: disable=eval-used
        except Exception as ex:
            msg = 'An exception occurred while rating: %s' % ex
        else:
            self._plugin_registry.stats['global_note'] = note
            msg = 'Your code has been rated at %.2f/10' % note
            pnote = previous_stats.get('global_note')
            if pnote is not None:
                msg += ' (previous run: %.2f/10, %+.2f)' % (pnote, note - pnote)

        if self._global_config.score:
            sect = report_nodes.EvaluationSection(msg)
            self._reporter.display_reports(sect)

    def get_checkers(self):
        """return all available checkers as a list"""
        return [
            c for c in self._plugin_registry.for_all_checkers()
        ]

    def prepare_checkers(self, linter):
        """return checkers needed for activated messages and reports"""
        # get needed checkers
        neededcheckers = []
        for checker in self.get_checkers()[1:]:
            messages = set(msg for msg in checker.msgs
                           if linter.is_message_enabled(msg))
            if (messages or
                    any(self._plugin_registry.report_is_enabled(r[0]) for r in checker.reports)):
                neededcheckers.append(checker)
        # Sort checkers by priority
        neededcheckers = sorted(neededcheckers,
                                key=operator.attrgetter('priority'),
                                reverse=True)
        return neededcheckers

    # pylint: disable=unused-argument
    @staticmethod
    def should_analyze_file(modname, path, is_argument=False):
        """Returns whether or not a module should be checked.

        This implementation returns True for all python source files,
        indicating that all files should be linted.

        Subclasses may override this method to indicate that modules satisfying
        certain conditions should not be linted.

        :param str modname: The name of the module to be checked.
        :param str path: The full path to the source code of the module.
        :param bool is_argument: Whetter the file is an argument to pylint or not.
                                 Files which respect this property are always
                                 checked, since the user requested it explicitly.
        :returns: True if the module should be checked.
        :rtype: bool
        """
        if is_argument:
            return True
        return path.endswith('.py')
    # pylint: enable=unused-argument

    def close_registration(self):
        """Stop registering plugins and prepare everything for checking."""
        MANAGER.always_load_extensions = self._global_config.unsafe_load_any_extension
        MANAGER.max_inferable_values = self._global_config.limit_inference_results
        MANAGER.extension_package_whitelist.update(
            self._global_config.extension_pkg_whitelist
        )

    def check(self, files_or_modules):
        """main checking entry: check a list of files or modules from their
        name.
        """
        # initialize msgs_state now that all messages have been registered into the store
        self.close_registration()

        if not isinstance(files_or_modules, (list, tuple)):
            files_or_modules = (files_or_modules,)

        # notify global begin
        all_stats = [self._plugin_registry.stats]
        # build ast and check modules or packages
        expanded_files = utils.expand_files(
            files_or_modules,
            self._plugin_registry,
            self._global_config.black_list,
            self._global_config.black_list_re
        )
        config_store = config.ConfigurationStore()
        for module_desc in expanded_files:
            directory = os.path.dirname(module_desc.path)

            local_config = config_store[directory]
            if not local_config:
                local_file = config.find_nearby_pylintrc(directory)
                if not local_file:
                    local_config = self._global_config
                else:
                    local_config = self._global_config.copy()
                    self._file_parser.parse(local_file, local_config)
                    local_config += self._cli_config

            config_store[directory] = local_config

        for module_desc in expanded_files:
            modname = module_desc.name
            filepath = module_desc.path
            if not module_desc.isarg and not self.should_analyze_file(modname, filepath):
                continue

            directory = os.path.dirname(module_desc.path)
            local_config = config_store.get_config_for(directory)
            linter = PyLinter(local_config)
            linter.msgs_store = self._plugin_registry.msgs_store
            for msg_ids, enable in local_config.msg_toggles:
                for msg_id in msg_ids:
                    if enable:
                        linter.enable(msg_id, scope='directory')
                    else:
                        linter.disable(msg_id, scope='directory')
            linter.open()

            walker = utils.PyLintASTWalker(self._plugin_registry)
            allcheckers = []
            tokencheckers = [linter]
            rawcheckers = []
            for checker_cls in self.prepare_checkers(linter):
                checker = checker_cls(linter)
                checker.linter = linter
                checker.open()
                allcheckers.append(checker)
                if interfaces.implements(checker, interfaces.ITokenChecker):
                    tokencheckers.append(checker)
                if interfaces.implements(checker, interfaces.IRawChecker):
                    rawcheckers.append(checker)
                if interfaces.implements(checker, interfaces.IAstroidChecker):
                    walker.add_checker(checker)

            linter.reporter = self._reporter
            linter.check(module_desc, walker, rawcheckers, tokencheckers)
            self._plugin_registry.stats['statement'] += walker.nbstatements
            all_stats.append(linter.stats)

            for checker in reversed(allcheckers):
                checker.close()

        self._plugin_registry.stats = _merge_stats(all_stats)

        return module_desc.basename, linter.msg_status


if __name__ == '__main__':
     CLIRunner().run(sys.argv[1:])
