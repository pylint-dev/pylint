# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Function checker for Python code."""

from __future__ import annotations

from collections import deque
from typing import Union

from astroid import nodes

from pylint.checkers import utils
from pylint.checkers.base.basic_checker import _BasicChecker

_GeneratorTree = Union[nodes.Try, nodes.Assign, nodes.Expr]


class FunctionChecker(_BasicChecker):
    """Check if a function definition handles possible side effects."""

    name = "function"
    msgs = {
        "W9999": (  # TODO: change this warning code number
            "Unhandled generator cleanup in contextmanager function %s",
            "contextmanager-generator-missing-cleanup",
            "Used when a generator is used in a contextmanager"
            " and the cleanup is not handled.",
        )
    }

    @utils.only_required_for_messages("contextmanager-generator-missing-cleanup")
    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        self._check_contextmanager_generator_missing_cleanup(node)

    def _check_contextmanager_generator_missing_cleanup(
        self, node: nodes.FunctionDef
    ) -> None:
        """Check a FunctionDef to see if it uses `contextmanager` on a generator
        function.

        The following code sample will never print the message **cm exit**::

            from contextlib import contextmanager

            @contextmanager
            def cm():
                print("cm enter")
                a = yield
                print('cm exit')

            def genfunc():
                with cm():
                    print("stepping")
                    yield

            def main():
                gen = genfunc()
                ref = weakref.ref(gen, print)
                next(gen)

        The function ``cm`` needs to include error handling for ``GeneratorExit``
        to properly finish the function execution.

        :param node: FunctionDef node to check
        :type node: nodes.FunctionDef
        """
        contextmanager_str = "contextmanager"
        if node.decorators is None:
            return

        decorator_list = node.decorators.nodes
        if not any(
            contextmanager_str == self._get_name(deco) for deco in decorator_list
        ):
            # No contextmanager decorator
            return

        # A ``yield`` statement can either be Expr or Assign, but the value is always of Yield
        # Additionally a good function could be input where the yield is already wrapped by a Try
        # but not have the required Handler or Finally
        body_nodes = self._find_yield_nodes(node)
        yield_nodes: list[nodes.Yield] = []
        for n in body_nodes:
            if not isinstance(n, nodes.Try):
                yield_nodes.append(n)
                continue
            # This Try Node has a Yield inside of it, making this a generator function wrapped
            # by contextlib.contextmanager. See if handlers or finally is present
            if (
                any(
                    self._get_name(handler.type) == "GeneratorExit"
                    for handler in n.handlers
                )
                or n.finalbody
            ):
                continue

            # this Try block doesn't properly handle GeneratorExit, add warning
            self.add_message(
                "contextmanager-generator-missing-cleanup", node=node, args=(node.name,)
            )
            return

        if yield_nodes:
            self.add_message(
                "contextmanager-generator-missing-cleanup", node=node, args=(node.name,)
            )

    @staticmethod
    def _get_name(node: nodes.NodeNG) -> str:
        """Helper function to get the name from a node.

        Helpful when possible to have a Name or Attribute node.

        :param node: Node to get name of
        :type node: nodes.NodeNG
        :return: string name
        :rtype: str
        """
        if hasattr(node, "name"):
            return node.name  # type: ignore[no-untype-def]
        if hasattr(node, "attrname"):
            return node.attrname  # type: ignore[no-untype-def]
        return node.as_string()  # type: ignore[no-untype-def]

    @staticmethod
    def _find_yield_nodes(node: nodes.FunctionDef) -> list[_GeneratorTree]:
        """Return all yield statements, possibly wrapped by a Try node.

        If a yield keyword is used inside a Try block, return the Try node.
        Otherwise return the node of the yield.
        Returns all such occurrences.

        :param node: Function root to check
        :type node: nodes.FunctionDef
        :return: List of found nodes
        :rtype: list[_GeneratorTree]
        """

        def get_body_nodes(n: nodes.NodeNG) -> list[nodes.NodeNG]:
            if hasattr(n, "body"):
                return n.body  # type: ignore[no-any-return]
            return []

        found_nodes: list[_GeneratorTree] = []
        # keep track of (current_node, TryParent | None)
        queue: deque[tuple[nodes.NodeNG, nodes.Try | None]] = deque([(node, None)])
        while queue:
            curr_node, try_parent = queue.popleft()
            if hasattr(curr_node, "value") and isinstance(curr_node.value, nodes.Yield):
                # If current node is a Expr/Assign etc, with a Yield add to output
                found_nodes.append(curr_node if try_parent is None else try_parent)
            if isinstance(curr_node, nodes.Try) and try_parent is None:
                # TODO: should this change Try block parent in the not None case?
                # isn't it code smell to try: try: try: ...
                try_parent = curr_node
            queue.extend(
                (body_node, curr_node) for body_node in get_body_nodes(curr_node)
            )

        return found_nodes
