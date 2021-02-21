# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Checker mixin for deprecated functionality."""

from itertools import chain
from typing import Any

import astroid

from pylint.checkers import utils

ACCEPTABLE_NODES = (
    astroid.BoundMethod,
    astroid.UnboundMethod,
    astroid.FunctionDef,
)


class DeprecatedMixin:
    """A mixin implementing logic for checking deprecated symbols.
    A class implementing mixin must define "deprecated-method" Message.
    """

    msgs: Any = {
        "W1505": (
            "Using deprecated method %s()",
            "deprecated-method",
            "The method is marked as deprecated and will be removed in the future.",
        ),
        "W1511": (
            "Using deprecated argument %s of method %s()",
            "deprecated-argument",
            "The argument is marked as deprecated and will be removed in the future.",
        ),
    }

    @utils.check_messages(
        "deprecated-method",
        "deprecated-argument",
    )
    def visit_call(self, node):
        """Called when a :class:`.astroid.node_classes.Call` node is visited.

        Args:
            node (astroid.node_classes.Call): The node to check.
        """
        try:
            for inferred in node.func.infer():
                # Calling entry point for deprecation check logic.
                self.check_deprecated_method(node, inferred)
        except astroid.InferenceError:
            return

    def deprecated_methods(self):
        """Callback returning the deprecated methods/functions.

        Returns:
            collections.abc.Container of deprecated function/method names.
        """
        # pylint: disable=no-self-use
        return ()

    def deprecated_arguments(self, method: str):
        """Callback returning the deprecated arguments of method/function.

        Args:
            method (str): name of function/method checked for deprecated arguments

        Returns:
            collections.abc.Iterable in form:
                ((POSITION1, PARAM1), (POSITION2: PARAM2) ...)
            where
                * POSITIONX - position of deprecated argument PARAMX in function definition.
                  If argument is keyword-only, POSITIONX should be None.
                * PARAMX - name of the deprecated argument.
            E.g. suppose function:

            .. code-block:: python
                def bar(arg1, arg2, arg3, arg4, arg5='spam')

            with deprecated arguments `arg2` and `arg4`. `deprecated_arguments` should return:

            .. code-block:: python
                ((1, 'arg2'), (3, 'arg4'))
        """
        # pylint: disable=no-self-use
        # pylint: disable=unused-argument
        return ()

    def check_deprecated_method(self, node, inferred):
        """Executes the checker for the given node. This method should
        be called from the checker implementing this mixin.
        """

        # Reject nodes which aren't of interest to us.
        if not isinstance(inferred, ACCEPTABLE_NODES):
            return

        if isinstance(node.func, astroid.Attribute):
            func_name = node.func.attrname
        elif isinstance(node.func, astroid.Name):
            func_name = node.func.name
        else:
            # Not interested in other nodes.
            return

        qname = inferred.qname()
        if any(name in self.deprecated_methods() for name in (qname, func_name)):
            self.add_message("deprecated-method", node=node, args=(func_name,))
        num_of_args = len(node.args)
        kwargs = {kw.arg for kw in node.keywords} if node.keywords else {}
        for position, arg_name in chain(
            self.deprecated_arguments(func_name), self.deprecated_arguments(qname)
        ):
            if arg_name in kwargs:
                # function was called with deprecated argument as keyword argument
                self.add_message(
                    "deprecated-argument", node=node, args=(arg_name, func_name)
                )
            elif position is not None and position < num_of_args:
                # function was called with deprecated argument as positional argument
                self.add_message(
                    "deprecated-argument", node=node, args=(arg_name, func_name)
                )
