from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter

# Checkers should always inherit from `BaseChecker`.


class MyAstroidChecker(BaseChecker):
    """Add class member attributes to the class local's dictionary."""

    # The name defines a custom section of the config for this checker.
    name = "custom"
    # This class variable declares the messages (i.e. the warnings and errors)
    # that the checker can emit.
    msgs = {
        # Each message has a code, a message that the user will see,
        # a unique symbol that identifies the message,
        # and a detailed help message
        # that will be included in the documentation.
        "W0001": ("Message that will be emitted", "message-symbol", "Message help")
    }
    # This class variable declares the options
    # that are configurable by the user.
    options = (
        # Each option definition has a name which is used on the command line
        # and in config files, and a dictionary of arguments
        # (similar to argparse.ArgumentParser.add_argument).
        (
            "store-locals-indicator",
            {
                "default": "properties",
                "help": (
                    "The expression name that indicates that the locals should "
                    "be stored"
                ),
            },
        ),
    )

    def visit_call(self, node: nodes.Call) -> None:
        """Called when a :class:`.nodes.Call` node is visited.

        See :mod:`astroid` for the description of available nodes.
        """
        if not (
            isinstance(node.func, nodes.Attribute)
            and isinstance(node.func.expr, nodes.Name)
            and node.func.expr.name == self.linter.config.store_locals_indicator
            and node.func.attrname == "create"
        ):
            return
        in_class = node.frame()
        for param in node.args:
            in_class.locals[param.name] = node


def register(linter: PyLinter) -> None:
    """This required method auto registers the checker during initialization.

    :param linter: The linter to register the checker to.
    """
    linter.register_checker(MyAstroidChecker(linter))
