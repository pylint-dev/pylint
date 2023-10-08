# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Function checker for Python code."""

from __future__ import annotations

from astroid import nodes

from pylint.checkers import utils
from pylint.checkers.base.basic_checker import _BasicChecker


class FunctionChecker(_BasicChecker):
    """Check if a function definition handles possible side effects."""

    name = "function"
    msgs = {
        "W9999": (  # TODO: change this warning code number
            "Unhandled generator cleanup in contextmanager",
            "contextmanager-generator-missing-cleanup",
            "Used when a generator is used in a contextmanager"
            " and the cleanup is not handled.",
        )
    }

    @utils.only_required_for_messages("contextmanager-generator-missing-cleanup")
    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        pass
