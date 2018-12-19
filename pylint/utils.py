# -*- coding: utf-8 -*-
# Copyright (c) 2006-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2009 Vincent
# Copyright (c) 2009 Mads Kiilerich <mads@kiilerich.com>
# Copyright (c) 2012-2014 Google, Inc.
# Copyright (c) 2014-2018 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014-2015 Michal Nowikowski <godfryd@gmail.com>
# Copyright (c) 2014 LCD 47 <lcd047@gmail.com>
# Copyright (c) 2014 Brett Cannon <brett@python.org>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2014 Damien Nozay <damien.nozay@gmail.com>
# Copyright (c) 2015 Aru Sahni <arusahni@gmail.com>
# Copyright (c) 2015 Florian Bruhin <me@the-compiler.org>
# Copyright (c) 2015 Simu Toni <simutoni@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2016 Moises Lopez <moylop260@vauxoo.com>
# Copyright (c) 2016 Glenn Matthews <glenn@e-dad.net>
# Copyright (c) 2016 Glenn Matthews <glmatthe@cisco.com>
# Copyright (c) 2016 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2016 xmo-odoo <xmo-odoo@users.noreply.github.com>
# Copyright (c) 2017-2018 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2017 Pierre Sassoulas <pierre.sassoulas@cea.fr>
# Copyright (c) 2017 Bryce Guinta <bryce.paul.guinta@gmail.com>
# Copyright (c) 2017 Chris Lamb <chris@chris-lamb.co.uk>
# Copyright (c) 2017 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2017 Thomas Hisch <t.hisch@gmail.com>
# Copyright (c) 2017 Mikhail Fesenko <proggga@gmail.com>
# Copyright (c) 2017 Craig Citro <craigcitro@gmail.com>
# Copyright (c) 2017 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2018 Pierre Sassoulas <pierre.sassoulas@wisebim.fr>
# Copyright (c) 2018 Reverb C <reverbc@users.noreply.github.com>
# Copyright (c) 2018 Nick Drozd <nicholasdrozd@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""some various utilities and helper classes, most of them used in the
main pylint class
"""
from __future__ import print_function

import codecs
import collections
from inspect import cleandoc
import os
from os.path import dirname, basename, splitext, exists, isdir, join, normpath
import re
import sys
import tokenize
import warnings
import textwrap

from astroid import nodes, Module
from astroid import modutils

from pylint.interfaces import IRawChecker, ITokenChecker, UNDEFINED, implements
from pylint.reporters.ureports.nodes import Section
from pylint.exceptions import InvalidMessageError, UnknownMessageError, EmptyReportError


MSG_TYPES = {
    "I": "info",
    "C": "convention",
    "R": "refactor",
    "W": "warning",
    "E": "error",
    "F": "fatal",
}
MSG_TYPES_LONG = {v: k for k, v in MSG_TYPES.items()}

MSG_TYPES_STATUS = {"I": 0, "C": 16, "R": 8, "W": 4, "E": 2, "F": 1}

_MSG_ORDER = "EWRCIF"
MSG_STATE_SCOPE_CONFIG = 0
MSG_STATE_SCOPE_MODULE = 1
MSG_STATE_CONFIDENCE = 2

# Allow stopping after the first semicolon/hash encountered,
# so that an option can be continued with the reasons
# why it is active or disabled.
OPTION_RGX = re.compile(r"\s*#.*\bpylint:\s*([^;#]+)[;#]{0,1}")

# The line/node distinction does not apply to fatal errors and reports.
_SCOPE_EXEMPT = "FR"


class WarningScope:
    LINE = "line-based-msg"
    NODE = "node-based-msg"


_MsgBase = collections.namedtuple(
    "_MsgBase",
    [
        "msg_id",
        "symbol",
        "msg",
        "C",
        "category",
        "confidence",
        "abspath",
        "path",
        "module",
        "obj",
        "line",
        "column",
    ],
)


class Message(_MsgBase):
    """This class represent a message to be issued by the reporters"""

    def __new__(cls, msg_id, symbol, location, msg, confidence):
        return _MsgBase.__new__(
            cls,
            msg_id,
            symbol,
            msg,
            msg_id[0],
            MSG_TYPES[msg_id[0]],
            confidence,
            *location
        )

    def format(self, template):
        """Format the message according to the given template.

        The template format is the one of the format method :
        cf. http://docs.python.org/2/library/string.html#formatstrings
        """
        # For some reason, _asdict on derived namedtuples does not work with
        # Python 3.4. Needs some investigation.
        return template.format(**dict(zip(self._fields, self)))


def get_module_and_frameid(node):
    """return the module name and the frame id in the module"""
    frame = node.frame()
    module, obj = "", []
    while frame:
        if isinstance(frame, Module):
            module = frame.name
        else:
            obj.append(getattr(frame, "name", "<lambda>"))
        try:
            frame = frame.parent.frame()
        except AttributeError:
            frame = None
    obj.reverse()
    return module, ".".join(obj)


def category_id(cid):
    cid = cid.upper()
    if cid in MSG_TYPES:
        return cid
    return MSG_TYPES_LONG.get(cid)


def safe_decode(line, encoding, *args, **kwargs):
    """return decoded line from encoding or decode with default encoding"""
    try:
        return line.decode(encoding or sys.getdefaultencoding(), *args, **kwargs)
    except LookupError:
        return line.decode(sys.getdefaultencoding(), *args, **kwargs)


def decoding_stream(stream, encoding, errors="strict"):
    try:
        reader_cls = codecs.getreader(encoding or sys.getdefaultencoding())
    except LookupError:
        reader_cls = codecs.getreader(sys.getdefaultencoding())
    return reader_cls(stream, errors)


def tokenize_module(module):
    with module.stream() as stream:
        readline = stream.readline
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
        (msg, symbol, descr) = msg_tuple
    else:
        # messages should have a symbol, but for backward compatibility
        # they may not.
        (msg, descr) = msg_tuple
        warnings.warn(
            "[pylint 0.26] description of message %s doesn't include "
            "a symbolic name" % msgid,
            DeprecationWarning,
        )
        symbol = None
    options.setdefault("scope", default_scope)
    return MessageDefinition(checker, msgid, msg, descr, symbol, **options)


class MessageDefinition:
    def __init__(
        self,
        checker,
        msgid,
        msg,
        descr,
        symbol,
        scope,
        minversion=None,
        maxversion=None,
        old_names=None,
    ):
        self.checker = checker
        if len(msgid) != 5:
            raise InvalidMessageError("Invalid message id %r" % msgid)
        if not msgid[0] in MSG_TYPES:
            raise InvalidMessageError("Bad message type %s in %r" % (msgid[0], msgid))
        self.msgid = msgid
        self.msg = msg
        self.descr = descr
        self.symbol = symbol
        self.scope = scope
        self.minversion = minversion
        self.maxversion = maxversion
        self.old_names = old_names or []

    def __repr__(self):
        return "MessageDefinition:{}".format(self.__dict__)

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
            desc += " This message belongs to the %s checker." % self.checker.name
        title = self.msg
        if self.symbol:
            msgid = "%s (%s)" % (self.symbol, self.msgid)
        else:
            msgid = self.msgid
        if self.minversion or self.maxversion:
            restr = []
            if self.minversion:
                restr.append("< %s" % ".".join([str(n) for n in self.minversion]))
            if self.maxversion:
                restr.append(">= %s" % ".".join([str(n) for n in self.maxversion]))
            restr = " or ".join(restr)
            if checkerref:
                desc += " It can't be emitted when using Python %s." % restr
            else:
                desc += " This message can't be emitted when using Python %s." % restr
        desc = _normalize_text(" ".join(desc.split()), indent="  ")
        if title != "%s":
            title = title.splitlines()[0]

            return ":%s: *%s*\n%s" % (msgid, title.rstrip(" "), desc)
        return ":%s:\n%s" % (msgid, desc)


class MessagesHandlerMixIn:
    """a mix-in class containing all the messages related methods for the main
    lint class
    """

    __by_id_managed_msgs = []  # type: ignore

    def __init__(self):
        self._msgs_state = {}
        self.msg_status = 0

    def _checker_messages(self, checker):
        for known_checker in self._checkers[checker.lower()]:
            for msgid in known_checker.msgs:
                yield msgid

    @classmethod
    def clear_by_id_managed_msgs(cls):
        cls.__by_id_managed_msgs.clear()

    @classmethod
    def get_by_id_managed_msgs(cls):
        return cls.__by_id_managed_msgs

    def _register_by_id_managed_msg(self, msgid, line, is_disabled=True):
        """If the msgid is a numeric one, then register it to inform the user
        it could furnish instead a symbolic msgid."""
        try:
            message_definitions = self.msgs_store.get_message_definitions(msgid)
            for message_definition in message_definitions:
                if msgid == message_definition.msgid:
                    MessagesHandlerMixIn.__by_id_managed_msgs.append(
                        (
                            self.current_name,
                            message_definition.msgid,
                            message_definition.symbol,
                            line,
                            is_disabled,
                        )
                    )
        except UnknownMessageError:
            pass

    def disable(self, msgid, scope="package", line=None, ignore_unknown=False):
        """don't output message of the given id"""
        self._set_msg_status(
            msgid, enable=False, scope=scope, line=line, ignore_unknown=ignore_unknown
        )
        self._register_by_id_managed_msg(msgid, line)

    def enable(self, msgid, scope="package", line=None, ignore_unknown=False):
        """reenable message of the given id"""
        self._set_msg_status(
            msgid, enable=True, scope=scope, line=line, ignore_unknown=ignore_unknown
        )
        self._register_by_id_managed_msg(msgid, line, is_disabled=False)

    def _set_msg_status(
        self, msgid, enable, scope="package", line=None, ignore_unknown=False
    ):
        assert scope in ("package", "module")

        if msgid == "all":
            for _msgid in MSG_TYPES:
                self._set_msg_status(_msgid, enable, scope, line, ignore_unknown)
            if enable and not self._python3_porting_mode:
                # Don't activate the python 3 porting checker if it wasn't activated explicitly.
                self.disable("python3")
            return

        # msgid is a category?
        catid = category_id(msgid)
        if catid is not None:
            for _msgid in self.msgs_store._msgs_by_category.get(catid):
                self._set_msg_status(_msgid, enable, scope, line)
            return

        # msgid is a checker name?
        if msgid.lower() in self._checkers:
            msgs_store = self.msgs_store
            for checker in self._checkers[msgid.lower()]:
                for _msgid in checker.msgs:
                    if _msgid in msgs_store._alternative_names:
                        self._set_msg_status(_msgid, enable, scope, line)
            return

        # msgid is report id?
        if msgid.lower().startswith("rp"):
            if enable:
                self.enable_report(msgid)
            else:
                self.disable_report(msgid)
            return

        try:
            # msgid is a symbolic or numeric msgid.
            message_definitions = self.msgs_store.get_message_definitions(msgid)
        except UnknownMessageError:
            if ignore_unknown:
                return
            raise
        for message_definition in message_definitions:
            self._set_one_msg_status(scope, message_definition, line, enable)

    def _set_one_msg_status(self, scope, msg, line, enable):
        if scope == "module":
            self.file_state.set_msg_status(msg, line, enable)
            if not enable and msg.symbol != "locally-disabled":
                self.add_message(
                    "locally-disabled", line=line, args=(msg.symbol, msg.msgid)
                )
        else:
            msgs = self._msgs_state
            msgs[msg.msgid] = enable
            # sync configuration object
            self.config.enable = [
                self._message_symbol(mid) for mid, val in sorted(msgs.items()) if val
            ]
            self.config.disable = [
                self._message_symbol(mid)
                for mid, val in sorted(msgs.items())
                if not val
            ]

    def _message_symbol(self, msgid):
        """Get the message symbol of the given message id

        Return the original message id if the message does not
        exist.
        """
        try:
            return [md.symbol for md in self.msgs_store.get_message_definitions(msgid)]
        except UnknownMessageError:
            return msgid

    def get_message_state_scope(self, msgid, line=None, confidence=UNDEFINED):
        """Returns the scope at which a message was enabled/disabled."""
        if self.config.confidence and confidence.name not in self.config.confidence:
            return MSG_STATE_CONFIDENCE
        try:
            if line in self.file_state._module_msgs_state[msgid]:
                return MSG_STATE_SCOPE_MODULE
        except (KeyError, TypeError):
            return MSG_STATE_SCOPE_CONFIG
        return None

    def is_message_enabled(self, msg_descr, line=None, confidence=None):
        """return true if the message associated to the given message id is
        enabled

        msgid may be either a numeric or symbolic message id.
        """
        if self.config.confidence and confidence:
            if confidence.name not in self.config.confidence:
                return False
        try:
            message_definitions = self.msgs_store.get_message_definitions(msg_descr)
            msgids = [md.msgid for md in message_definitions]
        except UnknownMessageError:
            # The linter checks for messages that are not registered
            # due to version mismatch, just treat them as message IDs
            # for now.
            msgids = [msg_descr]
        for msgid in msgids:
            if self.is_one_message_enabled(msgid, line):
                return True
        return False

    def is_one_message_enabled(self, msgid, line):
        if line is None:
            return self._msgs_state.get(msgid, True)
        try:
            return self.file_state._module_msgs_state[msgid][line]
        except KeyError:
            # Check if the message's line is after the maximum line existing in ast tree.
            # This line won't appear in the ast tree and won't be referred in
            #  self.file_state._module_msgs_state
            # This happens for example with a commented line at the end of a module.
            max_line_number = self.file_state.get_effective_max_line_number()
            if max_line_number and line > max_line_number:
                fallback = True
                lines = self.file_state._raw_module_msgs_state.get(msgid, {})

                # Doesn't consider scopes, as a disable can be in a different scope
                # than that of the current line.
                closest_lines = reversed(
                    [
                        (message_line, enable)
                        for message_line, enable in lines.items()
                        if message_line <= line
                    ]
                )
                last_line, is_enabled = next(closest_lines, (None, None))
                if last_line is not None:
                    fallback = is_enabled

                return self._msgs_state.get(msgid, fallback)
            return self._msgs_state.get(msgid, True)

    def add_message(
        self,
        msg_descr,
        line=None,
        node=None,
        args=None,
        confidence=UNDEFINED,
        col_offset=None,
    ):
        """Adds a message given by ID or name.

        If provided, the message string is expanded using args.

        AST checkers must provide the node argument (but may optionally
        provide line if the line number is different), raw and token checkers
        must provide the line argument.
        """
        message_definitions = self.msgs_store.get_message_definitions(msg_descr)
        for message_definition in message_definitions:
            self.add_one_message(
                message_definition, line, node, args, confidence, col_offset
            )

    def add_one_message(
        self, message_definition, line, node, args, confidence, col_offset
    ):
        msgid = message_definition.msgid
        # backward compatibility, message may not have a symbol
        symbol = message_definition.symbol or msgid
        # Fatal messages and reports are special, the node/scope distinction
        # does not apply to them.
        if msgid[0] not in _SCOPE_EXEMPT:
            if message_definition.scope == WarningScope.LINE:
                if line is None:
                    raise InvalidMessageError(
                        "Message %s must provide line, got None" % msgid
                    )
                if node is not None:
                    raise InvalidMessageError(
                        "Message %s must only provide line, "
                        "got line=%s, node=%s" % (msgid, line, node)
                    )
            elif message_definition.scope == WarningScope.NODE:
                # Node-based warnings may provide an override line.
                if node is None:
                    raise InvalidMessageError(
                        "Message %s must provide Node, got None" % msgid
                    )

        if line is None and node is not None:
            line = node.fromlineno
        if col_offset is None and hasattr(node, "col_offset"):
            col_offset = (
                node.col_offset
            )  # XXX measured in bytes for utf-8, divide by two for chars?

        # should this message be displayed
        if not self.is_message_enabled(msgid, line, confidence):
            self.file_state.handle_ignored_message(
                self.get_message_state_scope(msgid, line, confidence),
                msgid,
                line,
                node,
                args,
                confidence,
            )
            return
        # update stats
        msg_cat = MSG_TYPES[msgid[0]]
        self.msg_status |= MSG_TYPES_STATUS[msgid[0]]
        self.stats[msg_cat] += 1
        self.stats["by_module"][self.current_name][msg_cat] += 1
        try:
            self.stats["by_msg"][symbol] += 1
        except KeyError:
            self.stats["by_msg"][symbol] = 1
        # expand message ?
        msg = message_definition.msg
        if args:
            msg %= args
        # get module and object
        if node is None:
            module, obj = self.current_name, ""
            abspath = self.current_file
        else:
            module, obj = get_module_and_frameid(node)
            abspath = node.root().file
        path = abspath.replace(self.reporter.path_strip_prefix, "", 1)
        # add the message
        self.reporter.handle_message(
            Message(
                msgid,
                symbol,
                (abspath, path, module, obj, line or 1, col_offset or 0),
                msg,
                confidence,
            )
        )

    def print_full_documentation(self, stream=None):
        """output a full documentation in ReST format"""
        if not stream:
            stream = sys.stdout

        print("Pylint global options and switches", file=stream)
        print("----------------------------------", file=stream)
        print("", file=stream)
        print("Pylint provides global options and switches.", file=stream)
        print("", file=stream)

        by_checker = {}
        for checker in self.get_checkers():
            if checker.name == "master":
                if checker.options:
                    for section, options in checker.options_by_section():
                        if section is None:
                            title = "General options"
                        else:
                            title = "%s options" % section.capitalize()
                        print(title, file=stream)
                        print("~" * len(title), file=stream)
                        _rest_format_section(stream, None, options)
                        print("", file=stream)
            else:
                name = checker.name
                try:
                    by_checker[name]["options"] += checker.options_and_values()
                    by_checker[name]["msgs"].update(checker.msgs)
                    by_checker[name]["reports"] += checker.reports
                except KeyError:
                    by_checker[name] = {
                        "options": list(checker.options_and_values()),
                        "msgs": dict(checker.msgs),
                        "reports": list(checker.reports),
                    }

        print("Pylint checkers' options and switches", file=stream)
        print("-------------------------------------", file=stream)
        print("", file=stream)
        print("Pylint checkers can provide three set of features:", file=stream)
        print("", file=stream)
        print("* options that control their execution,", file=stream)
        print("* messages that they can raise,", file=stream)
        print("* reports that they can generate.", file=stream)
        print("", file=stream)
        print("Below is a list of all checkers and their features.", file=stream)
        print("", file=stream)

        for checker, info in sorted(by_checker.items()):
            self._print_checker_doc(checker, info, stream=stream)

    @staticmethod
    def _print_checker_doc(checker_name, info, stream=None):
        """Helper method for print_full_documentation.

        Also used by doc/exts/pylint_extensions.py.
        """
        if not stream:
            stream = sys.stdout

        doc = info.get("doc")
        module = info.get("module")
        msgs = info.get("msgs")
        options = info.get("options")
        reports = info.get("reports")

        checker_title = "%s checker" % (checker_name.replace("_", " ").title())

        if module:
            # Provide anchor to link against
            print(".. _%s:\n" % module, file=stream)
        print(checker_title, file=stream)
        print("~" * len(checker_title), file=stream)
        print("", file=stream)
        if module:
            print("This checker is provided by ``%s``." % module, file=stream)
        print("Verbatim name of the checker is ``%s``." % checker_name, file=stream)
        print("", file=stream)
        if doc:
            # Provide anchor to link against
            title = "{} Documentation".format(checker_title)
            print(title, file=stream)
            print("^" * len(title), file=stream)
            print(cleandoc(doc), file=stream)
            print("", file=stream)
        if options:
            title = "{} Options".format(checker_title)
            print(title, file=stream)
            print("^" * len(title), file=stream)
            _rest_format_section(stream, None, options)
            print("", file=stream)
        if msgs:
            title = "{} Messages".format(checker_title)
            print(title, file=stream)
            print("^" * len(title), file=stream)
            for msgid, msg in sorted(
                msgs.items(), key=lambda kv: (_MSG_ORDER.index(kv[0][0]), kv[1])
            ):
                msg = build_message_def(checker_name, msgid, msg)
                print(msg.format_help(checkerref=False), file=stream)
            print("", file=stream)
        if reports:
            title = "{} Reports".format(checker_title)
            print(title, file=stream)
            print("^" * len(title), file=stream)
            for report in reports:
                print(":%s: %s" % report[:2], file=stream)
            print("", file=stream)
        print("", file=stream)


class FileState:
    """Hold internal state specific to the currently analyzed file"""

    def __init__(self, modname=None):
        self.base_name = modname
        self._module_msgs_state = {}
        self._raw_module_msgs_state = {}
        self._ignored_msgs = collections.defaultdict(set)
        self._suppression_mapping = {}
        self._effective_max_line_number = None

    def collect_block_lines(self, msgs_store, module_node):
        """Walk the AST to collect block level options line numbers."""
        for msg, lines in self._module_msgs_state.items():
            self._raw_module_msgs_state[msg] = lines.copy()
        orig_state = self._module_msgs_state.copy()
        self._module_msgs_state = {}
        self._suppression_mapping = {}
        self._effective_max_line_number = module_node.tolineno
        self._collect_block_lines(msgs_store, module_node, orig_state)

    def _collect_block_lines(self, msgs_store, node, msg_state):
        """Recursively walk (depth first) AST to collect block level options
        line numbers.
        """
        for child in node.get_children():
            self._collect_block_lines(msgs_store, child, msg_state)
        first = node.fromlineno
        last = node.tolineno
        # first child line number used to distinguish between disable
        # which are the first child of scoped node with those defined later.
        # For instance in the code below:
        #
        # 1.   def meth8(self):
        # 2.        """test late disabling"""
        # 3.        # pylint: disable=E1102
        # 4.        print self.blip
        # 5.        # pylint: disable=E1101
        # 6.        print self.bla
        #
        # E1102 should be disabled from line 1 to 6 while E1101 from line 5 to 6
        #
        # this is necessary to disable locally messages applying to class /
        # function using their fromlineno
        if (
            isinstance(node, (nodes.Module, nodes.ClassDef, nodes.FunctionDef))
            and node.body
        ):
            firstchildlineno = node.body[0].fromlineno
        else:
            firstchildlineno = last
        for msgid, lines in msg_state.items():
            for lineno, state in list(lines.items()):
                original_lineno = lineno
                if first > lineno or last < lineno:
                    continue
                # Set state for all lines for this block, if the
                # warning is applied to nodes.
                message_definitions = msgs_store.get_message_definitions(msgid)
                for message_definition in message_definitions:
                    if message_definition.scope == WarningScope.NODE:
                        if lineno > firstchildlineno:
                            state = True
                        first_, last_ = node.block_range(lineno)
                    else:
                        first_ = lineno
                        last_ = last
                for line in range(first_, last_ + 1):
                    # do not override existing entries
                    if line in self._module_msgs_state.get(msgid, ()):
                        continue
                    if line in lines:  # state change in the same block
                        state = lines[line]
                        original_lineno = line
                    if not state:
                        self._suppression_mapping[(msgid, line)] = original_lineno
                    try:
                        self._module_msgs_state[msgid][line] = state
                    except KeyError:
                        self._module_msgs_state[msgid] = {line: state}
                del lines[lineno]

    def set_msg_status(self, msg, line, status):
        """Set status (enabled/disable) for a given message at a given line"""
        assert line > 0
        try:
            self._module_msgs_state[msg.msgid][line] = status
        except KeyError:
            self._module_msgs_state[msg.msgid] = {line: status}

    def handle_ignored_message(
        self, state_scope, msgid, line, node, args, confidence
    ):  # pylint: disable=unused-argument
        """Report an ignored message.

        state_scope is either MSG_STATE_SCOPE_MODULE or MSG_STATE_SCOPE_CONFIG,
        depending on whether the message was disabled locally in the module,
        or globally. The other arguments are the same as for add_message.
        """
        if state_scope == MSG_STATE_SCOPE_MODULE:
            try:
                orig_line = self._suppression_mapping[(msgid, line)]
                self._ignored_msgs[(msgid, orig_line)].add(line)
            except KeyError:
                pass

    def iter_spurious_suppression_messages(self, msgs_store):
        for warning, lines in self._raw_module_msgs_state.items():
            for line, enable in lines.items():
                if not enable and (warning, line) not in self._ignored_msgs:
                    yield "useless-suppression", line, (
                        msgs_store.get_msg_display_string(warning),
                    )
        # don't use iteritems here, _ignored_msgs may be modified by add_message
        for (warning, from_), lines in list(self._ignored_msgs.items()):
            for line in lines:
                yield "suppressed-message", line, (
                    msgs_store.get_msg_display_string(warning),
                    from_,
                )

    def get_effective_max_line_number(self):
        return self._effective_max_line_number


class MessagesStore:
    """The messages store knows information about every possible message but has
    no particular state during analysis.
    """

    def __init__(self):
        # Primary registry for all active messages (i.e. all messages
        # that can be emitted by pylint for the underlying Python
        # version). It contains the 1:1 mapping from symbolic names
        # to message definition objects.
        # Keys are msg ids, values are a 2-uple with the msg type and the
        # msg itself
        self._messages_definitions = {}
        # Maps alternative names (numeric IDs, deprecated names) to
        # message definitions. May contain several names for each definition
        # object.
        self._alternative_names = {}
        self._msgs_by_category = collections.defaultdict(list)

    @property
    def messages(self):
        """The list of all active messages."""
        return self._messages_definitions.values()

    def add_renamed_message(self, old_id, old_symbol, new_symbol):
        """Register the old ID and symbol for a warning that was renamed.

        This allows users to keep using the old ID/symbol in suppressions.
        """
        message_definition = self.get_message_definitions(new_symbol)[0]
        message_definition.old_names.append((old_id, old_symbol))
        self._register_alternative_name(message_definition, old_id, old_symbol)

    @staticmethod
    def get_checker_message_definitions(checker):
        """Return the list of messages definitions for a checker.

        :param BaseChecker checker:
        :rtype: list
        :return: A list of MessageDefinition.
        """
        message_definitions = []
        for msgid, msg_tuple in sorted(checker.msgs.items()):
            message = build_message_def(checker, msgid, msg_tuple)
            message_definitions.append(message)
        return message_definitions

    def register_messages_from_checker(self, checker):
        """Register all messages from a checker.

        :param BaseChecker checker:
        """
        checker_message_definitions = self.get_checker_message_definitions(checker)
        self._check_checker_consistency(checker_message_definitions)
        for message_definition in checker_message_definitions:
            self.register_message(message_definition)

    def register_message(self, message):
        """Register a MessageDefinition with consistency in mind.

        :param MessageDefinition message: The message definition being added.
        """
        self._check_id_and_symbol_consistency(message.msgid, message.symbol)
        self._check_symbol(message.msgid, message.symbol)
        self._check_msgid(message.msgid, message.symbol)
        for old_name in message.old_names:
            self._check_symbol(message.msgid, old_name[1])
        self._messages_definitions[message.symbol] = message
        self._register_alternative_name(message, message.msgid, message.symbol)
        for old_id, old_symbol in message.old_names:
            self._register_alternative_name(message, old_id, old_symbol)
        self._msgs_by_category[message.msgid[0]].append(message.msgid)

    @staticmethod
    def _check_checker_consistency(messages):
        """Check the msgid consistency in a list of messages definitions.

        msg ids for a checker should be a string of len 4, where the two first
        characters are the checker id and the two last the msg id in this
        checker.

        :param list messages: List of MessageDefinition.
        :raises InvalidMessageError: If the checker id in the messages are not
        always the same
        """
        checker_id = None
        existing_ids = []
        for message in messages:
            if checker_id is not None and checker_id != message.msgid[1:3]:
                error_msg = "Inconsistent checker part in message id "
                error_msg += "'{}' (expected 'x{checker_id}xx' ".format(
                    message.msgid, checker_id=checker_id
                )
                error_msg += "because we already had {existing_ids}).".format(
                    existing_ids=existing_ids
                )
                raise InvalidMessageError(error_msg)
            checker_id = message.msgid[1:3]
            existing_ids.append(message.msgid)

    def _register_alternative_name(self, msg, msgid, symbol):
        """helper for register_message()"""
        self._check_id_and_symbol_consistency(msgid, symbol)
        self._alternative_names[msgid] = msg
        self._alternative_names[symbol] = msg

    def _check_symbol(self, msgid, symbol):
        """Check that a symbol is not already used. """
        other_message = self._messages_definitions.get(symbol)
        if other_message:
            self._raise_duplicate_msg_id(symbol, msgid, other_message.msgid)
        else:
            alternative_msgid = None
        alternative_message = self._alternative_names.get(symbol)
        if alternative_message:
            if alternative_message.symbol == symbol:
                alternative_msgid = alternative_message.msgid
            else:
                for old_msgid, old_symbol in alternative_message.old_names:
                    if old_symbol == symbol:
                        alternative_msgid = old_msgid
                        break
            if msgid != alternative_msgid:
                self._raise_duplicate_msg_id(symbol, msgid, alternative_msgid)

    def _check_msgid(self, msgid, symbol):
        for message in self._messages_definitions.values():
            if message.msgid == msgid:
                self._raise_duplicate_symbol(msgid, symbol, message.symbol)

    def _check_id_and_symbol_consistency(self, msgid, symbol):
        try:
            alternative = self._alternative_names[msgid]
        except KeyError:
            alternative = False
        try:
            if not alternative:
                alternative = self._alternative_names[symbol]
        except KeyError:
            # There is no alternative names concerning this msgid/symbol.
            # So nothing to check
            return None
        old_symbolic_name = None
        old_symbolic_id = None
        for alternate_msgid, alternate_symbol in alternative.old_names:
            if alternate_msgid == msgid or alternate_symbol == symbol:
                old_symbolic_id = alternate_msgid
                old_symbolic_name = alternate_symbol
        if symbol not in (alternative.symbol, old_symbolic_name):
            if msgid == old_symbolic_id:
                self._raise_duplicate_symbol(msgid, symbol, old_symbolic_name)
            else:
                self._raise_duplicate_symbol(msgid, symbol, alternative.symbol)
        return None

    @staticmethod
    def _raise_duplicate_symbol(msgid, symbol, other_symbol):
        """Raise an error when a symbol is duplicated.

        :param str msgid: The msgid corresponding to the symbols
        :param str symbol: Offending symbol
        :param str other_symbol: Other offending symbol
        :raises InvalidMessageError: when a symbol is duplicated.
        """
        symbols = [symbol, other_symbol]
        symbols.sort()
        error_message = "Message id '{msgid}' cannot have both ".format(msgid=msgid)
        error_message += "'{other_symbol}' and '{symbol}' as symbolic name.".format(
            other_symbol=symbols[0], symbol=symbols[1]
        )
        raise InvalidMessageError(error_message)

    @staticmethod
    def _raise_duplicate_msg_id(symbol, msgid, other_msgid):
        """Raise an error when a msgid is duplicated.

        :param str symbol: The symbol corresponding to the msgids
        :param str msgid: Offending msgid
        :param str other_msgid: Other offending msgid
        :raises InvalidMessageError: when a msgid is duplicated.
        """
        msgids = [msgid, other_msgid]
        msgids.sort()
        error_message = "Message symbol '{symbol}' cannot be used for ".format(
            symbol=symbol
        )
        error_message += "'{other_msgid}' and '{msgid}' at the same time.".format(
            other_msgid=msgids[0], msgid=msgids[1]
        )
        raise InvalidMessageError(error_message)

    def get_message_definitions(self, msgid_or_symbol: str) -> list:
        """Returns the Message object for this message.

        :param str msgid_or_symbol: msgid_or_symbol may be either a numeric or symbolic id.
        :raises UnknownMessageError: if the message id is not defined.
        :rtype: List of MessageDefinition
        :return: A message definition corresponding to msgid_or_symbol
        """
        if msgid_or_symbol[1:].isdigit():
            msgid_or_symbol = msgid_or_symbol.upper()
        for source in (self._alternative_names, self._messages_definitions):
            try:
                return [source[msgid_or_symbol]]
            except KeyError:
                pass
        error_msg = "No such message id or symbol '{msgid_or_symbol}'.".format(
            msgid_or_symbol=msgid_or_symbol
        )
        raise UnknownMessageError(error_msg)

    def get_msg_display_string(self, msgid):
        """Generates a user-consumable representation of a message.

        Can be just the message ID or the ID and the symbol.
        """
        message_definitions = self.get_message_definitions(msgid)
        if len(message_definitions) == 1:
            return repr(message_definitions[0].symbol)
        return repr([md.symbol for md in message_definitions])

    def help_message(self, msgids):
        """Display help messages for the given message identifiers"""
        for msgid in msgids:
            try:
                for message_definition in self.get_message_definitions(msgid):
                    print(message_definition.format_help(checkerref=True))
                    print("")
            except UnknownMessageError as ex:
                print(ex)
                print("")
                continue

    def list_messages(self):
        """Output full messages list documentation in ReST format. """
        messages = sorted(self._messages_definitions.values(), key=lambda m: m.msgid)
        for message in messages:
            if not message.may_be_emitted():
                continue
            print(message.format_help(checkerref=False))
        print("")


class ReportsHandlerMixIn:
    """a mix-in class containing all the reports and stats manipulation
    related methods for the main lint class
    """

    def __init__(self):
        self._reports = collections.defaultdict(list)
        self._reports_state = {}

    def report_order(self):
        """ Return a list of reports, sorted in the order
        in which they must be called.
        """
        return list(self._reports)

    def register_report(self, reportid, r_title, r_cb, checker):
        """register a report

        reportid is the unique identifier for the report
        r_title the report's title
        r_cb the method to call to make the report
        checker is the checker defining the report
        """
        reportid = reportid.upper()
        self._reports[checker].append((reportid, r_title, r_cb))

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
        sect = Section("Report", "%s statements analysed." % (self.stats["statement"]))
        for checker in self.report_order():
            for reportid, r_title, r_cb in self._reports[checker]:
                if not self.report_is_enabled(reportid):
                    continue
                report_sect = Section(r_title)
                try:
                    r_cb(report_sect, stats, old_stats)
                except EmptyReportError:
                    continue
                report_sect.report_id = reportid
                sect.append(report_sect)
        return sect

    def add_stats(self, **kwargs):
        """add some stats entries to the statistic dictionary
        raise an AssertionError if there is a key conflict
        """
        for key, value in kwargs.items():
            if key[-1] == "_":
                key = key[:-1]
            assert key not in self.stats
            self.stats[key] = value
        return self.stats


def _basename_in_blacklist_re(base_name, black_list_re):
    """Determines if the basename is matched in a regex blacklist

    :param str base_name: The basename of the file
    :param list black_list_re: A collection of regex patterns to match against.
        Successful matches are blacklisted.

    :returns: `True` if the basename is blacklisted, `False` otherwise.
    :rtype: bool
    """
    for file_pattern in black_list_re:
        if file_pattern.match(base_name):
            return True
    return False


def _modpath_from_file(filename, is_namespace):
    def _is_package_cb(path, parts):
        return modutils.check_modpath_has_init(path, parts) or is_namespace

    return modutils.modpath_from_file_with_callback(
        filename, is_package_cb=_is_package_cb
    )


def expand_modules(files_or_modules, black_list, black_list_re):
    """take a list of files/modules/packages and return the list of tuple
    (file, module name) which have to be actually checked
    """
    result = []
    errors = []
    for something in files_or_modules:
        if os.path.basename(something) in black_list:
            continue
        if _basename_in_blacklist_re(os.path.basename(something), black_list_re):
            continue
        if exists(something):
            # this is a file or a directory
            try:
                modname = ".".join(modutils.modpath_from_file(something))
            except ImportError:
                modname = splitext(basename(something))[0]
            if isdir(something):
                filepath = join(something, "__init__.py")
            else:
                filepath = something
        else:
            # suppose it's a module or package
            modname = something
            try:
                filepath = modutils.file_from_modpath(modname.split("."))
                if filepath is None:
                    continue
            except (ImportError, SyntaxError) as ex:
                # FIXME p3k : the SyntaxError is a Python bug and should be
                # removed as soon as possible http://bugs.python.org/issue10588
                errors.append({"key": "fatal", "mod": modname, "ex": ex})
                continue

        filepath = normpath(filepath)
        modparts = (modname or something).split(".")

        try:
            spec = modutils.file_info_from_modpath(modparts, path=sys.path)
        except ImportError:
            # Might not be acceptable, don't crash.
            is_namespace = False
            is_directory = isdir(something)
        else:
            is_namespace = modutils.is_namespace(spec)
            is_directory = modutils.is_directory(spec)

        if not is_namespace:
            result.append(
                {
                    "path": filepath,
                    "name": modname,
                    "isarg": True,
                    "basepath": filepath,
                    "basename": modname,
                }
            )

        has_init = (
            not (modname.endswith(".__init__") or modname == "__init__")
            and basename(filepath) == "__init__.py"
        )

        if has_init or is_namespace or is_directory:
            for subfilepath in modutils.get_module_files(
                dirname(filepath), black_list, list_all=is_namespace
            ):
                if filepath == subfilepath:
                    continue
                if _basename_in_blacklist_re(basename(subfilepath), black_list_re):
                    continue

                modpath = _modpath_from_file(subfilepath, is_namespace)
                submodname = ".".join(modpath)
                result.append(
                    {
                        "path": subfilepath,
                        "name": submodname,
                        "isarg": False,
                        "basepath": filepath,
                        "basename": modname,
                    }
                )
    return result, errors


class PyLintASTWalker:
    def __init__(self, linter):
        # callbacks per node types
        self.nbstatements = 0
        self.visit_events = collections.defaultdict(list)
        self.leave_events = collections.defaultdict(list)
        self.linter = linter

    def _is_method_enabled(self, method):
        if not hasattr(method, "checks_msgs"):
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
            if cid == "default":
                continue
            if member.startswith("visit_"):
                v_meth = getattr(checker, member)
                # don't use visit_methods with no activated message:
                if self._is_method_enabled(v_meth):
                    visits[cid].append(v_meth)
                    vcids.add(cid)
            elif member.startswith("leave_"):
                l_meth = getattr(checker, member)
                # don't use leave_methods with no activated message:
                if self._is_method_enabled(l_meth):
                    leaves[cid].append(l_meth)
                    lcids.add(cid)
        visit_default = getattr(checker, "visit_default", None)
        if visit_default:
            for cls in nodes.ALL_NODE_CLASSES:
                cid = cls.__name__.lower()
                if cid not in vcids:
                    visits[cid].append(visit_default)
        # for now we have no "leave_default" method in Pylint

    def walk(self, astroid):
        """call visit events of astroid checkers for the given node, recurse on
        its children, then leave events.
        """
        cid = astroid.__class__.__name__.lower()

        # Detect if the node is a new name for a deprecated alias.
        # In this case, favour the methods for the deprecated
        # alias if any,  in order to maintain backwards
        # compatibility.
        visit_events = self.visit_events.get(cid, ())
        leave_events = self.leave_events.get(cid, ())

        if astroid.is_statement:
            self.nbstatements += 1
        # generate events for this node on each checker
        for cb in visit_events or ():
            cb(astroid)
        # recurse on children
        for child in astroid.get_children():
            self.walk(child)
        for cb in leave_events or ():
            cb(astroid)


PY_EXTS = (".py", ".pyc", ".pyo", ".pyw", ".so", ".dll")


def register_plugins(linter, directory):
    """load all module and package in the given directory, looking for a
    'register' function in each one, used to register pylint checkers
    """
    imported = {}
    for filename in os.listdir(directory):
        base, extension = splitext(filename)
        if base in imported or base == "__pycache__":
            continue
        if (
            extension in PY_EXTS
            and base != "__init__"
            or (not extension and isdir(join(directory, base)))
        ):
            try:
                module = modutils.load_module_from_file(join(directory, filename))
            except ValueError:
                # empty module name (usually emacs auto-save files)
                continue
            except ImportError as exc:
                print(
                    "Problem importing module %s: %s" % (filename, exc), file=sys.stderr
                )
            else:
                if hasattr(module, "register"):
                    module.register(linter)
                    imported[base] = 1


def get_global_option(checker, option, default=None):
    """ Retrieve an option defined by the given *checker* or
    by all known option providers.

    It will look in the list of all options providers
    until the given *option* will be found.
    If the option wasn't found, the *default* value will be returned.
    """
    # First, try in the given checker's config.
    # After that, look in the options providers.

    try:
        return getattr(checker.config, option.replace("-", "_"))
    except AttributeError:
        pass
    for provider in checker.linter.options_providers:
        for options in provider.options:
            if options[0] == option:
                return getattr(provider.config, option.replace("-", "_"))
    return default


def deprecated_option(
    shortname=None, opt_type=None, help_msg=None, deprecation_msg=None
):
    def _warn_deprecated(option, optname, *args):  # pylint: disable=unused-argument
        if deprecation_msg:
            sys.stderr.write(deprecation_msg % (optname,))

    option = {
        "help": help_msg,
        "hide": True,
        "type": opt_type,
        "action": "callback",
        "callback": _warn_deprecated,
        "deprecated": True,
    }
    if shortname:
        option["shortname"] = shortname
    return option


def _splitstrip(string, sep=","):
    """return a list of stripped string by splitting the string given as
    argument on `sep` (',' by default). Empty string are discarded.

    >>> _splitstrip('a, b, c   ,  4,,')
    ['a', 'b', 'c', '4']
    >>> _splitstrip('a')
    ['a']
    >>> _splitstrip('a,\nb,\nc,')
    ['a', 'b', 'c']

    :type string: str or unicode
    :param string: a csv line

    :type sep: str or unicode
    :param sep: field separator, default to the comma (',')

    :rtype: str or unicode
    :return: the unquoted string (or the input string if it wasn't quoted)
    """
    return [word.strip() for word in string.split(sep) if word.strip()]


def _unquote(string):
    """remove optional quotes (simple or double) from the string

    :type string: str or unicode
    :param string: an optionally quoted string

    :rtype: str or unicode
    :return: the unquoted string (or the input string if it wasn't quoted)
    """
    if not string:
        return string
    if string[0] in "\"'":
        string = string[1:]
    if string[-1] in "\"'":
        string = string[:-1]
    return string


def _normalize_text(text, line_len=80, indent=""):
    """Wrap the text on the given line length."""
    return "\n".join(
        textwrap.wrap(
            text, width=line_len, initial_indent=indent, subsequent_indent=indent
        )
    )


def _check_csv(value):
    if isinstance(value, (list, tuple)):
        return value
    return _splitstrip(value)


def _comment(string):
    """return string as a comment"""
    lines = [line.strip() for line in string.splitlines()]
    return "# " + ("%s# " % os.linesep).join(lines)


def _format_option_value(optdict, value):
    """return the user input's value from a 'compiled' value"""
    if isinstance(value, (list, tuple)):
        value = ",".join(_format_option_value(optdict, item) for item in value)
    elif isinstance(value, dict):
        value = ",".join("%s:%s" % (k, v) for k, v in value.items())
    elif hasattr(value, "match"):  # optdict.get('type') == 'regexp'
        # compiled regexp
        value = value.pattern
    elif optdict.get("type") == "yn":
        value = "yes" if value else "no"
    elif isinstance(value, str) and value.isspace():
        value = "'%s'" % value
    return value


def _ini_format_section(stream, section, options, doc=None):
    """format an options section using the INI format"""
    if doc:
        print(_comment(doc), file=stream)
    print("[%s]" % section, file=stream)
    _ini_format(stream, options)


def _ini_format(stream, options):
    """format options using the INI format"""
    for optname, optdict, value in options:
        value = _format_option_value(optdict, value)
        help_opt = optdict.get("help")
        if help_opt:
            help_opt = _normalize_text(help_opt, line_len=79, indent="# ")
            print(file=stream)
            print(help_opt, file=stream)
        else:
            print(file=stream)
        if value is None:
            print("#%s=" % optname, file=stream)
        else:
            value = str(value).strip()
            if re.match(r"^([\w-]+,)+[\w-]+$", str(value)):
                separator = "\n " + " " * len(optname)
                value = separator.join(x + "," for x in str(value).split(","))
                # remove trailing ',' from last element of the list
                value = value[:-1]
            print("%s=%s" % (optname, value), file=stream)


format_section = _ini_format_section


def _rest_format_section(stream, section, options, doc=None):
    """format an options section using as ReST formatted output"""
    if section:
        print("%s\n%s" % (section, "'" * len(section)), file=stream)
    if doc:
        print(_normalize_text(doc, line_len=79, indent=""), file=stream)
        print(file=stream)
    for optname, optdict, value in options:
        help_opt = optdict.get("help")
        print(":%s:" % optname, file=stream)
        if help_opt:
            help_opt = _normalize_text(help_opt, line_len=79, indent="  ")
            print(help_opt, file=stream)
        if value:
            value = str(_format_option_value(optdict, value))
            print(file=stream)
            print("  Default: ``%s``" % value.replace("`` ", "```` ``"), file=stream)
