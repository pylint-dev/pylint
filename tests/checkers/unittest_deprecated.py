import astroid

from pylint.checkers import BaseChecker, DeprecatedMixin
from pylint.interfaces import UNDEFINED, IAstroidChecker
from pylint.testutils import CheckerTestCase, Message


class _DeprecatedChecker(DeprecatedMixin, BaseChecker):
    __implements__ = (IAstroidChecker,)
    name = "deprecated"

    def deprecated_methods(self):
        return {"deprecated_func", ".Deprecated.deprecated_method"}

    def deprecated_modules(self):
        return {"deprecated_module"}

    def deprecated_arguments(self, method):
        if method == "myfunction1":
            # def myfunction1(arg1, deprecated_arg1='spam')
            return ((1, "deprecated_arg1"),)
        if method == "myfunction2":
            # def myfunction2(arg1, deprecated_arg1, arg2='foo', deprecated_arg2='spam'))
            return ((1, "deprecated_arg1"), (3, "deprecated_arg2"))
        if method == "myfunction3":
            # def myfunction1(arg1, *, deprecated_arg1='spam')
            return ((None, "deprecated_arg1"),)
        if method == ".MyClass.mymethod1":
            # def mymethod1(self, arg1, deprecated_arg1=None)
            return ((1, "deprecated_arg1"),)
        if method == ".MyClass.mymethod2":
            # def mymethod2(self, arg1, deprecated_arg1='bar', arg2='foo', deprecated_arg2='spam'))
            return ((1, "deprecated_arg1"), (3, "deprecated_arg2"))
        if method == ".MyClass.mymethod3":
            # def mymethod1(self, arg1, *, deprecated_arg1=None)
            return ((None, "deprecated_arg1"),)
        return ()


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

    def test_function_deprecated_arg(self):
        # Tests raising error when calling function with deprecated argument
        node = astroid.extract_node(
            """
        def myfunction1(arg1, deprecated_arg1='spam'):
            pass

        myfunction1(None, 'deprecated')
        """
        )
        with self.assertAddsMessages(
            Message(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "myfunction1"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_function_deprecated_kwarg(self):
        # Tests raising error when calling function with deprecated keyword argument
        node = astroid.extract_node(
            """
        def myfunction1(arg1, deprecated_arg1='spam'):
            pass

        myfunction1(None, deprecated_arg1='deprecated')
        """
        )
        with self.assertAddsMessages(
            Message(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "myfunction1"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_function_deprecated_not_used(self):
        # Tests raising error when calling function without deprecated argument
        node = astroid.extract_node(
            """
        def myfunction1(arg1, deprecated_arg1='spam'):
            pass

        myfunction1(None)
        """
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_function_deprecated_kwarg_only(self):
        # Tests raising error when calling function with deprecated keyword only argument
        node = astroid.extract_node(
            """
        def myfunction3(arg1, *, deprecated_arg1='spam'):
            pass

        myfunction3(None, deprecated_arg1='deprecated')
        """
        )
        with self.assertAddsMessages(
            Message(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "myfunction3"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_method_deprecated_arg(self):
        # Tests raising error when calling method with deprecated argument
        node = astroid.extract_node(
            """
        class MyClass:
            def mymethod1(self, arg1, deprecated_arg1):
                pass

        MyClass().mymethod1(None, 'deprecated')
        """
        )
        with self.assertAddsMessages(
            Message(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "mymethod1"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_method_deprecated_kwarg(self):
        # Tests raising error when calling method with deprecated keyword argument
        node = astroid.extract_node(
            """
        class MyClass:
            def mymethod1(self, arg1, deprecated_arg1):
                pass

        MyClass().mymethod1(None, deprecated_arg1='deprecated')
        """
        )
        with self.assertAddsMessages(
            Message(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "mymethod1"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_method_deprecated_not_used(self):
        # Tests raising error when calling method without deprecated argument
        node = astroid.extract_node(
            """
        class MyClass:
            def mymethod1(self, arg1, deprecated_arg1):
                pass

        MyClass().mymethod1(None)
        """
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_method_deprecated_kwarg_only(self):
        # Tests raising error when calling method with deprecated keyword only argument
        node = astroid.extract_node(
            """
        class MyClass:
            def mymethod3(self, arg1, *, deprecated_arg1):
                pass

        MyClass().mymethod3(None, deprecated_arg1='deprecated')
        """
        )
        with self.assertAddsMessages(
            Message(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "mymethod3"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_function_deprecated_arg_kwargs(self):
        # Tests raising error when calling function with deprecated argument
        # and keyword argument
        node = astroid.extract_node(
            """
        def myfunction2(arg1, deprecated_arg1, arg2='foo', deprecated_arg2='spam'):
            pass

        myfunction2(None, 'deprecated', deprecated_arg2='deprecated')
        """
        )
        with self.assertAddsMessages(
            Message(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "myfunction2"),
                node=node,
                confidence=UNDEFINED,
            ),
            Message(
                msg_id="deprecated-argument",
                args=("deprecated_arg2", "myfunction2"),
                node=node,
                confidence=UNDEFINED,
            ),
        ):
            self.checker.visit_call(node)

    def test_function_deprecated_kwarg_kwarg(self):
        # Tests raising error when calling function with deprecated keyword arguments
        node = astroid.extract_node(
            """
        def myfunction2(arg1, deprecated_arg1, arg2='foo', deprecated_arg2='spam'):
            pass

        myfunction2(None, deprecated_arg1='deprecated', deprecated_arg2='deprecated')
        """
        )
        with self.assertAddsMessages(
            Message(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "myfunction2"),
                node=node,
                confidence=UNDEFINED,
            ),
            Message(
                msg_id="deprecated-argument",
                args=("deprecated_arg2", "myfunction2"),
                node=node,
                confidence=UNDEFINED,
            ),
        ):
            self.checker.visit_call(node)

    def test_method_deprecated_arg_kwargs(self):
        # Tests raising error when calling method with deprecated argument
        # and keyword argument
        node = astroid.extract_node(
            """
        class MyClass:
            def mymethod2(self, arg1, deprecated_arg1, arg2='foo', deprecated_arg2='spam'):
                pass

        MyClass().mymethod2(None, 'deprecated', deprecated_arg2='deprecated')
        """
        )
        with self.assertAddsMessages(
            Message(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "mymethod2"),
                node=node,
                confidence=UNDEFINED,
            ),
            Message(
                msg_id="deprecated-argument",
                args=("deprecated_arg2", "mymethod2"),
                node=node,
                confidence=UNDEFINED,
            ),
        ):
            self.checker.visit_call(node)

    def test_method_deprecated_kwarg_kwarg(self):
        # Tests raising error when calling method with deprecated keyword arguments
        node = astroid.extract_node(
            """
        class MyClass:
            def mymethod2(self, arg1, deprecated_arg1, arg2='foo', deprecated_arg2='spam'):
                pass

        MyClass().mymethod2(None, deprecated_arg1='deprecated', deprecated_arg2='deprecated')
        """
        )
        with self.assertAddsMessages(
            Message(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "mymethod2"),
                node=node,
                confidence=UNDEFINED,
            ),
            Message(
                msg_id="deprecated-argument",
                args=("deprecated_arg2", "mymethod2"),
                node=node,
                confidence=UNDEFINED,
            ),
        ):
            self.checker.visit_call(node)

    def test_deprecated_module(self):
        # Tests detecting deprecated module
        node = astroid.extract_node(
            """
        import deprecated_module
        """
        )
        with self.assertAddsMessages(
            Message(
                msg_id="deprecated-module",
                args="deprecated_module",
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_import(node)

    def test_deprecated_module_from(self):
        # Tests detecting deprecated module
        node = astroid.extract_node(
            """
        from deprecated_module import myfunction
        """
        )
        with self.assertAddsMessages(
            Message(
                msg_id="deprecated-module",
                args="deprecated_module",
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_importfrom(node)
