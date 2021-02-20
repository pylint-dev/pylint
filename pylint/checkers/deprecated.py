# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Checker mixin for deprecated functionality."""

import abc
from typing import Any

import astroid

ACCEPTABLE_NODES = (
    astroid.BoundMethod,
    astroid.UnboundMethod,
    astroid.FunctionDef,
)


class DeprecatedMixin(metaclass=abc.ABCMeta):
    """A mixin implementing logic for checking deprecated symbols.
    A class imlementing mixin must define "deprecated-method" Message.
    """

    msgs: Any = {
        "W1505": (
            "Using deprecated method %s()",
            "deprecated-method",
            "The method is marked as deprecated and will be removed in the future.",
        ),
    }

    @abc.abstractmethod
    def deprecated_methods(self):
        """Callback returning the deprecated methods/functions.

        Returns:
            collections.abc.Container of deprecated function/method names.
        """

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
