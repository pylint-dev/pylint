# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Checker for features used that are not supported by all python versions
indicated by the py-version setting.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import (
    is_lazy_import,
    only_required_for_messages,
    safe_infer,
    uninferable_final_decorators,
)
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class UnsupportedVersionChecker(BaseChecker):
    """Checker for features that are not supported by all python versions
    indicated by the py-version setting.
    """

    name = "unsupported_version"
    msgs = {
        "W2601": (
            "F-strings are not supported by all versions included in the py-version setting",
            "using-f-string-in-unsupported-version",
            "Used when the py-version set by the user is lower than 3.6 and pylint encounters "
            "an f-string.",
        ),
        "W2602": (
            "typing.final is not supported by all versions included in the py-version setting",
            "using-final-decorator-in-unsupported-version",
            "Used when the py-version set by the user is lower than 3.8 and pylint encounters "
            "a ``typing.final`` decorator.",
        ),
        "W2603": (
            "Exception groups are not supported by all versions included in the py-version setting",
            "using-exception-groups-in-unsupported-version",
            "Used when the py-version set by the user is lower than 3.11 and pylint encounters "
            "``except*`` or `ExceptionGroup``.",
        ),
        "W2604": (
            "Generic type syntax (PEP 695) is not supported by all versions included in the py-version setting",
            "using-generic-type-syntax-in-unsupported-version",
            "Used when the py-version set by the user is lower than 3.12 and pylint encounters "
            "generic type syntax.",
        ),
        "W2605": (
            "Assignment expression is not supported by all versions included in the py-version setting",
            "using-assignment-expression-in-unsupported-version",
            "Used when the py-version set by the user is lower than 3.8 and pylint encounters "
            "an assignment expression (walrus) operator.",
        ),
        "W2606": (
            "Positional-only arguments are not supported by all versions included in the py-version setting",
            "using-positional-only-args-in-unsupported-version",
            "Used when the py-version set by the user is lower than 3.8 and pylint encounters "
            "positional-only arguments.",
        ),
        "W2607": (
            "Unpacking in comprehensions is not supported by all versions included in the py-version setting",
            "using-comprehension-unpacking-in-unsupported-version",
            "Used when the py-version set by the user is lower than 3.15 and pylint encounters "
            "the ``*`` or ``**`` unpacking added by PEP 798 in a comprehension.",
        ),
        "W2608": (
            "Lazy imports are not supported by all versions included in the py-version setting",
            "using-lazy-import-in-unsupported-version",
            "Used when the py-version set by the user is lower than 3.15 and pylint encounters "
            "the ``lazy`` import added by PEP 810.",
        ),
    }

    def open(self) -> None:
        """Initialize visit variables and statistics."""
        py_version = self.linter.config.py_version
        self._py36_plus = py_version >= (3, 6)
        self._py38_plus = py_version >= (3, 8)
        self._py311_plus = py_version >= (3, 11)
        self._py312_plus = py_version >= (3, 12)
        self._py315_plus = py_version >= (3, 15)

    @only_required_for_messages("using-f-string-in-unsupported-version")
    def visit_joinedstr(self, node: nodes.JoinedStr) -> None:
        """Check f-strings."""
        if not self._py36_plus:
            self.add_message(
                "using-f-string-in-unsupported-version", node=node, confidence=HIGH
            )

    @only_required_for_messages("using-assignment-expression-in-unsupported-version")
    def visit_namedexpr(self, node: nodes.JoinedStr) -> None:
        if not self._py38_plus:
            self.add_message(
                "using-assignment-expression-in-unsupported-version",
                node=node,
                confidence=HIGH,
            )

    @only_required_for_messages("using-positional-only-args-in-unsupported-version")
    def visit_arguments(self, node: nodes.Arguments) -> None:
        if not self._py38_plus and node.posonlyargs:
            self.add_message(
                "using-positional-only-args-in-unsupported-version",
                node=node,
                confidence=HIGH,
            )

    @only_required_for_messages("using-final-decorator-in-unsupported-version")
    def visit_decorators(self, node: nodes.Decorators) -> None:
        """Check decorators."""
        self._check_typing_final(node)

    def _check_typing_final(self, node: nodes.Decorators) -> None:
        """Add a message when the `typing.final` decorator is used and the
        py-version is lower than 3.8.
        """
        if self._py38_plus:
            return

        decorators = []
        for decorator in node.get_children():
            inferred = safe_infer(decorator)
            if inferred and inferred.qname() == "typing.final":
                decorators.append(decorator)

        for decorator in decorators or uninferable_final_decorators(node):
            self.add_message(
                "using-final-decorator-in-unsupported-version",
                node=decorator,
                confidence=HIGH,
            )

    @only_required_for_messages("using-exception-groups-in-unsupported-version")
    def visit_trystar(self, node: nodes.TryStar) -> None:
        if not self._py311_plus:
            self.add_message(
                "using-exception-groups-in-unsupported-version",
                node=node,
                confidence=HIGH,
            )

    @only_required_for_messages("using-exception-groups-in-unsupported-version")
    def visit_excepthandler(self, node: nodes.ExceptHandler) -> None:
        if (
            not self._py311_plus
            and isinstance(node.type, nodes.Name)
            and node.type.name == "ExceptionGroup"
        ):
            self.add_message(
                "using-exception-groups-in-unsupported-version",
                node=node,
                confidence=HIGH,
            )

    @only_required_for_messages("using-exception-groups-in-unsupported-version")
    def visit_raise(self, node: nodes.Raise) -> None:
        if (
            not self._py311_plus
            and isinstance(node.exc, nodes.Call)
            and isinstance(node.exc.func, nodes.Name)
            and node.exc.func.name == "ExceptionGroup"
        ):
            self.add_message(
                "using-exception-groups-in-unsupported-version",
                node=node,
                confidence=HIGH,
            )

    @only_required_for_messages("using-generic-type-syntax-in-unsupported-version")
    def visit_typealias(self, node: nodes.TypeAlias) -> None:
        if not self._py312_plus:
            self.add_message(
                "using-generic-type-syntax-in-unsupported-version",
                node=node,
                confidence=HIGH,
            )

    @only_required_for_messages("using-generic-type-syntax-in-unsupported-version")
    def visit_typevar(self, node: nodes.TypeVar) -> None:
        if not self._py312_plus:
            self.add_message(
                "using-generic-type-syntax-in-unsupported-version",
                node=node,
                confidence=HIGH,
            )

    @only_required_for_messages("using-generic-type-syntax-in-unsupported-version")
    def visit_typevartuple(self, node: nodes.TypeVarTuple) -> None:
        if not self._py312_plus:
            self.add_message(
                "using-generic-type-syntax-in-unsupported-version",
                node=node,
                confidence=HIGH,
            )

    @only_required_for_messages("using-comprehension-unpacking-in-unsupported-version")
    def visit_listcomp(self, node: nodes.ListComp) -> None:
        self._check_comprehension_unpacking(node)

    @only_required_for_messages("using-comprehension-unpacking-in-unsupported-version")
    def visit_setcomp(self, node: nodes.SetComp) -> None:
        self._check_comprehension_unpacking(node)

    @only_required_for_messages("using-comprehension-unpacking-in-unsupported-version")
    def visit_generatorexp(self, node: nodes.GeneratorExp) -> None:
        self._check_comprehension_unpacking(node)

    def _check_comprehension_unpacking(
        self, node: nodes.ListComp | nodes.SetComp | nodes.GeneratorExp
    ) -> None:
        """Add a message for ``[*element for element in elements]`` when the
        py-version is lower than 3.15.
        """
        if not self._py315_plus and isinstance(node.elt, nodes.Starred):
            self.add_message(
                "using-comprehension-unpacking-in-unsupported-version",
                node=node,
                confidence=HIGH,
            )

    @only_required_for_messages("using-comprehension-unpacking-in-unsupported-version")
    def visit_dictcomp(self, node: nodes.DictComp) -> None:
        """Add a message for ``{**element for element in elements}``.

        astroid represents that unpacking with a ``DictUnpack`` key.
        """
        if not self._py315_plus and isinstance(node.key, nodes.DictUnpack):
            self.add_message(
                "using-comprehension-unpacking-in-unsupported-version",
                node=node,
                confidence=HIGH,
            )

    @only_required_for_messages("using-lazy-import-in-unsupported-version")
    def visit_import(self, node: nodes.Import) -> None:
        self._check_lazy_import(node)

    @only_required_for_messages("using-lazy-import-in-unsupported-version")
    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        self._check_lazy_import(node)

    def _check_lazy_import(self, node: nodes.Import | nodes.ImportFrom) -> None:
        """Add a message for ``lazy import elements`` when the py-version is
        lower than 3.15.
        """
        if not self._py315_plus and is_lazy_import(node):
            self.add_message(
                "using-lazy-import-in-unsupported-version",
                node=node,
                confidence=HIGH,
            )


def register(linter: PyLinter) -> None:
    linter.register_checker(UnsupportedVersionChecker(linter))
