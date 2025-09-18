# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import logging  # Added for debugging
from typing import TYPE_CHECKING, Set, Dict, Union, List

from astroid import Uninferable, nodes
from astroid.exceptions import InferenceError

from pylint import checkers, interfaces
from pylint.checkers import utils

if TYPE_CHECKING:
    from pylint.lint import PyLinter

DefinitionType = Union[nodes.NodeNG, str]

class RepeatedIteratorLoopChecker(checkers.BaseChecker):
    """
    Checks for exhaustible iterators that are re-used in a nested loop.
    """


    name = "looping-through-iterator"
    msgs = {
        "W4801": (
            "Iterator '%s' from an outer scope is re-used or consumed in a nested loop.",
            "looping-through-iterator",
            "...",
        )
    }

    options = ()

    KNOWN_ITERATOR_PRODUCING_FUNCTIONS: Set[str] = {
        "builtins.map", "builtins.filter", "builtins.zip", "builtins.iter", "builtins.reversed"
    }

    def __init__(self, linter: PyLinter | None = None) -> None:
        super().__init__(linter)
        self._scope_stack: List[Dict[str, DefinitionType]] = []

    # --- Scope Management ---

    def visit_module(self, node: nodes.Module) -> None:
        self._scope_stack = [{}]

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        self._scope_stack.append({})

    def leave_functiondef(self, node: nodes.FunctionDef) -> None:
        self._scope_stack.pop()

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

    def leave_for(self, node: nodes.For) -> None:
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
            if inferred_func and hasattr(inferred_func, "qname"):
                if inferred_func.qname() in self.KNOWN_ITERATOR_PRODUCING_FUNCTIONS:
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
        for arg in node.args:
            if isinstance(arg, nodes.Name):
                self._check_variable_usage(arg)

    # --- Core Logic ---

    def _check_variable_usage(self, usage_node: nodes.Name) -> None:
        """
        When a variable is used, this method checks if it is a re-used
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

        # 2. Get all ancestor loops of the USAGE node.
        ancestor_loops_of_usage = []
        current: nodes.NodeNG | None = usage_node
        while (loop := self._find_ancestor_loop(current)):
            ancestor_loops_of_usage.append(loop)
            current = loop.parent

        if len(ancestor_loops_of_usage) < 2:
            # Usage is not in a nested loop, so it's safe.
            return

        # 3. Get the loop that directly contains the DEFINITION.
        definition_loop = self._find_ancestor_loop(definition)

        # 4. THE FINAL RULE: The usage is unsafe if the definition was not created
        #    within one of the loops that contains the usage.
        if definition_loop not in ancestor_loops_of_usage:
            self.add_message(
                "looping-through-iterator",
                node=usage_node,
                args=(iterator_name,),
                confidence=interfaces.HIGH,
            )

    # --- Helper Methods ---

    def _find_ancestor_loop(self, node: nodes.NodeNG) -> nodes.For | nodes.While | None:
        """Walks up the AST from a node to find the first containing loop."""
        current: nodes.NodeNG | None = node
        while current:
            if isinstance(current, (nodes.For, nodes.While)):
                return current
            if isinstance(current, (nodes.FunctionDef, nodes.ClassDef, nodes.Module)):
                return None
            current = current.parent
        return None

def register(linter: PyLinter) -> None:
    """This required function is called by Pylint to register the checker."""
    linter.register_checker(RepeatedIteratorLoopChecker(linter))
