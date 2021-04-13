# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""Checker mixin for deprecated functionality."""
from itertools import chain
from typing import Any, Container, Iterable, Tuple, Union

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
        "W0402": (
            "Uses of a deprecated module %r",
            "deprecated-module",
            "A module marked as deprecated is imported.",
        ),
    }

    @utils.check_messages(
        "deprecated-method",
        "deprecated-argument",
    )
    def visit_call(self, node: astroid.Call) -> None:
        """Called when a :class:`.astroid.node_classes.Call` node is visited."""
        try:
            for inferred in node.func.infer():
                # Calling entry point for deprecation check logic.
                self.check_deprecated_method(node, inferred)
        except astroid.InferenceError:
            pass

    @utils.check_messages("deprecated-module")
    def visit_import(self, node):
        """triggered when an import statement is seen"""
        for name in (name for name, _ in node.names):
            self.check_deprecated_module(node, name)

    @utils.check_messages("deprecated-module")
    def visit_importfrom(self, node):
        """triggered when a from statement is seen"""
        basename = node.modname
        self.check_deprecated_module(node, basename)

    def deprecated_methods(self) -> Container[str]:
        """Callback returning the deprecated methods/functions.

        Returns:
            collections.abc.Container of deprecated function/method names.
        """
        # pylint: disable=no-self-use
        return ()

    def deprecated_arguments(
        self, method: str
    ) -> Iterable[Tuple[Union[int, None], str]]:
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

    def deprecated_modules(self) -> Iterable:
        """Callback returning the deprecated modules.

        Returns:
            collections.abc.Container of deprecated module names.
        """
        # pylint: disable=no-self-use
        return ()

    def check_deprecated_module(self, node, mod_path):
        """Checks if the module is deprecated"""

        for mod_name in self.deprecated_modules():
            if mod_path == mod_name or mod_path.startswith(mod_name + "."):
                self.add_message("deprecated-module", node=node, args=mod_path)

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
            return
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
