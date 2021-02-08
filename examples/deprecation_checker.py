"""
Example checker detecting deprecated functions/methods. Following example searches for usages of
deprecated function `deprecated_function` and deprecated method `MyClass.deprecated_method`
from module mymodule:

.. code-block:: console
    $ cat mymodule.py
    def deprecated_function():
        pass

    class MyClass:
        def deprecated_method(self):
            pass

    $ cat mymain.py
    from mymodule import deprecated_function, MyClass

    deprecated_function()
    MyClass().deprecated_method()

    $ pylint --load-plugins=deprecation_checker mymain.py
    ************* Module mymain
    mymain.py:3:0: W1505: Using deprecated method deprecated_function() (deprecated-method)
    mymain.py:4:0: W1505: Using deprecated method deprecated_method() (deprecated-method)

    ------------------------------------------------------------------
    Your code has been rated at 3.33/10 (previous run: 3.33/10, +0.00)
"""

import astroid

from pylint.checkers import BaseChecker, DeprecatedMixin, utils
from pylint.interfaces import IAstroidChecker


class DeprecationChecker(BaseChecker, DeprecatedMixin):
    """Class implementing deprecation checker."""

    __implements__ = (IAstroidChecker,)
    # The name defines a custom section of the config for this checker.
    name = "deprecated"
    # This class variable declares the messages (ie the warnings and errors)
    # that the checker can emit.
    msgs = {
        # Each message has a code, a message that the user will see,
        # a unique symbol that identifies the message,
        # and a detailed help message
        # that will be included in the documentation.
        "W1505": (
            "Using deprecated method %s()",
            "deprecated-method",
            "The method is marked as deprecated and will be removed in the future.",
        ),
    }

    @utils.check_messages(
        "deprecated-method",
    )
    def visit_call(self, node):
        """Called when a :class:`.astroid.node_classes.Call` node is visited.

        See :mod:`astroid` for the description of available nodes.

        :param node: The node to check.
        :type node: astroid.node_classes.Call
        """
        try:
            for inferred in node.func.infer():
                # Calling entry point for deprecation check logic.
                self.check_deprecated_method(node, inferred)
        except astroid.InferenceError:
            return

    def deprecated_methods(self):
        """Callback method called by DeprecatedMixin for every method/function found in the code.

        Returns:
            collections.abc.Container of deprecated function/method names.
        """
        return {"mymodule.deprecated_function", "mymodule.MyClass.deprecated_method"}


def register(linter):
    """This required method auto registers the checker.

    :param linter: The linter to register the checker to.
    :type linter: pylint.lint.PyLinter
    """
    linter.register_checker(DeprecationChecker(linter))
