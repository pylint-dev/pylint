# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

from __future__ import print_function

import sys
from inspect import cleandoc

from pylint.exceptions import InvalidMessageError, UnknownMessageError
from pylint.interfaces import UNDEFINED
from pylint.message.constants import (
    _MSG_ORDER,
    _SCOPE_EXEMPT,
    MSG_STATE_CONFIDENCE,
    MSG_STATE_SCOPE_CONFIG,
    MSG_STATE_SCOPE_MODULE,
    MSG_TYPES,
    MSG_TYPES_STATUS,
)
from pylint.message.message import Message
from pylint.utils.warning_scope import WarningScope
from pylint.message.build_message_definition import build_message_def
from pylint.utils.utils import (
    _format_option_value,
    category_id,
    get_module_and_frameid,
    normalize_text,
)


def _rest_format_section(stream, section, options, doc=None):
    """format an options section using as ReST formatted output"""
    if section:
        print("%s\n%s" % (section, "'" * len(section)), file=stream)
    if doc:
        print(normalize_text(doc, line_len=79, indent=""), file=stream)
        print(file=stream)
    for optname, optdict, value in options:
        help_opt = optdict.get("help")
        print(":%s:" % optname, file=stream)
        if help_opt:
            help_opt = normalize_text(help_opt, line_len=79, indent="  ")
            print(help_opt, file=stream)
        if value:
            value = str(_format_option_value(optdict, value))
            print(file=stream)
            print("  Default: ``%s``" % value.replace("`` ", "```` ``"), file=stream)


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
