# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import astroid
import pytest

from pylint.checkers import typecheck
from pylint.interfaces import INFERENCE, UNDEFINED
from pylint.testutils import CheckerTestCase, MessageTest, set_config

try:
    from coverage import tracer as _  # pylint: disable=unused-import

    C_EXTENTIONS_AVAILABLE = True
except ImportError:
    _ = None
    C_EXTENTIONS_AVAILABLE = False

needs_c_extension = pytest.mark.skipif(
    not C_EXTENTIONS_AVAILABLE, reason="Requires coverage (source of C-extension)"
)


class TestTypeChecker(CheckerTestCase):
    """Tests for pylint.checkers.typecheck."""

    CHECKER_CLASS = typecheck.TypeChecker

    @set_config(suggestion_mode=False)
    @needs_c_extension
    def test_nomember_on_c_extension_error_msg(self) -> None:
        node = astroid.extract_node(
            """
        from coverage import tracer
        tracer.CTracer  #@
        """
        )
        message = MessageTest(
            "no-member",
            node=node,
            args=("Module", "coverage.tracer", "CTracer", ""),
            confidence=INFERENCE,
            line=3,
            col_offset=0,
            end_line=3,
            end_col_offset=14,
        )
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    @set_config(suggestion_mode=True)
    @needs_c_extension
    def test_nomember_on_c_extension_info_msg(self) -> None:
        node = astroid.extract_node(
            """
        from coverage import tracer
        tracer.CTracer  #@
        """
        )
        message = MessageTest(
            "c-extension-no-member",
            node=node,
            args=("Module", "coverage.tracer", "CTracer", ""),
            confidence=INFERENCE,
            line=3,
            col_offset=0,
            end_line=3,
            end_col_offset=14,
        )
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)


class TestTypeCheckerOnDecorators(CheckerTestCase):
    """Tests for pylint.checkers.typecheck on decorated functions."""

    CHECKER_CLASS = typecheck.TypeChecker

    def test_issue3882_class_decorators(self) -> None:
        decorators = """
        class Unsubscriptable:
            def __init__(self, f):
                self.f = f

        class Subscriptable:
            def __init__(self, f):
                self.f = f

            def __getitem__(self, item):
                return item
        """
        for generic in "Optional", "List", "ClassVar", "Final", "Literal":
            self.typing_objects_are_subscriptable(generic)

        self.getitem_on_modules()
        self.decorated_by_a_subscriptable_class(decorators)
        self.decorated_by_an_unsubscriptable_class(decorators)

        self.decorated_by_subscriptable_then_unsubscriptable_class(decorators)
        self.decorated_by_unsubscriptable_then_subscriptable_class(decorators)

    def getitem_on_modules(self) -> None:
        """Mainly validate the code won't crash if we're not having a function."""
        module = astroid.parse(
            """
        import collections
        test = collections[int]
        """
        )
        subscript = module.body[-1].value
        with self.assertAddsMessages(
            MessageTest(
                "unsubscriptable-object",
                node=subscript.value,
                args="collections",
                confidence=UNDEFINED,
                line=3,
                col_offset=7,
                end_line=3,
                end_col_offset=18,
            )
        ):
            self.checker.visit_subscript(subscript)

    def typing_objects_are_subscriptable(self, generic: str) -> None:
        module = astroid.parse(
            f"""
        import typing
        test = typing.{generic}[int]
        """
        )
        subscript = module.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_subscript(subscript)

    def decorated_by_a_subscriptable_class(self, decorators: str) -> None:
        module = astroid.parse(
            decorators
            + """
        @Subscriptable
        def decorated():
            ...

        test = decorated[None]
        """
        )
        subscript = module.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_subscript(subscript)

    def decorated_by_subscriptable_then_unsubscriptable_class(
        self, decorators: str
    ) -> None:
        module = astroid.parse(
            decorators
            + """
        @Unsubscriptable
        @Subscriptable
        def decorated():
            ...

        test = decorated[None]
        """
        )
        subscript = module.body[-1].value
        with self.assertAddsMessages(
            MessageTest(
                "unsubscriptable-object",
                node=subscript.value,
                args="decorated",
                confidence=UNDEFINED,
                line=18,
                col_offset=7,
                end_line=18,
                end_col_offset=16,
            )
        ):
            self.checker.visit_subscript(subscript)

    def decorated_by_unsubscriptable_then_subscriptable_class(
        self, decorators: str
    ) -> None:
        module = astroid.parse(
            decorators
            + """
        @Subscriptable
        @Unsubscriptable
        def decorated():
            ...

        test = decorated[None]
        """
        )
        subscript = module.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_subscript(subscript)

    def decorated_by_an_unsubscriptable_class(self, decorators: str) -> None:
        module = astroid.parse(
            decorators
            + """
        @Unsubscriptable
        def decorated():
            ...

        test = decorated[None]
        """
        )
        subscript = module.body[-1].value
        with self.assertAddsMessages(
            MessageTest(
                "unsubscriptable-object",
                node=subscript.value,
                args="decorated",
                confidence=UNDEFINED,
                line=17,
                col_offset=7,
                end_line=17,
                end_col_offset=16,
            )
        ):
            self.checker.visit_subscript(subscript)


class TestTypeCheckerNoMemberCache(CheckerTestCase):
    """Tests for the no-member checker cache."""

    CHECKER_CLASS = typecheck.TypeChecker

    def test_cache_fill(self) -> None:
        """Tests a variety of formats for cache keys."""
        self.checker.node_exists = {}

        nodes = astroid.extract_node(
            """
        class Object1:
            def method(self):
                return

        class Object2:
            val = 3

        Object1().method  #@
        Object2().method  #@
        Object1.val  #@
        Object2.val  #@
        obj1 = Object1()
        obj2 = Object2()
        obj1.method()  #@
        obj2.method()  #@
        """
        )

        # 0: Object1().method
        with self.assertNoMessages():
            self.checker.visit_attribute(nodes[0])
        assert len(self.checker.node_exists) == 1
        assert self.checker.node_exists.get(("", 0, "Object1().method")) is True

        # 1: Object2().method
        with self.assertAddsMessages(
            MessageTest(
                "no-member",
                node=nodes[1],
                args=("Instance of", "Object2", "method", ""),
                confidence=INFERENCE,
                line=10,
                col_offset=0,
                end_line=10,
                end_col_offset=16,
            )
        ):
            self.checker.visit_attribute(nodes[1])
        assert len(self.checker.node_exists) == 2
        assert self.checker.node_exists.get(("", 0, "Object2().method")) is False

        # 2: Object1.val
        with self.assertAddsMessages(
            MessageTest(
                "no-member",
                node=nodes[2],
                args=("Class", "Object1", "val", ""),
                confidence=INFERENCE,
                line=11,
                col_offset=0,
                end_line=11,
                end_col_offset=11,
            )
        ):
            self.checker.visit_attribute(nodes[2])
        assert len(self.checker.node_exists) == 3
        assert self.checker.node_exists.get(("", 0, "Object1.val")) is False

        # 3: Object2.val
        with self.assertNoMessages():
            self.checker.visit_attribute(nodes[3])
        assert len(self.checker.node_exists) == 4
        assert self.checker.node_exists.get(("", 0, "Object2.val")) is True

        # 4: obj1.method()
        obj1_method_attr = nodes[4].func
        with self.assertNoMessages():
            self.checker.visit_attribute(obj1_method_attr)
        assert len(self.checker.node_exists) == 5
        assert self.checker.node_exists.get(("", 0, "obj1.method")) is True

        # 5: obj2.method()
        obj2_method_attr = nodes[5].func
        with self.assertAddsMessages(
            MessageTest(
                "no-member",
                node=obj2_method_attr,
                args=("Instance of", "Object2", "method", ""),
                confidence=INFERENCE,
                line=16,
                col_offset=0,
                end_line=16,
                end_col_offset=11,
            )
        ):
            self.checker.visit_attribute(obj2_method_attr)
        assert len(self.checker.node_exists) == 6
        assert self.checker.node_exists.get(("", 0, "obj2.method")) is False

    def test_cache_hit(self) -> None:
        """Tests basic functionality for cache hits."""
        self.checker.node_exists = {}

        nodes = astroid.extract_node(
            """
        from collections import Counter

        Counter().elements  #@
        Counter().elements  #@
        Counter().b  #@
        Counter().b  #@
        """
        )

        with self.assertNoMessages():
            self.checker.visit_attribute(nodes[0])
        assert len(self.checker.node_exists) == 1
        assert self.checker.node_exists.get(("", 0, "Counter().elements")) is True

        # Cache hit
        with self.assertNoMessages():
            self.checker.visit_attribute(nodes[1])
        assert len(self.checker.node_exists) == 1
        assert self.checker.node_exists.get(("", 0, "Counter().elements")) is True

        with self.assertAddsMessages(
            MessageTest(
                "no-member",
                node=nodes[2],
                args=("Instance of", "Counter", "b", ""),
                confidence=INFERENCE,
                line=6,
                col_offset=0,
                end_line=6,
                end_col_offset=11,
            )
        ):
            self.checker.visit_attribute(nodes[2])
        assert len(self.checker.node_exists) == 2
        assert self.checker.node_exists.get(("", 0, "Counter().b")) is False

        # Technically a cache hit but we execute the rest of the function anyways
        with self.assertAddsMessages(
            MessageTest(
                "no-member",
                node=nodes[3],
                args=("Instance of", "Counter", "b", ""),
                confidence=INFERENCE,
                line=7,
                col_offset=0,
                end_line=7,
                end_col_offset=11,
            )
        ):
            self.checker.visit_attribute(nodes[3])
        assert len(self.checker.node_exists) == 2
        assert self.checker.node_exists.get(("", 0, "Counter().b")) is False

    def test_scoped_cache(self) -> None:
        """Tests scoped cache."""
        self.checker.node_exists = {}

        nodes = astroid.extract_node(
            """
        class CounterContainerA:
            class SpecialCounter:
                elements = [1, 2, 3]

            counter = SpecialCounter()

            def get_b(self):
                self.counter.elements  #@
                self.counter.b  #@

        class CounterContainerB:
            class SpecialCounter:
                elements = [1, 2, 3]
                b = 12

            counter = SpecialCounter()

            def get_b(self):
                self.counter.elements  #@
                self.counter.b  #@
        """
        )

        with self.assertNoMessages():
            self.checker.visit_attribute(nodes[0])
        assert len(self.checker.node_exists) == 1
        assert (
            self.checker.node_exists.get(("CounterContainerA", 2, "counter.elements"))
            is True
        )

        with self.assertAddsMessages(
            MessageTest(
                "no-member",
                node=nodes[1],
                args=("Instance of", "SpecialCounter", "b", ""),
                confidence=INFERENCE,
                line=10,
                col_offset=8,
                end_line=10,
                end_col_offset=22,
            )
        ):
            self.checker.visit_attribute(nodes[1])
        assert len(self.checker.node_exists) == 2
        assert (
            self.checker.node_exists.get(("CounterContainerA", 2, "counter.b")) is False
        )

        with self.assertNoMessages():
            self.checker.visit_attribute(nodes[2])
        assert len(self.checker.node_exists) == 3
        assert (
            self.checker.node_exists.get(("CounterContainerB", 12, "counter.elements"))
            is True
        )

        with self.assertNoMessages():
            self.checker.visit_attribute(nodes[3])
        assert len(self.checker.node_exists) == 4
        assert (
            self.checker.node_exists.get(("CounterContainerB", 12, "counter.b")) is True
        )
