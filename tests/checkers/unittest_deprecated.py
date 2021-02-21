import astroid

from pylint.checkers import BaseChecker, DeprecatedMixin, utils
from pylint.interfaces import UNDEFINED, IAstroidChecker
from pylint.testutils import CheckerTestCase, Message


class _DeprecatedChecker(DeprecatedMixin, BaseChecker):
    __implements__ = (IAstroidChecker,)
    name = "deprecated"

    msgs = {
        "W1505": (
            "Using deprecated method %s()",
            "deprecated-method",
            "The method is marked as deprecated and will be removed in "
            "a future version of Python. Consider looking for an "
            "alternative in the documentation.",
        )
    }

    @utils.check_messages(
        "deprecated-method",
    )
    def visit_call(self, node):
        """Visit a Call node."""
        try:
            for inferred in node.func.infer():
                self.check_deprecated_method(node, inferred)
        except astroid.InferenceError:
            return

    def deprecated_methods(self):
        return {"deprecated_func", ".Deprecated.deprecated_method"}


class TestDeprecatedChecker(CheckerTestCase):
    CHECKER_CLASS = _DeprecatedChecker

    def test_deprecated_function(self):
        # Tests detecting deprecated function
        node = astroid.extract_node(
            """
        def deprecated_func():
            pass

        deprecated_func()
        """
        )
        with self.assertAddsMessages(
            Message(
                msg_id="deprecated-method",
                args=("deprecated_func",),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_deprecated_method(self):
        # Tests detecting deprecated method
        node = astroid.extract_node(
            """
        class Deprecated:
            def deprecated_method():
                pass

        d = Deprecated()
        d.deprecated_method()
        """
        )
        with self.assertAddsMessages(
            Message(
                msg_id="deprecated-method",
                args=("deprecated_method",),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_no_message(self):
        # Tests not raising error when no deprecated functions/methods are present.
        node = astroid.extract_node(
            """
        class MyClass:
            def mymethod():
                pass

        MyClass().mymethod()

        def myfunc():
            pass

        myfunc()
        """
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)
