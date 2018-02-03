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


MANAGER = astroid.MANAGER


def _get_new_args(message):
    location = (
        message.abspath,
        message.path,
        message.module,
        message.obj,
        message.line,
        message.column,
    )
    return (message.msg_id, message.symbol, location, message.msg, message.confidence)


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
    for stat in stats:
        message_stats = stat.pop("by_msg", {})
        by_msg.update(message_stats)

        for key, item in stat.items():
            if key not in merged:
                merged[key] = item
            else:
                if isinstance(item, dict):
                    merged[key].update(item)
                else:
                    merged[key] = merged[key] + item

    merged["by_msg"] = by_msg
    return merged


# Python Linter class #########################################################

MSGS = {
    "F0001": (
        "%s",
        "fatal",
        "Used when an error occurred preventing the analysis of a \
              module (unable to find it for instance).",
    ),
    "F0002": (
        "%s: %s",
        "astroid-error",
        "Used when an unexpected error occurred while building the "
        "Astroid  representation. This is usually accompanied by a "
        "traceback. Please report such errors !",
    ),
    "F0010": (
        "error while code parsing: %s",
        "parse-error",
        "Used when an exception occurred while building the Astroid "
        "representation which could be handled by astroid.",
    ),
    "I0001": (
        "Unable to run raw checkers on built-in module %s",
        "raw-checker-failed",
        "Used to inform that a built-in module has not been checked "
        "using the raw checkers.",
    ),
    "I0010": (
        "Unable to consider inline option %r",
        "bad-inline-option",
        "Used when an inline option is either badly formatted or can't "
        "be used inside modules.",
    ),
    "I0011": (
        "Locally disabling %s (%s)",
        "locally-disabled",
        "Used when an inline option disables a message or a messages category.",
    ),
    "I0013": (
        "Ignoring entire file",
        "file-ignored",
        "Used to inform that the file will not be checked",
    ),
    "I0020": (
        "Suppressed %s (from line %d)",
        "suppressed-message",
        "A message was triggered on a line, but suppressed explicitly "
        "by a disable= comment in the file. This message is not "
        "generated for messages that are ignored due to configuration "
        "settings.",
    ),
    "I0021": (
        "Useless suppression of %s",
        "useless-suppression",
        "Reported when a message is explicitly disabled for a line or "
        "a block of code, but never triggered.",
    ),
    "I0022": (
        'Pragma "%s" is deprecated, use "%s" instead',
        "deprecated-pragma",
        "Some inline pylint options have been renamed or reworked, "
        "only the most recent form should be used. "
        "NOTE:skip-all is only available with pylint >= 0.26",
        {"old_names": [("I0014", "deprecated-disable-all")]},
    ),
    "E0001": ("%s", "syntax-error", "Used when a syntax error is raised for a module."),
    "E0011": (
        "Unrecognized file option %r",
        "unrecognized-inline-option",
        "Used when an unknown inline option is encountered.",
    ),
    "E0012": (
        "Bad option value %r",
        "bad-option-value",
        "Used when a bad value for an inline option is encountered.",
    ),
}


# pylint: disable=too-many-instance-attributes
class PyLinter(
    utils.MessagesHandlerMixIn, utils.ReportsHandlerMixIn, checkers.BaseTokenChecker
):
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

    __implements__ = (interfaces.ITokenChecker,)

    name = "master"
    priority = 0
    level = 0
    msgs = MSGS

    options = (
        (
            "ignore",
            {
                "type": "csv",
                "metavar": "<file>,...",
                "dest": "black_list",
                "default": ("CVS",),
                "help": "Add files or directories to the blacklist. "
                "They should be base names, not paths.",
            },
        ),
        (
            "ignore-patterns",
            {
                "type": "regexp_csv",
                "metavar": "<pattern>,...",
                "dest": "black_list_re",
                "default": (),
                "help": "Add files or directories matching the regex patterns to the"
                " blacklist. The regex matches against base names, not paths.",
            },
        ),
        (
            "persistent",
            {
                "default": True,
                "type": "yn",
                "metavar": "<y_or_n>",
                "level": 1,
                "help": "Pickle collected data for later comparisons.",
            },
        ),
        (
            "load-plugins",
            {
                "type": "csv",
                "metavar": "<modules>",
                "default": (),
                "level": 1,
                "help": "List of plugins (as comma separated values of "
                "python modules names) to load, usually to register "
                "additional checkers.",
            },
        ),
        (
            "output-format",
            {
                "default": "text",
                "type": "string",
                "metavar": "<format>",
                "short": "f",
                "group": "Reports",
                "help": "Set the output format. Available formats are text,"
                " parseable, colorized, json and msvs (visual studio)."
                " You can also give a reporter class, e.g. mypackage.mymodule."
                "MyReporterClass.",
            },
        ),
        (
            "reports",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y_or_n>",
                "short": "r",
                "group": "Reports",
                "help": "Tells whether to display a full report or only the "
                "messages",
            },
        ),
        (
            "evaluation",
            {
                "type": "string",
                "metavar": "<python_expression>",
                "group": "Reports",
                "level": 1,
                "default": "10.0 - ((float(5 * error + warning + refactor + "
                "convention) / statement) * 10)",
                "help": "Python expression which should return a note less "
                "than 10 (10 is the highest note). You have access "
                "to the variables errors warning, statement which "
                "respectively contain the number of errors / "
                "warnings messages and the total number of "
                "statements analyzed. This is used by the global "
                "evaluation report (RP0004).",
            },
        ),
        (
            "score",
            {
                "default": True,
                "type": "yn",
                "metavar": "<y_or_n>",
                "short": "s",
                "group": "Reports",
                "help": "Activate the evaluation score.",
            },
        ),
        (
            "confidence",
            {
                "type": "multiple_choice",
                "metavar": "<levels>",
                "default": "",
                "choices": [c.name for c in interfaces.CONFIDENCE_LEVELS],
                "group": "Messages control",
                "help": "Only show warnings with the listed confidence levels."
                " Leave empty to show all. Valid levels: %s"
                % (", ".join(c.name for c in interfaces.CONFIDENCE_LEVELS),),
            },
        ),
        (
            "enable",
            {
                "type": "csv",
                "metavar": "<msg ids>",
                "short": "e",
                "group": "Messages control",
                "help": "Enable the message, report, category or checker with the "
                "given id(s). You can either give multiple identifier "
                "separated by comma (,) or put this option multiple time "
                "(only on the command line, not in the configuration file "
                "where it should appear only once). "
                'See also the "--disable" option for examples. ',
            },
        ),
        (
            "disable",
            {
                "type": "csv",
                "metavar": "<msg ids>",
                "short": "d",
                "group": "Messages control",
                "help": "Disable the message, report, category or checker "
                "with the given id(s). You can either give multiple identifiers"
                " separated by comma (,) or put this option multiple times "
                "(only on the command line, not in the configuration file "
                "where it should appear only once)."
                'You can also use "--disable=all" to disable everything first '
                "and then reenable specific checks. For example, if you want "
                "to run only the similarities checker, you can use "
                '"--disable=all --enable=similarities". '
                "If you want to run only the classes checker, but have no "
                "Warning level messages displayed, use"
                '"--disable=all --enable=classes --disable=W"',
            },
        ),
        (
            "msg-template",
            {
                "type": "string",
                "metavar": "<template>",
                "default": "",
                "group": "Reports",
                "help": (
                    "Template used to display messages. "
                    "This is a python new-style format string "
                    "used to format the message information. "
                    "See doc for all details"
                ),
            },
        ),
        (
            "jobs",
            {
                "type": "int",
                "metavar": "<n-processes>",
                "short": "j",
                "default": 1,
                "help": """Use multiple processes to speed up Pylint.""",
            },
        ),
        (
            "unsafe-load-any-extension",
            {
                "type": "yn",
                "metavar": "<yn>",
                "default": False,
                "hide": True,
                "help": (
                    "Allow loading of arbitrary C extensions. Extensions"
                    " are imported into the active Python interpreter and"
                    " may run arbitrary code."
                ),
            },
        ),
        (
            "extension-pkg-whitelist",
            {
                "type": "csv",
                "metavar": "<pkg>,...",
                "default": [],
                "help": (
                    "A comma-separated list of package or module names"
                    " from where C extensions may be loaded. Extensions are"
                    " loading into the active Python interpreter and may run"
                    " arbitrary code"
                ),
            },
        ),
        (
            "suggestion-mode",
            {
                "type": "yn",
                "metavar": "<yn>",
                "default": True,
                "help": (
                    "When enabled, pylint would attempt to guess common "
                    "misconfiguration and emit user-friendly hints instead "
                    "of false-positive error messages"
                ),
            },
        ),
        (
            "exit-zero",
            {
                "action": "store_true",
                "help": (
                    "Always return a 0 (non-error) status code, even if "
                    "lint errors are found. This is primarily useful in "
                    "continuous integration scripts."
                ),
            },
        ),
    )

    option_groups = (
        ("Messages control", "Options controlling analysis messages"),
        ("Reports", "Options related to output formatting and reporting"),
    )

    def __init__(self, config=None):
        # some stuff has to be done before ancestors initialization...
        #
        # messages store / checkers / reporter / astroid manager
        self.config = config
        self.msgs_store = utils.MessagesStore()
        self.reporter = None
        self._reporters = {}
        self._checkers = collections.defaultdict(list)
        self._pragma_lineno = {}
        self._ignore_file = False
        # visit variables
        self.file_state = utils.FileState()
        self.current_name = None
        self.current_file = None
        self.stats = None

        # TODO: Runner needs to give this to parser?
        full_version = "%%prog %s\nastroid %s\nPython %s" % (
            version,
            astroid_version,
            sys.version,
        )
        utils.MessagesHandlerMixIn.__init__(self)
        utils.ReportsHandlerMixIn.__init__(self)
        checkers.BaseTokenChecker.__init__(self)
        # provided reports
        self.reports = (
            ("RP0001", "Messages by category", report_total_messages_stats),
            (
                "RP0002",
                "% errors / warnings by module",
                report_messages_by_module_stats,
            ),
            ("RP0003", "Messages", report_messages_stats),
        )
        self._dynamic_plugins = set()
        self._python3_porting_mode = False
        self._error_mode = False

    def load_plugin_configuration(self):
        """Call the configuration hook for plugins

        This walks through the list of plugins, grabs the "load_configuration"
        hook, if exposed, and calls it to allow plugins to configure specific
        settings.
        """
        for modname in self._dynamic_plugins:
            module = modutils.load_module_from_name(modname)
            if hasattr(module, "load_configuration"):
                module.load_configuration(self)

    def load_reporter(self):
        name = self.config.output_format.lower()
        if name in self._reporters:
            self.set_reporter(self._reporters[name]())
        else:
            try:
                reporter_class = self._load_reporter_class()
            except (ImportError, AttributeError):
                raise exceptions.InvalidReporterError(name)
            else:
                self.set_reporter(reporter_class())

    def _load_reporter_class(self):
        qname = self.config.output_format
        module = modutils.load_module_from_name(modutils.get_module_part(qname))
        class_name = qname.split(".")[-1]
        reporter_class = getattr(module, class_name)
        return reporter_class

    def set_reporter(self, reporter):
        """set the reporter used to display messages and reports"""
        self.reporter = reporter
        reporter.linter = self

    def register_reporter(self, reporter_class):
        self._reporters[reporter_class.name] = reporter_class
        if reporter_class.name == self.config.output_format.lower():
            self.load_reporter()

    def report_order(self):
        reports = sorted(self._reports, key=lambda x: getattr(x, "name", ""))
        try:
            # Remove the current reporter and add it
            # at the end of the list.
            reports.pop(reports.index(self))
        except ValueError:
            pass
        else:
            reports.append(self)
        return reports

    # checkers manipulation methods ############################################

    def disable_noerror_messages(self):
        for msgcat, msgids in self.msgs_store._msgs_by_category.items():
            # enable only messages with 'error' severity and above ('fatal')
            if msgcat in ["E", "F"]:
                for msgid in msgids:
                    self.enable(msgid)
            else:
                for msgid in msgids:
                    self.disable(msgid)

    def disable_reporters(self):
        """disable all reporters"""
        for _reporters in self._reports.values():
            for report_id, _, _ in _reporters:
                self.disable_report(report_id)

    def error_mode(self):
        """error mode: enable only errors; no reports, no persistent"""
        self._error_mode = True
        self.disable_noerror_messages()
        self.disable("miscellaneous")
        if self._python3_porting_mode:
            self.disable("all")
            for msg_id in self._checker_messages("python3"):
                if msg_id.startswith("E"):
                    self.enable(msg_id)
            config_parser = self.cfgfile_parser
            if config_parser.has_option("MESSAGES CONTROL", "disable"):
                value = config_parser.get("MESSAGES CONTROL", "disable")
                self.global_set_option("disable", value)
        else:
            self.disable("python3")
        self.set_option("reports", False)
        self.set_option("persistent", False)
        self.set_option("score", False)

    def python3_porting_mode(self):
        """Disable all other checkers and enable Python 3 warnings."""
        self.disable("all")
        self.enable("python3")
        if self._error_mode:
            # The error mode was activated, using the -E flag.
            # So we'll need to enable only the errors from the
            # Python 3 porting checker.
            for msg_id in self._checker_messages("python3"):
                if msg_id.startswith("E"):
                    self.enable(msg_id)
                else:
                    self.disable(msg_id)
        config_parser = self.cfgfile_parser
        if config_parser.has_option("MESSAGES CONTROL", "disable"):
            value = config_parser.get("MESSAGES CONTROL", "disable")
            self.global_set_option("disable", value)
        self._python3_porting_mode = True

    # block level option handling #############################################
    #
    # see func_block_disable_msg.py test case for expected behaviour

    def process_tokens(self, tokens):
        """process tokens from the current module to search for module/block
        level options
        """
        options_methods = {"enable": self.enable, "disable": self.disable}
        control_pragmas = {"disable", "enable"}
        for (tok_type, content, start, _, _) in tokens:
            if tok_type != tokenize.COMMENT:
                continue
            match = utils.OPTION_RGX.search(content)
            if match is None:
                continue

            first_group = match.group(1)
            if (
                first_group.strip() == "disable-all"
                or first_group.strip() == "skip-file"
            ):
                if first_group.strip() == "disable-all":
                    self.add_message(
                        "deprecated-pragma",
                        line=start[0],
                        args=("disable-all", "skip-file"),
                    )
                self.add_message("file-ignored", line=start[0])
                self._ignore_file = True
                return
            try:
                opt, value = first_group.split("=", 1)
            except ValueError:
                self.add_message(
                    "bad-inline-option", args=first_group.strip(), line=start[0]
                )
                continue
            opt = opt.strip()
            if opt in options_methods:
                meth = options_methods[opt]
                for msgid in utils._splitstrip(value):
                    # Add the line where a control pragma was encountered.
                    if opt in control_pragmas:
                        self._pragma_lineno[msgid] = start[0]

                    try:
                        if (opt, msgid) == ("disable", "all"):
                            self.add_message(
                                "deprecated-pragma",
                                line=start[0],
                                args=("disable=all", "skip-file"),
                            )
                            self.add_message("file-ignored", line=start[0])
                            self._ignore_file = True
                            return
                        meth(msgid, "module", start[0])
                    except exceptions.UnknownMessageError:
                        self.add_message("bad-option-value", args=msgid, line=start[0])
            else:
                self.add_message("unrecognized-inline-option", args=opt, line=start[0])

    # code checking methods ###################################################

    def get_checkers(self):
        """return all available checkers as a list"""
        return [self] + [
            c
            for _checkers in self._checkers.values()
            for c in _checkers
            if c is not self
        ]

    def prepare_checkers(self):
        """return checkers needed for activated messages and reports"""
        if not self.config.reports:
            self.disable_reporters()
        # get needed checkers
        neededcheckers = [self]
        for checker in self.get_checkers()[1:]:
            messages = {msg for msg in checker.msgs if self.is_message_enabled(msg)}
            if messages or any(self.report_is_enabled(r[0]) for r in checker.reports):
                neededcheckers.append(checker)
        # Sort checkers by priority
        neededcheckers = sorted(
            neededcheckers, key=operator.attrgetter("priority"), reverse=True
        )
        return neededcheckers

    # pylint: disable=unused-argument
    @staticmethod
    def should_analyze_file(modname, path, is_argument=False):
        """Returns whether or not a module should be checked.

        This implementation returns True for all python source file, indicating
        that all files should be linted.

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
        return path.endswith(".py")

    # pylint: enable=unused-argument

    def _init_msg_states(self):
        for msg in self.msgs_store.messages:
            if not msg.may_be_emitted():
                self._msgs_state[msg.msgid] = False

    def check(self, files_or_modules):
        """main checking entry: check a list of files or modules from their
        name.
        """
        assert self.reporter, "A reporter has not been loaded"
        # initialize msgs_state now that all messages have been registered into
        # the store
        self._init_msg_states()

        if not isinstance(files_or_modules, (list, tuple)):
            files_or_modules = (files_or_modules,)

        self._do_check(files_or_modules)

    def _do_check(self, files_or_modules):
        walker = utils.PyLintASTWalker(self)
        _checkers = self.prepare_checkers()
        tokencheckers = [
            c
            for c in _checkers
            if interfaces.implements(c, interfaces.ITokenChecker) and c is not self
        ]
        rawcheckers = [
            c for c in _checkers if interfaces.implements(c, interfaces.IRawChecker)
        ]
        # notify global begin
        for checker in _checkers:
            checker.open()
            if interfaces.implements(checker, interfaces.IAstroidChecker):
                walker.add_checker(checker)
        # build ast and check modules or packages
        expanded_files = utils.expand_files(
            files_or_modules, self, self.config.black_list, self.config.black_list_re
        )
        for module_desc in expanded_files:
            modname = module_desc.name
            filepath = module_desc.path
            if not module_desc.isarg and not self.should_analyze_file(
                modname, filepath
            ):
                continue

            self.set_current_module(modname, filepath)
            # get the module representation
            ast_node = self.get_ast(filepath, modname)
            if ast_node is None:
                continue
            # XXX to be correct we need to keep module_msgs_state for every
            # analyzed module (the problem stands with localized messages which
            # are only detected in the .close step)
            self.file_state = utils.FileState(module_desc.basename)
            self._ignore_file = False
            # fix the current file (if the source file was not available or
            # if it's actually a c extension)
            self.current_file = ast_node.file  # pylint: disable=maybe-no-member
            self.check_astroid_module(ast_node, walker, rawcheckers, tokencheckers)
            # warn about spurious inline messages handling
            spurious_messages = self.file_state.iter_spurious_suppression_messages(
                self.msgs_store
            )
            for msgid, line, args in spurious_messages:
                self.add_message(msgid, line, None, args)
        # notify global end
        self.stats["statement"] = walker.nbstatements
        for checker in reversed(_checkers):
            checker.close()

    def set_current_module(self, modname, filepath=None):
        """set the name of the currently analyzed module and
        init statistics for it
        """
        if not modname and filepath is None:
            return
        self.reporter.on_set_current_module(modname, filepath)
        self.current_name = modname
        self.current_file = filepath or modname
        self.stats["by_module"][modname] = {}
        self.stats["by_module"][modname]["statement"] = 0
        for msg_cat in utils.MSG_TYPES.values():
            self.stats["by_module"][modname][msg_cat] = 0

    def get_ast(self, filepath, modname):
        """return an ast(roid) representation for a module"""
        try:
            return MANAGER.ast_from_file(filepath, modname, source=True)
        except astroid.AstroidSyntaxError as ex:
            # pylint: disable=no-member
            self.add_message(
                "syntax-error", line=getattr(ex.error, "lineno", 0), args=str(ex.error)
            )
        except astroid.AstroidBuildingException as ex:
            self.add_message("parse-error", args=ex)
        except Exception as ex:
            import traceback

            traceback.print_exc()
            self.add_message("astroid-error", args=(ex.__class__, ex))

    def check_astroid_module(self, ast_node, walker, rawcheckers, tokencheckers):
        """Check a module from its astroid representation."""
        try:
            tokens = utils.tokenize_module(ast_node)
        except tokenize.TokenError as ex:
            self.add_message("syntax-error", line=ex.args[1][0], args=ex.args[0])
            return None

        if not ast_node.pure_python:
            self.add_message("raw-checker-failed", args=ast_node.name)
        else:
            # assert astroid.file.endswith('.py')
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

    # IAstroidChecker interface #################################################

    def open(self):
        """initialize counters"""
        self.stats = {"by_module": {}, "by_msg": {}}
        MANAGER.always_load_extensions = self.config.unsafe_load_any_extension
        MANAGER.max_inferable_values = self.config.limit_inference_results
        MANAGER.extension_package_whitelist.update(self.config.extension_pkg_whitelist)
        for msg_cat in utils.MSG_TYPES.values():
            self.stats[msg_cat] = 0

    def generate_reports(self):
        """close the whole package /module, it's time to make reports !

        if persistent run, pickle results for later comparison
        """
        # Display whatever messages are left on the reporter.
        self.reporter.display_messages(report_nodes.Section())

        if self.file_state.base_name is not None:
            # load previous results if any
            previous_stats = config.load_results(self.file_state.base_name)
            # XXX code below needs refactoring to be more reporter agnostic
            self.reporter.on_close(self.stats, previous_stats)
            if self.config.reports:
                sect = self.make_reports(self.stats, previous_stats)
            else:
                sect = report_nodes.Section()

            if self.config.reports:
                self.reporter.display_reports(sect)
            self._report_evaluation()
            # save results if persistent run
            if self.config.persistent:
                config.save_results(self.stats, self.file_state.base_name)
        else:
            self.reporter.on_close(self.stats, {})

    def _report_evaluation(self):
        """make the global evaluation report"""
        # check with at least check 1 statements (usually 0 when there is a
        # syntax error preventing pylint from further processing)
        previous_stats = config.load_results(self.file_state.base_name)
        if self.stats["statement"] == 0:
            return

        # get a global note for the code
        evaluation = self.config.evaluation
        try:
            note = eval(evaluation, {}, self.stats)  # pylint: disable=eval-used
        except Exception as ex:
            msg = "An exception occurred while rating: %s" % ex
        else:
            self.stats["global_note"] = note
            msg = "Your code has been rated at %.2f/10" % note
            pnote = previous_stats.get("global_note")
            if pnote is not None:
                msg += " (previous run: %.2f/10, %+.2f)" % (pnote, note - pnote)

        if self.config.score:
            sect = report_nodes.EvaluationSection(msg)
            self.reporter.display_reports(sect)


# some reporting functions ####################################################


def report_total_messages_stats(sect, stats, previous_stats):
    """make total errors / warnings report"""
    lines = ["type", "number", "previous", "difference"]
    lines += checkers.table_lines_from_stats(
        stats, previous_stats, ("convention", "refactor", "warning", "error")
    )
    sect.append(report_nodes.Table(children=lines, cols=4, rheaders=1))


def report_messages_stats(sect, stats, _):
    """make messages type report"""
    if not stats["by_msg"]:
        # don't print this report when we didn't detected any errors
        raise exceptions.EmptyReportError()
    in_order = sorted(
        [
            (value, msg_id)
            for msg_id, value in stats["by_msg"].items()
            if not msg_id.startswith("I")
        ]
    )
    in_order.reverse()
    lines = ("message id", "occurrences")
    for value, msg_id in in_order:
        lines += (msg_id, str(value))
    sect.append(report_nodes.Table(children=lines, cols=2, rheaders=1))


def report_messages_by_module_stats(sect, stats, _):
    """make errors / warnings by modules report"""
    if len(stats["by_module"]) == 1:
        # don't print this report when we are analysing a single module
        raise exceptions.EmptyReportError()
    by_mod = collections.defaultdict(dict)
    for m_type in ("fatal", "error", "warning", "refactor", "convention"):
        total = stats[m_type]
        for module in stats["by_module"].keys():
            mod_total = stats["by_module"][module][m_type]
            if total == 0:
                percent = 0
            else:
                percent = float((mod_total) * 100) / total
            by_mod[module][m_type] = percent
    sorted_result = []
    for module, mod_info in by_mod.items():
        sorted_result.append(
            (
                mod_info["error"],
                mod_info["warning"],
                mod_info["refactor"],
                mod_info["convention"],
                module,
            )
        )
    sorted_result.sort()
    sorted_result.reverse()
    lines = ["module", "error", "warning", "refactor", "convention"]
    for line in sorted_result:
        # Don't report clean modules.
        if all(entry == 0 for entry in line[:-1]):
            continue
        lines.append(line[-1])
        for val in line[:-1]:
            lines.append("%.2f" % val)
    if len(lines) == 5:
        raise exceptions.EmptyReportError()
    sect.append(report_nodes.Table(children=lines, cols=5, rheaders=1))


# utilities ###################################################################


class ArgumentPreprocessingError(Exception):
    """Raised if an error occurs during argument preprocessing."""


def preprocess_options(args, search_for):
    """look for some options (keys of <search_for>) which have to be processed
    before others

    values of <search_for> are callback functions to call when the option is
    found
    """
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith("--"):
            try:
                option, val = arg[2:].split("=", 1)
            except ValueError:
                option, val = arg[2:], None
            try:
                cb, takearg = search_for[option]
            except KeyError:
                i += 1
            else:
                del args[i]
                if takearg and val is None:
                    if i >= len(args) or args[i].startswith("-"):
                        msg = "Option %s expects a value" % option
                        raise ArgumentPreprocessingError(msg)
                    val = args[i]
                    del args[i]
                elif not takearg and val is not None:
                    msg = "Option %s doesn't expects a value" % option
                    raise ArgumentPreprocessingError(msg)
                cb(option, val)
        else:
            i += 1


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


class CheckerRegistry(object):
    """A class to register checkers to."""

    def __init__(self, linter):
        super(CheckerRegistry, self).__init__()
        self.register_options = lambda options: None
        self._checkers = collections.defaultdict(list)
        # TODO: Remove. This is needed for the MessagesHandlerMixIn for now.
        linter._checkers = self._checkers
        self._linter = linter
        self.register_checker(linter)

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

        :raises ValueError: If the priority of the checker is invalid.
        """
        if checker.name in self._checkers:
            # TODO: Raise if classes are the same
            for duplicate in self._checkers[checker.name]:
                msg = "A checker called {} has already been registered ({})."
                msg = msg.format(checker.name, duplicate.__class__)
                warnings.warn(msg)

        if checker.priority > 0:
            # TODO: Use a custom exception
            msg = "{}.priority must be <= 0".format(checker.__class__)
            raise ValueError(msg)

        self._checkers[checker.name].append(checker)

        # TODO: Move elsewhere
        for r_id, r_title, r_cb in checker.reports:
            self._linter.register_report(r_id, r_title, r_cb, checker)

        self.register_options(checker.options)

        # TODO: Move elsewhere
        if hasattr(checker, "msgs"):
            self._linter.msgs_store.register_messages(checker)

        # Register the checker, but disable all of its messages.
        # TODO(cpopa): we should have a better API for this.
        if not getattr(checker, "enabled", True):
            self._linter.disable(checker.name)

    # For now simply defer missing attributs to the linter,
    # until we know what API we want.
    def __getattr__(self, attribute):
        return getattr(self._linter, attribute)


class Runner(object):
    """A class to manager how the linter runs."""

    option_definitions = ()
    """The runner specific configuration options.

    :type: set(OptionDefinition)
    """


class CLIRunner(Runner):
    option_definitions = (
        (
            "rcfile",
            {
                "type": "string",
                "metavar": "<file>",
                "help": "Specify a configuration file.",
            },
        ),
        (
            "init-hook",
            {
                "type": "string",
                "metavar": "<code>",
                "level": 1,
                "help": "Python code to execute, usually for sys.path "
                "manipulation such as pygtk.require().",
            },
        ),
        (
            "help-msg",
            {
                "type": "string",
                "metavar": "<msg-id>",
                "group": "Commands",
                "default": None,
                "help": "Display a help message for the given message id and "
                "exit. The value may be a comma separated list of message ids.",
            },
        ),
        (
            "list-msgs",
            {
                "metavar": "<msg-id>",
                "group": "Commands",
                "level": 1,
                "default": None,
                "help": "Generate pylint's messages.",
            },
        ),
        (
            "list-conf-levels",
            {
                "group": "Commands",
                "level": 1,
                "action": "store_true",
                "default": False,
                "help": "Generate pylint's confidence levels.",
            },
        ),
        (
            "full-documentation",
            {
                "metavar": "<msg-id>",
                "default": None,
                "group": "Commands",
                "level": 1,
                "help": "Generate pylint's full documentation.",
            },
        ),
        (
            "generate-rcfile",
            {
                "group": "Commands",
                "action": "store_true",
                "default": False,
                "help": "Generate a sample configuration file according to "
                "the current configuration. You can put other options "
                "before this one to get them in the generated "
                "configuration.",
            },
        ),
        (
            "generate-man",
            {
                "group": "Commands",
                "action": "store_true",
                "default": False,
                "help": "Generate pylint's man page.",
                "hide": True,
            },
        ),
        (
            "errors-only",
            {
                "short": "E",
                "action": "store_true",
                "default": False,
                "help": "In error mode, checkers without error messages are "
                "disabled and for others, only the ERROR messages are "
                "displayed, and no reports are done by default"
                "",
            },
        ),
        (
            "py3k",
            {
                "action": "store_true",
                "default": False,
                "help": "In Python 3 porting mode, all checkers will be "
                "disabled and only messages emitted by the porting "
                "checker will be displayed",
            },
        ),
    )

    option_groups = (
        (
            "Commands",
            "Options which are actually commands. Options in this \
group are mutually exclusive.",
        ),
    )

    description = (
        "pylint [options] module_or_package\n"
        "\n"
        "  Check that a module satisfies a coding standard (and more !).\n"
        "\n"
        "    pylint --help\n"
        "\n"
        "  Display this help message and exit.\n"
        "\n"
        "    pylint --help-msg <msg-id>[,<msg-id>]\n"
        "\n"
        "  Display help messages about given message identifiers and exit.\n"
    )

    def __init__(self):
        super(CLIRunner, self).__init__()
        self._linter = PyLinter()
        self._checker_registry = CheckerRegistry(self._linter)
        self._loaded_plugins = set()

    def run(self, args):
        # Phase 1: Preprocessing
        option_definitions = self.option_definitions + self._linter.options
        parser = config.CLIParser(self.description)
        parser.add_option_definitions(option_definitions)
        parser.add_help_section("Environment variables", config.ENV_HELP, level=1)
        # pylint: disable=bad-continuation
        parser.add_help_section(
            "Output",
            "Using the default text output, the message format is :                          \n"
            "                                                                                \n"
            "        MESSAGE_TYPE: LINE_NUM:[OBJECT:] MESSAGE                                \n"
            "                                                                                \n"
            "There are 5 kind of message types :                                             \n"
            "    * (C) convention, for programming standard violation                        \n"
            "    * (R) refactor, for bad code smell                                          \n"
            "    * (W) warning, for python specific problems                                 \n"
            "    * (E) error, for probable bugs in the code                                  \n"
            "    * (F) fatal, if an error occurred which prevented pylint from doing further\n"
            "processing.\n",
            level=1,
        )
        parser.add_help_section(
            "Output status code",
            "Pylint should leave with following status code:                                 \n"
            "    * 0 if everything went fine                                                 \n"
            "    * 1 if a fatal message was issued                                           \n"
            "    * 2 if an error message was issued                                          \n"
            "    * 4 if a warning message was issued                                         \n"
            "    * 8 if a refactor message was issued                                        \n"
            "    * 16 if a convention message was issued                                     \n"
            "    * 32 on usage error                                                         \n"
            "                                                                                \n"
            "status 1 to 16 will be bit-ORed so you can know which different categories has\n"
            "been issued by analysing pylint output status code\n",
            level=1,
        )

        global_config = config.Configuration()
        global_config.add_options(option_definitions)
        self._linter.config = global_config

        parsed = parser.preprocess(
            args, "init_hook", "rcfile", "load_plugins", "ignore", "ignore_patterns"
        )

        # Call init-hook
        if parsed.init_hook:
            exec(parsed.init_hook)

        # Load rcfile, else system rcfile
        file_parser = config.IniFileParser()
        file_parser.add_option_definitions(self._linter.options)
        rcfile = parsed.rcfile or config.PYLINTRC
        if rcfile:
            file_parser.parse(rcfile, global_config)

        def register_options(options):
            global_config.add_options(options)
            parser.add_option_definitions(options)
            file_parser.add_option_definitions(options)

        self._checker_registry.register_options = register_options

        checkers.initialize(self._checker_registry)

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
            file_parser.parse(rcfile, global_config)
        # Fully load CLI into global config
        parser.parse(args, global_config)

        if global_config.generate_rcfile:
            file_parser.write()
            sys.exit(0)

        # TODO: if global_config.generate_man

        if global_config.errors_only:
            self._linter.errors_mode()

        if global_config.py3k:
            self._linter.python3_porting_mode()

        if global_config.full_documentation:
            self._linter.print_full_documentation()
            sys.exit(0)

        if global_config.list_conf_levels:
            for level in interfaces.CONFIDENCE_LEVELS:
                print("%-18s: %s" % level)
            sys.exit(0)

        if global_config.list_msgs:
            self._linter.msgs_store.list_messages()
            sys.exit(0)

        if global_config.help_msg:
            msg = utils._splitstrip(global_config.help_msg)
            self._linter.msgs_store.help_message(msg)
            sys.exit(0)

        self.load_default_plugins()

        self._linter.disable("I")
        self._linter.enable("c-extension-no-member")

        for checker in self._checker_registry.for_all_checkers():
            checker.config = global_config

        with fix_import_path(global_config.module_or_package):
            assert self._linter.config.jobs == 1
            self._linter.check(global_config.module_or_package)

            self._linter.generate_reports()

        if linter.config.exit_zero:
            sys.exit(0)
        else:
            sys.exit(self.linter.msg_status)

    def load_plugin(self, module_name):
        if module_name in self._loaded_plugins:
            msg = "Already loaded plugin {0}. Ignoring".format(module_name)
            warnings.warn(msg)
        else:
            module = astroid.modutils.load_module_from_name(module_name)
            module.register(self._checker_registry)

    def load_plugins(self, module_names):
        """Load a plugin.

        Args:
            module_names (list(str)): The name of plugin modules to load.
        """
        for module_name in module_names:
            self.load_plugin(module_name)

    def load_default_plugins(self):
        """Load all of the default plugins."""
        reporters.initialize(self._linter)
        # Make sure to load the default reporter, because
        # the option has been set before the plugins had been loaded.
        if not self._linter.reporter:
            self._linter.load_reporter()


if __name__ == "__main__":
    CLIRunner().run(sys.argv[1:])
