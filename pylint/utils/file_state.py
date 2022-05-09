# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import collections
import sys
import warnings
from collections import defaultdict
from collections.abc import Iterator
from typing import TYPE_CHECKING, Dict

from astroid import nodes

from pylint.constants import (
    INCOMPATIBLE_WITH_USELESS_SUPPRESSION,
    MSG_STATE_SCOPE_MODULE,
    WarningScope,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

if TYPE_CHECKING:
    from pylint.message import MessageDefinition, MessageDefinitionStore


MessageStateDict = Dict[str, Dict[int, bool]]


class FileState:
    """Hold internal state specific to the currently analyzed file."""

    def __init__(
        self,
        modname: str | None = None,
        msg_store: MessageDefinitionStore | None = None,
        node: nodes.Module | None = None,
        *,
        is_base_filestate: bool = False,
    ) -> None:
        if modname is None:
            warnings.warn(
                "FileState needs a string as modname argument. "
                "This argument will be required in pylint 3.0",
                DeprecationWarning,
            )
        if msg_store is None:
            warnings.warn(
                "FileState needs a 'MessageDefinitionStore' as msg_store argument. "
                "This argument will be required in pylint 3.0",
                DeprecationWarning,
            )
        self.base_name = modname
        self._module_msgs_state: MessageStateDict = {}
        self._raw_module_msgs_state: MessageStateDict = {}
        self._ignored_msgs: defaultdict[
            tuple[str, int], set[int]
        ] = collections.defaultdict(set)
        self._suppression_mapping: dict[tuple[str, int], int] = {}
        self._module = node
        if node:
            self._effective_max_line_number = node.tolineno
        else:
            self._effective_max_line_number = None
        self._msgs_store = msg_store
        self._is_base_filestate = is_base_filestate
        """If this FileState is the base state made during initialization of PyLinter."""

    def collect_block_lines(
        self, msgs_store: MessageDefinitionStore, module_node: nodes.Module
    ) -> None:
        """Walk the AST to collect block level options line numbers."""
        for msg, lines in self._module_msgs_state.items():
            self._raw_module_msgs_state[msg] = lines.copy()
        orig_state = self._module_msgs_state.copy()
        self._module_msgs_state = {}
        self._suppression_mapping = {}
        self._effective_max_line_number = module_node.tolineno
        self._collect_block_lines(msgs_store, module_node, orig_state)

    def _collect_block_lines(
        self,
        msgs_store: MessageDefinitionStore,
        node: nodes.NodeNG,
        msg_state: MessageStateDict,
    ) -> None:
        """Recursively walk (depth first) AST to collect block level options
        line numbers.
        """
        for child in node.get_children():
            self._collect_block_lines(msgs_store, child, msg_state)
        # first child line number used to distinguish between disable
        # which are the first child of scoped node with those defined later.
        # For instance in the code below:
        #
        # 1.   def meth8(self):
        # 2.        """test late disabling"""
        # 3.        pylint: disable=not-callable, useless-suppression
        # 4.        print(self.blip)
        # 5.        pylint: disable=no-member, useless-suppression
        # 6.        print(self.bla)
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
            firstchildlineno = node.tolineno
        for msgid, lines in msg_state.items():
            for msg in msgs_store.get_message_definitions(msgid):
                self._set_message_state_in_block(msg, lines, node, firstchildlineno)

    def _set_message_state_in_block(
        self,
        msg: MessageDefinition,
        lines: dict[int, bool],
        node: nodes.NodeNG,
        firstchildlineno: int,
    ) -> None:
        """Set the state of a message in a block of lines."""
        first = node.fromlineno
        last = node.tolineno
        for lineno, state in list(lines.items()):
            original_lineno = lineno
            if first > lineno or last < lineno:
                continue
            # Set state for all lines for this block, if the
            # warning is applied to nodes.
            if msg.scope == WarningScope.NODE:
                if lineno > firstchildlineno:
                    state = True
                first_, last_ = node.block_range(lineno)
            else:
                first_ = lineno
                last_ = last
            for line in range(first_, last_ + 1):
                # do not override existing entries
                if line in self._module_msgs_state.get(msg.msgid, ()):
                    continue
                if line in lines:  # state change in the same block
                    state = lines[line]
                    original_lineno = line
                if not state:
                    self._suppression_mapping[(msg.msgid, line)] = original_lineno
                try:
                    self._module_msgs_state[msg.msgid][line] = state
                except KeyError:
                    self._module_msgs_state[msg.msgid] = {line: state}
            del lines[lineno]

    def set_msg_status(self, msg: MessageDefinition, line: int, status: bool) -> None:
        """Set status (enabled/disable) for a given message at a given line."""
        assert line > 0
        try:
            self._module_msgs_state[msg.msgid][line] = status
        except KeyError:
            self._module_msgs_state[msg.msgid] = {line: status}

    def handle_ignored_message(
        self, state_scope: Literal[0, 1, 2] | None, msgid: str, line: int | None
    ) -> None:
        """Report an ignored message.

        state_scope is either MSG_STATE_SCOPE_MODULE or MSG_STATE_SCOPE_CONFIG,
        depending on whether the message was disabled locally in the module,
        or globally.
        """
        if state_scope == MSG_STATE_SCOPE_MODULE:
            assert isinstance(line, int)  # should always be int inside module scope

            try:
                orig_line = self._suppression_mapping[(msgid, line)]
                self._ignored_msgs[(msgid, orig_line)].add(line)
            except KeyError:
                pass

    def iter_spurious_suppression_messages(
        self,
        msgs_store: MessageDefinitionStore,
    ) -> Iterator[
        tuple[
            Literal["useless-suppression", "suppressed-message"],
            int,
            tuple[str] | tuple[str, int],
        ]
    ]:
        for warning, lines in self._raw_module_msgs_state.items():
            for line, enable in lines.items():
                if (
                    not enable
                    and (warning, line) not in self._ignored_msgs
                    and warning not in INCOMPATIBLE_WITH_USELESS_SUPPRESSION
                ):
                    yield "useless-suppression", line, (
                        msgs_store.get_msg_display_string(warning),
                    )
        # don't use iteritems here, _ignored_msgs may be modified by add_message
        for (warning, from_), ignored_lines in list(self._ignored_msgs.items()):
            for line in ignored_lines:
                yield "suppressed-message", line, (
                    msgs_store.get_msg_display_string(warning),
                    from_,
                )

    def get_effective_max_line_number(self) -> int | None:
        return self._effective_max_line_number
