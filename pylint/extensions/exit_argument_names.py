# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Optional checker for the argument names of ``__exit__`` and ``__aexit__``."""

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker, utils
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint import PyLinter

EXIT_METHODS = frozenset(("__exit__", "__aexit__"))
EXPECTED_ARGUMENT_NAMES = ("exc_type", "exc_value", "traceback")


class ExitArgumentNamesChecker(BaseChecker):
    """Checks that ``__exit__`` and ``__aexit__`` use the argument names of the
    Python data model documentation.
    """

    name = "exit-argument-names"
    msgs = {
        "C3801": (
            "Arguments of %s should be named '%s' instead of '%s'",
            "non-standard-exit-argument-names",
            "Used when the three arguments of a ``__exit__`` or ``__aexit__`` method "
            "are not named ``exc_type, exc_value, traceback``, as in the Python data "
            "model documentation. Arguments matching ``ignored-argument-names`` are "
            "not checked.",
        ),
    }

    @utils.only_required_for_messages("non-standard-exit-argument-names")
    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        if node.name not in EXIT_METHODS or not node.is_method():
            return
        if node.type != "method":
            # staticmethod / classmethod: the arguments are shifted, skip them.
            return
        arguments = node.args
        if arguments.vararg or arguments.kwarg:
            return
        positional = [*arguments.posonlyargs, *arguments.args]
        if len(positional) != 4:
            # Wrong arity is reported by unexpected-special-method-signature.
            return
        names = [arg.name for arg in positional[1:]]
        ignored = self.linter.config.ignored_argument_names
        if all(
            name == expected or (ignored and ignored.match(name))
            for name, expected in zip(names, EXPECTED_ARGUMENT_NAMES)
        ):
            return
        self.add_message(
            "non-standard-exit-argument-names",
            node=node,
            args=(
                node.name,
                ", ".join(EXPECTED_ARGUMENT_NAMES),
                ", ".join(names),
            ),
            confidence=HIGH,
        )

    visit_asyncfunctiondef = visit_functiondef


def register(linter: PyLinter) -> None:
    linter.register_checker(ExitArgumentNamesChecker(linter))
