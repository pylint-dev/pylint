# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Looks for  comparisons to empty string."""

from __future__ import annotations

import itertools
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from astroid import nodes

from pylint import checkers
from pylint.checkers import utils

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class CompareToEmptyStringChecker(checkers.BaseChecker):
    """Checks for comparisons to empty string.

    Most of the time you should use the fact that empty strings are false.
    An exception to this rule is when an empty string value is allowed in the program
    and has a different meaning than None!
    """

    # configuration section name
    name = "compare-to-empty-string"
    msgs = {
        "C1901": (
            "Avoid comparisons to empty string",
            "compare-to-empty-string",
            "Used when Pylint detects comparison to an empty string constant.",
        )
    }

    options = ()

    @utils.only_required_for_messages("compare-to-empty-string")
    def visit_compare(self, node: nodes.Compare) -> None:
        _operators = ["!=", "==", "is not", "is"]
        # note: astroid.Compare has the left most operand in node.left
        # while the rest are a list of tuples in node.ops
        # the format of the tuple is ('compare operator sign', node)
        # here we squash everything into `ops` to make it easier for processing later
        ops = [("", node.left)]
        ops.extend(node.ops)
        iter_ops: Iterable[Any] = iter(ops)
        ops = list(itertools.chain(*iter_ops))

        for ops_idx in range(len(ops) - 2):
            op_1 = ops[ops_idx]
            op_2 = ops[ops_idx + 1]
            op_3 = ops[ops_idx + 2]
            error_detected = False

            # x ?? ""
            if utils.is_empty_str_literal(op_1) and op_2 in _operators:
                error_detected = True
            # '' ?? X
            elif op_2 in _operators and utils.is_empty_str_literal(op_3):
                error_detected = True

            if error_detected:
                self.add_message("compare-to-empty-string", node=node)


def register(linter: PyLinter) -> None:
    linter.register_checker(CompareToEmptyStringChecker(linter))
