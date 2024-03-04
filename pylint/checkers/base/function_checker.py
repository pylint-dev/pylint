# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Function checker for Python code."""
# pylint: disable=wrong-spelling-in-comment

from __future__ import annotations

from itertools import chain

from astroid import nodes

from pylint.checkers import utils
from pylint.checkers.base.basic_checker import _BasicChecker
from pylint.lint.pylinter import PyLinter


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

    def __init__(self, linter: PyLinter) -> None:
        """Initialize the checker and container to store context-managers."""
        super().__init__(linter)
        # as this walks FunctionDef nodes, if it is wrapped in a contextmanager
        # add it here for checking in generator functions
        # if encounter generator FunctionDef, then check if it uses a contextmanager and conditionally add here
        # TODO: should this string be function name or module import name (foo v mod.bar.foo)
        self._contextmanagers: set[str] = set()
        # as this walks FunctionDef nodes, if it is a generator that uses a With/AsyncWith node
        # add it here for checking against contextmanager, in case order of visiting is reversed
        # key is the contextmanager string name, value is the generator FunctionDef node to be used in the message
        self._generator_with_contextmanager: dict[str, nodes.FunctionDef] = {}

    def _add_node_to_contextmanagers(self, node: nodes.FunctionDef) -> None:
        """Add a node to the internal contextmanager set.

        Checks if the node was previously added and if so, adds a message.

        :param node: FunctionDef node to add
        :type node: nodes.FunctionDef
        """
        simple_name = node.name
        if simple_name not in self._contextmanagers:
            self._contextmanagers.add(simple_name)
        else:
            err_node = self._generator_with_contextmanager[simple_name]
            self.add_message(
                "contextmanager-generator-missing-cleanup",
                node=err_node,
                args=(err_node.lineno,),
            )

    def _add_node_to_generators(
        self, with_node: nodes.With | nodes.AsyncWith, node: nodes.FunctionDef
    ) -> None:
        """Adds node to the internal generator set.

        If the used contextmanager for this generator has already been added, add a message.

        :param with_node: The With or AsyncWith node to add that the generator function uses
        :type with_node: nodes.With | nodes.AsyncWith
        :param node: The function node to possible add messages about
        :type node: nodes.FunctionDef
        """
        # with statements can have multiple items, so we will just add all for now
        # TODO: clean up this logic, probably have to change the input params to be the contextManager call
        for item in with_node.items:
            used_contextmanager = item[0]
            contextmgr_name = self._get_name(used_contextmanager)
            if contextmgr_name in self._contextmanagers:
                self.add_message(
                    "contextmanager-generator-missing-cleanup",
                    node=node,
                    args=(node.lineno,),
                )
            else:
                self._generator_with_contextmanager[contextmgr_name] = node
                self._contextmanagers.add(contextmgr_name)

    @utils.only_required_for_messages("contextmanager-generator-missing-cleanup")
    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        self._check_contextmanager_generator_missing_cleanup(node)

    @utils.only_required_for_messages("contextmanager-generator-missing-cleanup")
    def visit_asyncfunctiondef(self, node: nodes.AsyncFunctionDef) -> None:
        self._check_contextmanager_generator_missing_cleanup(node)

    def _check_contextmanager_generator_missing_cleanup(
        self, node: nodes.FunctionDef
    ) -> None:
        """Check a FunctionDef to find context-managers and generators used in a no
        cleanup pattern.

        :param node: FunctionDef node to check
        :type node: nodes.FunctionDef
        """
        # if function does not use a Yield statement, it cant be a generator or a contextmanager
        # TODO: should this also capture YieldFrom?
        yield_nodes = list(node.nodes_of_class(nodes.Yield))
        if not yield_nodes:
            return

        # check if function has a contextmanager decorator
        contextmanager_str = "contextlib.contextmanager"
        should_be_added_to_contextmanagers = any(
            decorator
            # this is fully qualified import name
            for decorator in node.decoratornames()
            if decorator == contextmanager_str
        )
        # cant be a contextmanager and a erroring generator at the same time
        if (
            should_be_added_to_contextmanagers
            and self._node_fails_contextmanager_cleanup(node, yield_nodes=yield_nodes)
        ):
            self._add_node_to_contextmanagers(node)
            return

        # otherwise could be a generator that uses a contextmanager
        with_nodes = list(node.nodes_of_class(nodes.With))
        async_with_nodes = list(node.nodes_of_class(nodes.AsyncWith))
        if not with_nodes and not async_with_nodes:
            # no inner contextmanager, so no need to check
            return
        all_nodes = chain(with_nodes, async_with_nodes)
        for with_node in all_nodes:
            if self._node_fails_generator_checks(with_node):
                self._add_node_to_generators(with_node, node)

    @staticmethod
    def _node_fails_contextmanager_cleanup(
        node: nodes.FunctionDef, yield_nodes: list[nodes.Yield]
    ) -> bool:
        """Check if a node fails contextmanager cleanup.

        Current checks for a contextmanager:
            - only if the context manager yields something other than None
            - only if the context manager lacks a finally, or does not catch GeneratorExit

        :param node: Node to check
        :type node: nodes.FunctionDef
        :return: True if fails, False otherwise
        :param yield_nodes: List of Yield nodes in the function body
        :type yield_nodes: list[nodes.Yield]
        :rtype: bool
        """
        # if context manager yields a non-constant value, then continue checking
        if any(
            yield_node.value is None or isinstance(yield_node.value, nodes.Const)
            for yield_node in yield_nodes
        ):
            return False
        # if function body has multiple Try, filter down to the ones that have a yield node
        try_with_yield_nodes = [
            try_node
            for try_node in node.nodes_of_class(nodes.Try)
            if any(
                try_body_node.value in yield_nodes for try_body_node in try_node.body
            )
        ]
        if not try_with_yield_nodes:
            # no try blocks at all, so checks after this line do not apply
            return True
        # if the contextmanager has a finally block, then it is fine
        if all(try_node.finalbody for try_node in try_with_yield_nodes):
            return False
        # if the contextmanager catches GeneratorExit, then it is fine
        if all(
            any(
                isinstance(handler.type, nodes.Name)
                and handler.type.name == "GeneratorExit"
                for handler in try_node.handlers
            )
            for try_node in try_with_yield_nodes
        ):
            return False
        return True

    @staticmethod
    def _node_fails_generator_checks(node: nodes.With | nodes.AsyncWith) -> bool:
        """Check if a node fails generator checks.

        Current checks for generator functions:
            - only if a with/async with statement is used
            - only if the val in `with cm() as val` is not discarded, e.g. not for uses like with cm():

        :param node: Node to check
        :type node: nodes.With | nodes.AsyncWith
        :return: True if fails, False otherwise
        :rtype: bool
        """
        # if the with/async with statement discards the value, then return False
        if all(item[1] is None for item in node.items):
            return False

        return True

    @staticmethod
    def _get_name(node: nodes.NodeNG) -> str:
        """Helper function to get the final name component of a node.

        Helpful when possible to have a Name or Attribute node.
        If Attribute, returns the attrname, otherwise returns the name.

        :param node: Node to get name of
        :type node: nodes.NodeNG
        :return: string name
        :rtype: str
        """
        if isinstance(node, nodes.Name):
            return node.name  # type: ignore[no-any-return]
        if isinstance(node, nodes.Attribute):
            return node.attrname  # type: ignore[no-any-return]
        if isinstance(node, nodes.Call):
            return node.func.repr_name()  # type: ignore[no-any-return]
        return node.as_string()  # type: ignore[no-any-return]
