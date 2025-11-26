# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the type_annotations checker."""

from __future__ import annotations

import astroid

from pylint.checkers.type_annotations import TypeAnnotationChecker
from pylint.testutils import CheckerTestCase, MessageTest


class TestTypeAnnotationChecker(
    CheckerTestCase
):  # pylint: disable=too-many-public-methods
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
        """Test that 'cls' parameter is skipped in class methods."""
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

    def test_type_comment_returns_skipped(self) -> None:
        """Test that functions with type comment returns are skipped."""
        node = astroid.extract_node(
            """
        def foo(x):  #@
            # type: (int) -> int
            return x
        """
        )
        # Should only check params, not return type
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

    def test_abstract_property_skipped(self) -> None:
        """Test that abstract properties are skipped."""
        node = astroid.extract_node(
            """
        from abc import abstractproperty

        class MyClass:
            @abstractproperty
            def foo(self):  #@
                pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_typing_overload_skipped(self) -> None:
        """Test that typing.overload decorated functions are skipped."""
        node = astroid.extract_node(
            """
        from typing import overload

        @overload
        def foo(x):  #@
            pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_typing_extensions_overload_skipped(self) -> None:
        """Test that typing_extensions.overload decorated functions are skipped."""
        node = astroid.extract_node(
            """
        from typing_extensions import overload

        @overload
        def foo(x):  #@
            pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_property_setter_skipped(self) -> None:
        """Test that property setters are skipped."""
        node = astroid.extract_node(
            """
        class MyClass:
            @property
            def foo(self) -> int:
                return 42

            @foo.setter
            def foo(self, value):  #@
                pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_property_deleter_skipped(self) -> None:
        """Test that property deleters are skipped."""
        node = astroid.extract_node(
            """
        class MyClass:
            @property
            def foo(self) -> int:
                return 42

            @foo.deleter
            def foo(self):  #@
                pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_builtins_property_skipped(self) -> None:
        """Test that builtins.property decorated functions are skipped."""
        node = astroid.extract_node(
            """
        import builtins

        class MyClass:
            @builtins.property
            def foo(self):  #@
                return 42
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_positional_only_args_missing_annotation(self) -> None:
        """Test detection of missing positional-only argument annotations."""
        node = astroid.extract_node(
            """
        def foo(x, y, /) -> None:  #@
            pass
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
            ),
            MessageTest(
                msg_id="missing-param-type-annotation",
                args=("y", "foo"),
                node=node,
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=7,
            ),
        ):
            self.checker.visit_functiondef(node)

    def test_positional_only_args_with_self_skipped(self) -> None:
        """Test that self is skipped in positional-only args."""
        node = astroid.extract_node(
            """
        class MyClass:
            def foo(self, x, /) -> None:  #@
                pass
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-param-type-annotation",
                args=("x", "foo"),
                node=node,
                line=3,
                col_offset=4,
                end_line=3,
                end_col_offset=11,
            )
        ):
            self.checker.visit_functiondef(node)

    def test_positional_only_args_fully_annotated(self) -> None:
        """Test that fully annotated positional-only args don't trigger warnings."""
        node = astroid.extract_node(
            """
        def foo(x: int, y: str, /) -> None:  #@
            pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_positional_only_args_with_cls_skipped(self) -> None:
        """Test that cls is skipped in positional-only args for classmethods."""
        node = astroid.extract_node(
            """
        class MyClass:
            @classmethod
            def foo(cls, x, /) -> None:  #@
                pass
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-param-type-annotation",
                args=("x", "foo"),
                node=node,
                line=4,
                col_offset=4,
                end_line=4,
                end_col_offset=11,
            )
        ):
            self.checker.visit_functiondef(node)

    def test_method_with_second_arg_missing_annotation(self) -> None:
        """Test that only self/cls is skipped, not subsequent args."""
        node = astroid.extract_node(
            """
        class MyClass:
            def foo(self, x, y: int) -> None:  #@
                pass
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-param-type-annotation",
                args=("x", "foo"),
                node=node,
                line=3,
                col_offset=4,
                end_line=3,
                end_col_offset=11,
            )
        ):
            self.checker.visit_functiondef(node)

    def test_mixed_positional_and_regular_args(self) -> None:
        """Test functions with both positional-only and regular args."""
        node = astroid.extract_node(
            """
        def foo(x: int, /, y, z: str) -> None:  #@
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

    def test_keyword_only_args_fully_annotated(self) -> None:
        """Test that fully annotated keyword-only args don't trigger warnings."""
        node = astroid.extract_node(
            """
        def foo(*, x: int, y: str) -> None:  #@
            pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)
