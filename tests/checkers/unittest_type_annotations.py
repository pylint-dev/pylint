# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the type_annotations checker."""

from __future__ import annotations

import astroid

from pylint.checkers.type_annotations import TypeAnnotationChecker
from pylint.testutils import CheckerTestCase, MessageTest


class TestTypeAnnotationChecker(CheckerTestCase):
    """Tests for TypeAnnotationChecker."""

    CHECKER_CLASS = TypeAnnotationChecker

    def test_missing_return_type_annotation(self) -> None:
        """Test detection of missing return type annotation."""
        node = astroid.extract_node(
            """
        def foo(x):  #@
            return x
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-return-type-annotation",
                args=("foo",),
                node=node,
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=7,
            ),
            MessageTest(
                msg_id="missing-param-type-annotation",
                args=("x", "foo"),
                node=node,
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=7,
            ),
        ):
            self.checker.visit_functiondef(node)

    def test_function_with_return_type_annotation(self) -> None:
        """Test that functions with return type annotations don't trigger warnings."""
        node = astroid.extract_node(
            """
        def foo(x: int) -> int:  #@
            return x
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_init_method_skipped(self) -> None:
        """Test that __init__ methods are skipped for return type."""
        node = astroid.extract_node(
            """
        class MyClass:
            def __init__(self, x):  #@
                self.x = x
        """
        )
        # __init__ should skip return type check, but still check params
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-param-type-annotation",
                args=("x", "__init__"),
                node=node,
                line=3,
                col_offset=4,
                end_line=3,
                end_col_offset=16,
            )
        ):
            self.checker.visit_functiondef(node)

    def test_async_function_missing_return_type(self) -> None:
        """Test detection in async functions."""
        node = astroid.extract_node(
            """
        async def foo(x):  #@
            return x
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-return-type-annotation",
                args=("foo",),
                node=node,
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=13,
            ),
            MessageTest(
                msg_id="missing-param-type-annotation",
                args=("x", "foo"),
                node=node,
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=13,
            ),
        ):
            self.checker.visit_asyncfunctiondef(node)

    def test_missing_param_type_annotation(self) -> None:
        """Test detection of missing parameter type annotation."""
        node = astroid.extract_node(
            """
        def foo(x) -> int:  #@
            return x
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-param-type-annotation",
                args=("x", "foo"),
                node=node,
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=7,
            )
        ):
            self.checker.visit_functiondef(node)

    def test_function_with_all_annotations(self) -> None:
        """Test that fully annotated functions don't trigger warnings."""
        node = astroid.extract_node(
            """
        def foo(x: int, y: str) -> bool:  #@
            return True
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_method_self_parameter_skipped(self) -> None:
        """Test that 'self' parameter is skipped in methods."""
        node = astroid.extract_node(
            """
        class MyClass:
            def foo(self, x: int) -> int:  #@
                return x
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_classmethod_cls_parameter_skipped(self) -> None:
        """Test that 'cls' parameter is skipped in classmethods."""
        node = astroid.extract_node(
            """
        class MyClass:
            @classmethod
            def foo(cls, x: int) -> int:  #@
                return x
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_abstract_method_skipped(self) -> None:
        """Test that abstract methods are skipped."""
        node = astroid.extract_node(
            """
        from abc import abstractmethod

        class MyClass:
            @abstractmethod
            def foo(self, x):  #@
                pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_property_skipped(self) -> None:
        """Test that property methods are skipped."""
        node = astroid.extract_node(
            """
        class MyClass:
            @property
            def foo(self):  #@
                return 42
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_vararg_missing_annotation(self) -> None:
        """Test detection of missing *args annotation."""
        node = astroid.extract_node(
            """
        def foo(*args) -> None:  #@
            pass
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-param-type-annotation",
                args=("args", "foo"),
                node=node,
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=7,
            )
        ):
            self.checker.visit_functiondef(node)

    def test_kwarg_missing_annotation(self) -> None:
        """Test detection of missing **kwargs annotation."""
        node = astroid.extract_node(
            """
        def foo(**kwargs) -> None:  #@
            pass
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-param-type-annotation",
                args=("kwargs", "foo"),
                node=node,
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=7,
            )
        ):
            self.checker.visit_functiondef(node)

    def test_fully_annotated_with_varargs(self) -> None:
        """Test that fully annotated functions with *args and **kwargs work."""
        node = astroid.extract_node(
            """
        def foo(x: int, *args: str, **kwargs: bool) -> None:  #@
            pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_keyword_only_args_missing_annotation(self) -> None:
        """Test detection of missing keyword-only argument annotations."""
        node = astroid.extract_node(
            """
        def foo(x: int, *, y) -> None:  #@
            pass
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-param-type-annotation",
                args=("y", "foo"),
                node=node,
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=7,
            )
        ):
            self.checker.visit_functiondef(node)
