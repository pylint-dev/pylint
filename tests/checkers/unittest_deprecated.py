from typing import List, Optional, Set, Tuple, Union

import astroid

from pylint.checkers import BaseChecker, DeprecatedMixin
from pylint.interfaces import UNDEFINED, IAstroidChecker
from pylint.testutils import CheckerTestCase, MessageTest


class _DeprecatedChecker(DeprecatedMixin, BaseChecker):
    __implements__ = (IAstroidChecker,)
    name = "deprecated"

    def deprecated_methods(self) -> Set[str]:
        return {"deprecated_func", ".Deprecated.deprecated_method"}

    def deprecated_modules(self) -> Set[str]:
        return {"deprecated_module"}

    def deprecated_classes(self, module: str) -> List[str]:
        return ["DeprecatedClass"] if module == "deprecated" else []

    def deprecated_arguments(
        self, method: str
    ) -> Union[
        Tuple[Tuple[Optional[int], str], ...], Tuple[Tuple[int, str], Tuple[int, str]]
    ]:
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
        if method == ".MyClass":
            # def __init__(self, deprecated_arg=None)
            return ((0, "deprecated_arg"),)
        return ()

    def deprecated_decorators(self) -> Set[str]:
        return {".deprecated_decorator"}


class TestDeprecatedChecker(CheckerTestCase):
    CHECKER_CLASS = _DeprecatedChecker

    def test_deprecated_function(self) -> None:
        # Tests detecting deprecated function
        node = astroid.extract_node(
            """
        def deprecated_func():
            pass

        deprecated_func()
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="deprecated-method",
                args=("deprecated_func",),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_deprecated_method(self) -> None:
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
            MessageTest(
                msg_id="deprecated-method",
                args=("deprecated_method",),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_deprecated_method_alias(self) -> None:
        # Tests detecting deprecated method defined as alias
        # to existing method
        node = astroid.extract_node(
            """
        class Deprecated:
            def _deprecated_method(self):
                pass

            deprecated_method = _deprecated_method

        d = Deprecated()
        d.deprecated_method()
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="deprecated-method",
                args=("deprecated_method",),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_no_message(self) -> None:
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

    def test_function_deprecated_arg(self) -> None:
        # Tests raising error when calling function with deprecated argument
        node = astroid.extract_node(
            """
        def myfunction1(arg1, deprecated_arg1='spam'):
            pass

        myfunction1(None, 'deprecated')
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "myfunction1"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_function_deprecated_kwarg(self) -> None:
        # Tests raising error when calling function with deprecated keyword argument
        node = astroid.extract_node(
            """
        def myfunction1(arg1, deprecated_arg1='spam'):
            pass

        myfunction1(None, deprecated_arg1='deprecated')
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "myfunction1"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_function_deprecated_not_used(self) -> None:
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

    def test_function_deprecated_kwarg_only(self) -> None:
        # Tests raising error when calling function with deprecated keyword only argument
        node = astroid.extract_node(
            """
        def myfunction3(arg1, *, deprecated_arg1='spam'):
            pass

        myfunction3(None, deprecated_arg1='deprecated')
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "myfunction3"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_method_deprecated_arg(self) -> None:
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
            MessageTest(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "mymethod1"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_method_deprecated_kwarg(self) -> None:
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
            MessageTest(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "mymethod1"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_method_deprecated_not_used(self) -> None:
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

    def test_method_deprecated_kwarg_only(self) -> None:
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
            MessageTest(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "mymethod3"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_function_deprecated_arg_kwargs(self) -> None:
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
            MessageTest(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "myfunction2"),
                node=node,
                confidence=UNDEFINED,
            ),
            MessageTest(
                msg_id="deprecated-argument",
                args=("deprecated_arg2", "myfunction2"),
                node=node,
                confidence=UNDEFINED,
            ),
        ):
            self.checker.visit_call(node)

    def test_function_deprecated_kwarg_kwarg(self) -> None:
        # Tests raising error when calling function with deprecated keyword arguments
        node = astroid.extract_node(
            """
        def myfunction2(arg1, deprecated_arg1, arg2='foo', deprecated_arg2='spam'):
            pass

        myfunction2(None, deprecated_arg1='deprecated', deprecated_arg2='deprecated')
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "myfunction2"),
                node=node,
                confidence=UNDEFINED,
            ),
            MessageTest(
                msg_id="deprecated-argument",
                args=("deprecated_arg2", "myfunction2"),
                node=node,
                confidence=UNDEFINED,
            ),
        ):
            self.checker.visit_call(node)

    def test_method_deprecated_arg_kwargs(self) -> None:
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
            MessageTest(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "mymethod2"),
                node=node,
                confidence=UNDEFINED,
            ),
            MessageTest(
                msg_id="deprecated-argument",
                args=("deprecated_arg2", "mymethod2"),
                node=node,
                confidence=UNDEFINED,
            ),
        ):
            self.checker.visit_call(node)

    def test_method_deprecated_kwarg_kwarg(self) -> None:
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
            MessageTest(
                msg_id="deprecated-argument",
                args=("deprecated_arg1", "mymethod2"),
                node=node,
                confidence=UNDEFINED,
            ),
            MessageTest(
                msg_id="deprecated-argument",
                args=("deprecated_arg2", "mymethod2"),
                node=node,
                confidence=UNDEFINED,
            ),
        ):
            self.checker.visit_call(node)

    def test_class_deprecated_arguments(self) -> None:

        node = astroid.extract_node(
            """
        class MyClass:
            def __init__(self, deprecated_arg=None):
                pass

        MyClass(5)
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="deprecated-argument",
                args=("deprecated_arg", "MyClass"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_deprecated_module(self) -> None:
        # Tests detecting deprecated module
        node = astroid.extract_node(
            """
        import deprecated_module
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="deprecated-module",
                args="deprecated_module",
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_import(node)

    def test_deprecated_module_from(self) -> None:
        # Tests detecting deprecated module
        node = astroid.extract_node(
            """
        from deprecated_module import myfunction
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="deprecated-module",
                args="deprecated_module",
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_importfrom(node)

    def test_deprecated_class_import_from(self) -> None:
        # Tests detecting deprecated class via import from
        node = astroid.extract_node(
            """
        from deprecated import DeprecatedClass
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="deprecated-class",
                args=("DeprecatedClass", "deprecated"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_importfrom(node)

    def test_deprecated_class_import(self) -> None:
        # Tests detecting deprecated class via import
        node = astroid.extract_node(
            """
        import deprecated.DeprecatedClass
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="deprecated-class",
                args=("DeprecatedClass", "deprecated"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_import(node)

    def test_deprecated_class_call(self) -> None:
        # Tests detecting deprecated class via call
        node = astroid.extract_node(
            """
        import deprecated
        deprecated.DeprecatedClass()
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="deprecated-class",
                args=("DeprecatedClass", "deprecated"),
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    def test_deprecated_decorator(self) -> None:
        # Tests detecting deprecated decorator
        node = astroid.extract_node(
            """
        def deprecated_decorator(f):
            def wrapper():
                return f()
            return wrapper

        @deprecated_decorator #@
        def function():
            pass
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="deprecated-decorator",
                args=".deprecated_decorator",
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_decorators(node)

    def test_deprecated_decorator_with_arguments(self) -> None:
        # Tests detecting deprecated decorator with arguments
        node = astroid.extract_node(
            """
        def deprecated_decorator(arg1, arg2):
            def wrapper(f):
                def wrapped():
                    return f()
                return wrapped
            return wrapper

        @deprecated_decorator(2, 3) #@
        def function():
            pass
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="deprecated-decorator",
                args=".deprecated_decorator",
                node=node,
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_decorators(node)
