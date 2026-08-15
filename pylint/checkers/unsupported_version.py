# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Checker for features used and version checks made that do not agree with the
py-version setting.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import (
    REVERSED_COMPS,
    is_sys_version_info,
    only_required_for_messages,
    safe_infer,
    uninferable_final_decorators,
)
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def _oldest_supported_value(
    node: nodes.NodeNG, py_version: tuple[int, ...]
) -> tuple[bool, tuple[int, ...]] | None:
    """Evaluate a ``sys.version_info`` expression for the oldest supported interpreter.

    With ``py-version=3.10``, so ``py_version`` being ``(3, 10)``::

        sys.version_info        ->  (False, (3, 10))
        sys.version_info[:2]    ->  (False, (3, 10))
        sys.version_info[:1]    ->  (False, (3,))
        sys.version_info[0]     ->  (True, (3,))
        sys.version_info.major  ->  (True, (3,))
        sys.version_info.minor  ->  None
        sys.version_info[1]     ->  None
        sys.version_info[1:]    ->  None
        anything_else           ->  None

    The first item says whether the expression is a plain number instead of a
    tuple, so that ``sys.version_info[0] >= (3, 10)`` — a ``TypeError`` when it
    runs — is never decided here.

    ``minor`` gets ``None`` because it goes back to 0 on a new major release: it
    does not grow with the interpreter version, unlike the whole tuple and the
    slices that start at the major version.
    """
    if is_sys_version_info(node):
        return False, py_version
    if isinstance(node, nodes.Attribute) and is_sys_version_info(node.expr):
        return (True, py_version[:1]) if node.attrname == "major" else None
    if not isinstance(node, nodes.Subscript) or not is_sys_version_info(node.value):
        return None
    index = node.slice
    if isinstance(index, nodes.Const):
        return (True, py_version[:1]) if index.value == 0 else None
    if not isinstance(index, nodes.Slice) or index.step is not None:
        return None
    if index.lower is not None and not (
        isinstance(index.lower, nodes.Const) and index.lower.value == 0
    ):
        return None
    if index.upper is None:
        return False, py_version
    if isinstance(index.upper, nodes.Const) and isinstance(index.upper.value, int):
        return False, py_version[: index.upper.value]
    return None


def _version_constant(node: nodes.NodeNG) -> tuple[bool, tuple[int, ...]] | None:
    """Return the integer or integer tuple literal that node is, if any."""
    if isinstance(node, nodes.Const):
        return (True, (node.value,)) if isinstance(node.value, int) else None
    if not isinstance(node, nodes.Tuple) or not node.elts:
        return None
    values = []
    for element in node.elts:
        if not isinstance(element, nodes.Const) or not isinstance(element.value, int):
            return None
        values.append(element.value)
    return False, tuple(values)


def _constant_comparison_result(
    operator: str, oldest: tuple[int, ...], constant: tuple[int, ...]
) -> str | None:
    """Return the outcome shared by every supported interpreter, if there is one.

    The set of supported versions has no upper bound, so a comparison can only be
    decided by its lower bound: ``sys.version_info < x`` is never always true.
    """
    if operator in {">=", "<"}:
        decided = oldest >= constant
    else:
        decided = oldest > constant
    if not decided:
        return None
    return "True" if operator in {">=", ">", "!="} else "False"


class UnsupportedVersionChecker(BaseChecker):
    """Checker for features used and version checks made that do not agree with
    the py-version setting.
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
            "'%s' is always %s for the Python versions supported by py-version (%s)",
            "useless-version-check",
            "Emitted when a ``sys.version_info`` comparison can only have one outcome "
            "for the interpreters allowed by the py-version setting, so the branch it "
            "guards is dead code. Disabled by default: it is meant to be run once when "
            "you drop the maintenance of a Python interpreter, and py-version defaults "
            "to the interpreter running pylint rather than to the oldest one you "
            "support.",
            {"default_enabled": False},
        ),
    }

    def open(self) -> None:
        """Initialize visit variables and statistics."""
        py_version = self.linter.config.py_version
        self._py_version = py_version
        self._py_version_string = ".".join(str(part) for part in py_version)
        self._py36_plus = py_version >= (3, 6)
        self._py38_plus = py_version >= (3, 8)
        self._py311_plus = py_version >= (3, 11)
        self._py312_plus = py_version >= (3, 12)

    @only_required_for_messages("useless-version-check")
    def visit_compare(self, node: nodes.Compare) -> None:
        """Check ``sys.version_info`` comparisons that py-version already decides."""
        if len(node.ops) != 1:
            return
        operator, right = node.ops[0]
        if operator not in REVERSED_COMPS:
            return

        projection = _oldest_supported_value(node.left, self._py_version)
        constant = _version_constant(right)
        if projection is None or constant is None:
            # I.e. ``(3, 8) <= sys.version_info``
            projection = _oldest_supported_value(right, self._py_version)
            constant = _version_constant(node.left)
            operator = REVERSED_COMPS[operator]
        if projection is None or constant is None:
            return

        is_scalar, oldest = projection
        constant_is_scalar, expected = constant
        if is_scalar is not constant_is_scalar:
            # Comparing a tuple with an int always raises a TypeError
            return
        # py-version omits the parts it does not constrain: 3.10 means 3.10.0
        oldest += (0,) * (len(expected) - len(oldest))

        result = _constant_comparison_result(operator, oldest, expected)
        if result is None:
            return
        self.add_message(
            "useless-version-check",
            node=node,
            args=(node.as_string(), result, self._py_version_string),
            confidence=HIGH,
        )

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


def register(linter: PyLinter) -> None:
    linter.register_checker(UnsupportedVersionChecker(linter))
