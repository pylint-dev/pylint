# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import astroid
import pytest

from pylint.checkers import typecheck
from pylint.interfaces import INFERENCE, UNDEFINED
from pylint.testutils import CheckerTestCase, MessageTest

try:
    from coverage import tracer as _

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


class TestTypeCheckerStringDistance:
    """Tests for the _string_distance helper in pylint.checkers.typecheck."""

    def test_string_distance_identical_strings(self) -> None:
        seq1 = "hi"
        seq2 = "hi"
        assert typecheck._string_distance(seq1, seq2, len(seq1), len(seq2)) == 0

        seq1, seq2 = seq2, seq1
        assert typecheck._string_distance(seq1, seq2, len(seq1), len(seq2)) == 0

    def test_string_distance_empty_string(self) -> None:
        seq1 = ""
        seq2 = "hi"
        assert typecheck._string_distance(seq1, seq2, len(seq1), len(seq2)) == 2

        seq1, seq2 = seq2, seq1
        assert typecheck._string_distance(seq1, seq2, len(seq1), len(seq2)) == 2

    def test_string_distance_edit_distance_one_character(self) -> None:
        seq1 = "hi"
        seq2 = "he"
        assert typecheck._string_distance(seq1, seq2, len(seq1), len(seq2)) == 1

        seq1, seq2 = seq2, seq1
        assert typecheck._string_distance(seq1, seq2, len(seq1), len(seq2)) == 1

    def test_string_distance_edit_distance_multiple_similar_characters(self) -> None:
        seq1 = "hello"
        seq2 = "yelps"
        assert typecheck._string_distance(seq1, seq2, len(seq1), len(seq2)) == 3

        seq1, seq2 = seq2, seq1
        assert typecheck._string_distance(seq1, seq2, len(seq1), len(seq2)) == 3

    def test_string_distance_edit_distance_all_dissimilar_characters(self) -> None:
        seq1 = "yellow"
        seq2 = "orange"
        assert typecheck._string_distance(seq1, seq2, len(seq1), len(seq2)) == 6

        seq1, seq2 = seq2, seq1
        assert typecheck._string_distance(seq1, seq2, len(seq1), len(seq2)) == 6
