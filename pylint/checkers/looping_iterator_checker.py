# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pylint import checkers, interfaces
from pylint.checkers import utils

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class RepeatedIteratorLoopChecker(checkers.BaseChecker):
    """Checks for exhaustible iterators that are reused in a nested loop."""

    name = "looping-through-iterator"
    msgs = {
        "W4801": (
            "Iterator '%s' from an outer scope is reused or consumed in a nested loop.",
            "looping-through-iterator",
            "Used when an iterator defined in an outer loop scope is consumed in a "
            "nested loop. Because iterators are stateful and exhausted upon consumption, "
            "the inner loop will fully consume the iterator during the first iteration "
            "of the outer loop, leaving it empty for all subsequent iterations.",
        )
    }

    options = ()

    # Callables that return a single, finite, one-shot iterator. Generator
    # functions defined with ``yield`` are detected structurally with
    # ``is_generator()`` instead. Deliberately excluded: ``itertools.tee``
    # (returns a tuple of iterators), ``itertools.count``/``cycle`` (infinite,
    # so the "exhausted on the second pass" pattern does not apply) and the
    # re-iterable ``dict`` views.
    KNOWN_ITERATOR_PRODUCING_FUNCTION_QNAMES: set[str] = {
        "builtins.map",
        "builtins.filter",
        "builtins.zip",
        "builtins.iter",
        "builtins.reversed",
        "builtins.enumerate",
        "itertools.chain",
        "itertools.islice",
        "itertools.groupby",
        "itertools.starmap",
        "itertools.accumulate",
        "itertools.product",
        "itertools.permutations",
        "itertools.combinations",
        "itertools.combinations_with_replacement",
        "itertools.compress",
        "itertools.dropwhile",
        "itertools.takewhile",
        "itertools.filterfalse",
        "itertools.zip_longest",
        "itertools.pairwise",
        "itertools.batched",
    }

    def __init__(self, linter: PyLinter) -> None:
        super().__init__(linter)
        self._scope_stack: list[dict[str, nodes.NodeNG | str]] = []

    # --- Scope Management ---

    @utils.only_required_for_messages("looping-through-iterator")
    def visit_module(self, _node: nodes.Module) -> None:
        self._scope_stack = [{}]

    @utils.only_required_for_messages("looping-through-iterator")
    def visit_functiondef(self, _node: nodes.FunctionDef) -> None:
        self._scope_stack.append({})

    @utils.only_required_for_messages("looping-through-iterator")
    def leave_functiondef(self, _node: nodes.FunctionDef) -> None:
        self._scope_stack.pop()

    @utils.only_required_for_messages("looping-through-iterator")
    def visit_for(self, node: nodes.For) -> None:
        # The variables created by the for loop itself (e.g., `i` in `for i in ...`)
        # are not iterators we need to track; they are the items. We mark them
        # as "SAFE" in the current scope to prevent false positives.
        for target in node.target.nodes_of_class(nodes.AssignName):
            self._scope_stack[-1][target.name] = "SAFE"

        # The body of the loop has its own new scope.
        self._scope_stack.append({})
        # Now, check the iterator being looped over.
        if isinstance(node.iter, nodes.Name):
            self._check_variable_usage(node.iter)

    @utils.only_required_for_messages("looping-through-iterator")
    def leave_for(self, _node: nodes.For) -> None:
        self._scope_stack.pop()

    # --- State Building & Reactive Checks ---

    @utils.only_required_for_messages("looping-through-iterator")
    def visit_assign(self, node: nodes.Assign) -> None:
        value_node = node.value
        is_iterator_definition = False
        if isinstance(value_node, nodes.GeneratorExp):
            is_iterator_definition = True
        elif isinstance(value_node, nodes.Call):
            # Use `safe_infer` for a robust check of the function being called
            inferred_func = utils.safe_infer(value_node.func)
            if inferred_func is not None:
                # A call to a user-defined generator function returns a one-shot
                # generator, just like the known builtins below.
                if (
                    isinstance(inferred_func, nodes.FunctionDef)
                    and inferred_func.is_generator()
                ):
                    is_iterator_definition = True
                elif (
                    hasattr(inferred_func, "qname")
                    and inferred_func.qname()
                    in self.KNOWN_ITERATOR_PRODUCING_FUNCTION_QNAMES
                ):
                    is_iterator_definition = True

        current_scope = self._scope_stack[-1]
        for target in node.targets:
            if isinstance(target, nodes.AssignName):
                variable_name = target.name
                if is_iterator_definition:
                    current_scope[variable_name] = value_node
                else:
                    current_scope[variable_name] = "SAFE"

    @utils.only_required_for_messages("looping-through-iterator")
    def visit_call(self, node: nodes.Call) -> None:
        # When the user use 'next' it's easy to raise a false positive
        # and the user usually know what they do so. the primer looked
        # especially bad.
        if isinstance(node.func, nodes.Name) and node.func.name == "next":
            return
        for arg in node.args:
            if isinstance(arg, nodes.Name):
                self._check_variable_usage(arg)

    # --- Core Logic ---

    def _has_direct_unconditional_exit(self, statements: list[nodes.NodeNG]) -> bool:
        """Only checks top-level statements, no branching logic."""
        return any(
            isinstance(stmt, (nodes.Return, nodes.Break, nodes.Raise))
            for stmt in statements
        )

    def _check_variable_usage(self, usage_node: nodes.Name) -> None:
        """
        When a variable is used, this method checks if it is a reused
        exhaustible iterator inside a nested loop.
        """
        iterator_name = usage_node.name

        # 1. Find the true definition of this variable by searching our scope stack.
        definition = None
        for scope in reversed(self._scope_stack):
            if iterator_name in scope:
                definition = scope[iterator_name]
                break

        if not definition or definition == "SAFE":
            return

        # 2. Get all ancestor loops of the USAGE node, innermost first.
        ancestor_loops_of_usage = self._enclosing_for_loops(usage_node)

        if len(ancestor_loops_of_usage) < 2:
            # Usage is not in a nested loop, so it's safe.
            return

        # 3. Find where the iterator gets redefined, if at all. The definition is
        # refreshed on every iteration of the loop that directly contains it, so
        # that loop (and anything outside it) cannot expose a stale iterator.
        definition_loops = self._enclosing_for_loops(definition)
        definition_loop = definition_loops[0] if definition_loops else None
        if definition_loop in ancestor_loops_of_usage:
            redefinition_boundary = ancestor_loops_of_usage.index(definition_loop)
        else:
            # Defined outside every loop enclosing the usage (module/function
            # scope, or an unrelated sibling loop): never refreshed.
            redefinition_boundary = len(ancestor_loops_of_usage)

        # The consuming loop is ``ancestor_loops_of_usage[0]``. Any loop *between*
        # it and the redefinition re-runs the consumption without refreshing the
        # iterator -- that is the bug, at any nesting depth. If there is no such
        # loop, the iterator is refreshed on every repetition and we are safe.
        repeating_loops = ancestor_loops_of_usage[1:redefinition_boundary]
        if not repeating_loops:
            return

        inner_loop = ancestor_loops_of_usage[0]
        enclosing_loop = ancestor_loops_of_usage[1]

        if inner_loop.orelse and self._has_direct_unconditional_exit(inner_loop.orelse):
            # ``for ... else: raise`` is a deliberate fail-fast cursor.
            return

        if inner_loop not in enclosing_loop.body:
            # The inner loop is nested under some other statement (e.g. an
            # ``if``) rather than directly in the enclosing loop's body. Stay
            # conservative and emit no message.
            return
        inner_loop_index = enclosing_loop.body.index(inner_loop)
        statements_after_inner_loop = enclosing_loop.body[inner_loop_index + 1 :]
        if self._has_direct_unconditional_exit(statements_after_inner_loop):
            # The enclosing loop exits unconditionally after consuming the
            # iterator, so it never re-enters with an exhausted iterator.
            return

        self.add_message(
            "looping-through-iterator",
            node=usage_node,
            args=(iterator_name,),
            confidence=interfaces.HIGH,
        )

    # --- Helper Method ---

    def _enclosing_for_loops(self, node: nodes.NodeNG) -> list[nodes.For]:
        """Return the ``for`` loops enclosing ``node``, innermost first.

        Modeled on the astroid ``_get_if_statement_ancestor`` walk, but collects
        every enclosing loop and stops at the first scope boundary so a loop
        from an outer scope is never mistaken for one nesting the node.
        """
        loops: list[nodes.For] = []
        for parent in node.node_ancestors():
            if isinstance(parent, nodes.For):
                loops.append(parent)
            elif isinstance(parent, (nodes.FunctionDef, nodes.ClassDef, nodes.Module)):
                break
        return loops


def register(linter: PyLinter) -> None:
    linter.register_checker(RepeatedIteratorLoopChecker(linter))
