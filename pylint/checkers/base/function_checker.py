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

    msgs = {
        "W0135": (
            "The code after line %s will never be executed ('GeneratorExit' needs to be handled)",
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
        body_nodes: list[nodes.Yield | nodes.Try] = list(
            node.nodes_of_class((nodes.Yield, nodes.Try))
        )
        yield_nodes: list[nodes.Yield] = []
        for n in body_nodes:
            if not isinstance(n, nodes.Try):
                yield_nodes.append(n)
                continue
            if not n.nodes_of_class(nodes.Yield):
                # if Try has no Yield inside it, ignore
                continue
            # This Try Node has a Yield inside of it, making this a generator function wrapped
            # by contextlib.contextmanager. See if handlers or finally is present
            if (
                any(
                    self._get_name(handler.type) == "GeneratorExit"
                    for handler in n.handlers
                    if handler.type is not None
                )
                or n.finalbody
            ):
                continue

            # this Try block doesn't properly handle GeneratorExit, add warning
            self.add_message(
                "contextmanager-generator-missing-cleanup",
                node=node,
                args=(node.end_lineno,),
            )
            return

        # if there are yield nodes in function and nodes that could be cleanup after it
        # add the warning
        # if the last statement is the yield, there is no cleanup to be done
        if yield_nodes and not self._check_node_has_yield(node.body[-1]):
            self.add_message(
                "contextmanager-generator-missing-cleanup",
                node=node,
                args=(node.end_lineno,),
            )

    @staticmethod
    def _check_node_has_yield(node: nodes.NodeNG) -> bool:
        """Return whether a given node has a Yield node in it.

        :param node: Node to check
        :type node: nodes.NodeNG
        :return: True if Yield contained, False otherwise
        :rtype: bool
        """
        return any(node.nodes_of_class(nodes.Yield))

    @staticmethod
    def _get_name(node: nodes.NodeNG) -> str:
        """Helper function to get the name from a node.

        Helpful when possible to have a Name or Attribute node.

        :param node: Node to get name of
        :type node: nodes.NodeNG
        :return: string name
        :rtype: str
        """
        if isinstance(node, nodes.Name):
            return node.name  # type: ignore[no-any-return]
        if isinstance(node, nodes.Attribute):
            return node.attrname  # type: ignore[no-any-return]
        return node.as_string()  # type: ignore[no-any-return]
