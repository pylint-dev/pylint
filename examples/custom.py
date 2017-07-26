import astroid

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker


# This is our checker class.
# Checkers should always inherit from `BaseChecker`.
class MyAstroidChecker(BaseChecker):
    """Add class member attributes to the class locals dictionary."""

    # This class variable defines the type of checker that we are implementing.
    # In this case, we are implementing an AST checker.
    __implements__ = IAstroidChecker

    # The name defines a custom section of the config for this checker.
    name = 'custom'
    # The priority indicates the order that pylint will run the checkers.
    priority = -1
    # This class variable declares the messages (ie the warnings and errors)
    # that the checker can emit.
    msgs = {
        # Each message has a code, a message that the user will see,
        # a unique symbol that identifies the message,
        # and a detailed help message
        # that will be included in the documentation.
        'W0001': ('Message that will be emitted',
                  'message-symbol',
                  'Message help')
    }
    # This class variable declares the options
    # that are configurable by the user.
    options = (
        # Each option definition has a name which is used on the command line
        # and in config files, and a dictionary of arguments
        # (similar to those to those to
        # argparse.ArgumentParser.add_argument).
        ('store-locals-indicator',
         {'default': 'properties',
          'help': ('The expression name that indicates that the locals should '
                   'be stored'),
          },
         ),
    )

    def visit_call(self, node):
        """Called when a :class:`.astroid.node_classes.Call` node is visited.

        See :mod:`astroid` for the description of available nodes.

        :param node: The node to check.
        :type node: astroid.node_classes.Call
        """
        if not (isinstance(node.func, astroid.Attribute)
                and isinstance(node.func.expr, astroid.Name)
                and node.func.expr.name == self.config.store_locals_indicator
                and node.func.attrname == 'create'):
            return
        in_class = node.frame()
        for param in node.args:
            in_class.locals[param.name] = node


def register(linter):
    """This required method auto registers the checker.

    :param linter: The linter to register the checker to.
    :type linter: pylint.lint.PyLinter
    """
    linter.register_checker(MyAstroidChecker(linter))
