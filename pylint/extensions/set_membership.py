# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from typing import TYPE_CHECKING

import astroid
from astroid import bases, nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages

if TYPE_CHECKING:
    from astroid.typing import InferenceResult

    from pylint.lint import PyLinter


_UNHASHABLE_LITERAL_NODES = (
    nodes.Starred,
    nodes.List,
    nodes.Dict,
    nodes.Set,
    nodes.ListComp,
    nodes.DictComp,
    nodes.SetComp,
)

_HASHABLE_CALLABLE_NODES = (
    nodes.FunctionDef,
    nodes.Lambda,
    bases.BoundMethod,
    bases.UnboundMethod,
)

_ALWAYS_HASHABLE_INFERRED_NODES = (
    nodes.Const,
    nodes.Module,
    *_HASHABLE_CALLABLE_NODES,
)


def _is_provably_non_none_hash_def(hash_def: nodes.NodeNG) -> bool:
    """Return True if every inferred value of a __hash__ definition is callable."""
    found = False
    try:
        for inferred in hash_def.infer():
            found = True
            if not isinstance(inferred, _HASHABLE_CALLABLE_NODES):
                return False
    except astroid.InferenceError:
        return False
    return found


def _has_hashable_instances(cls: nodes.ClassDef) -> bool:
    """Return True if instances of `cls` are provably hashable."""
    try:
        mro = cls.mro()
    except astroid.MroError:
        return False

    for base in mro:
        if base.qname() == "builtins.tuple":
            return False
        if "__hash__" in base.locals:
            return all(
                _is_provably_non_none_hash_def(hash_def)
                for hash_def in base.locals["__hash__"]
            )
        if "__eq__" in base.locals or base.is_dataclass:
            return False

    return False


def _is_inferred_hashable(
    inferred: InferenceResult, visited: frozenset[nodes.NodeNG]
) -> bool:
    """Return True if an inferred astroid object is provably hashable."""
    if isinstance(inferred, _ALWAYS_HASHABLE_INFERRED_NODES):
        return True
    if isinstance(inferred, nodes.Tuple):
        return _is_provably_hashable(inferred, visited)
    if isinstance(inferred, nodes.ClassDef):
        metaclass = inferred.metaclass()
        if metaclass is None:
            return inferred._metaclass is None
        return isinstance(metaclass, nodes.ClassDef) and _has_hashable_instances(
            metaclass
        )
    if isinstance(inferred, bases.Instance):
        return _has_hashable_instances(inferred._proxied)
    return False


def _is_provably_hashable(
    node: nodes.NodeNG, visited: frozenset[nodes.NodeNG] = frozenset()
) -> bool:
    """Return True if every possible value of `node` is provably hashable."""
    if isinstance(node, nodes.Const):
        return True
    if isinstance(node, _UNHASHABLE_LITERAL_NODES):
        return False
    if isinstance(node, nodes.Tuple):
        if node in visited:
            return False
        next_visited = visited | {node}
        return all(_is_provably_hashable(elt, next_visited) for elt in node.elts)

    found = False
    try:
        for inferred in node.infer():
            found = True
            if not _is_inferred_hashable(inferred, visited):
                return False
    except astroid.InferenceError:
        return False
    return found


class SetMembershipChecker(BaseChecker):
    name = "set_membership"
    msgs = {
        "R6201": (
            "Consider using set for membership test",
            "use-set-for-membership",
            "Membership tests are more efficient when performed on "
            "a lookup optimized datatype like ``sets``.",
        ),
    }

    def __init__(self, linter: PyLinter) -> None:
        """Initialize checker instance."""
        super().__init__(linter=linter)

    @only_required_for_messages("use-set-for-membership")
    def visit_compare(self, node: nodes.Compare) -> None:
        for op, comparator in node.ops:
            if op == "in":
                self._check_in_comparison(comparator)

    def _check_in_comparison(self, comparator: nodes.NodeNG) -> None:
        """Checks for membership comparisons with in-place container objects."""
        if not isinstance(comparator, nodes.BaseContainer) or isinstance(
            comparator, nodes.Set
        ):
            return

        # Heuristic - We need to be sure all items in set are hashable
        if all(_is_provably_hashable(item) for item in comparator.elts):
            self.add_message("use-set-for-membership", node=comparator)


def register(linter: PyLinter) -> None:
    linter.register_checker(SetMembershipChecker(linter))
