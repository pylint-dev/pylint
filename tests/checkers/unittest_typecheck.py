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

    def test_assignment_from_no_return_hint_args(self) -> None:
        """The no-return message can name attributes, names, and complex calls."""
        self.linter.config.known_side_effects_only_functions = (
            "reverse:reversed",
            "shuffle:sample",
            "malformed-entry-without-suggestion",
        )
        self.checker.open()
        module = astroid.parse("""
            items = []
            result = items.reverse()
            result = shuffle(items)
            functions = [shuffle]
            result = functions[0](items)
            """)
        reverse_assign = module.body[1]
        shuffle_assign = module.body[2]
        subscript_assign = module.body[4]

        assert self.checker._assignment_from_no_return_args(reverse_assign.value) == (
            "reverse",
            ", did you mean to use 'reversed(...)' instead?",
        )
        assert self.checker._assignment_from_no_return_args(shuffle_assign.value) == (
            "shuffle",
            ", did you mean to use 'sample(...)' instead?",
        )
        assert self.checker._assignment_from_no_return_args(subscript_assign.value) == (
            "functions[0]",
            "",
        )

    @needs_c_extension
    def test_nomember_on_c_extension_info_msg(self) -> None:
        node = astroid.extract_node("""
        from coverage import tracer
        tracer.CTracer  #@
        """)
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
        module = astroid.parse("""
        import collections
        test = collections[int]
        """)
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
        module = astroid.parse(f"""
        import typing
        test = typing.{generic}[int]
        """)
        subscript = module.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_subscript(subscript)

    def decorated_by_a_subscriptable_class(self, decorators: str) -> None:
        module = astroid.parse(decorators + """
        @Subscriptable
        def decorated():
            ...

        test = decorated[None]
        """)
        subscript = module.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_subscript(subscript)

    def decorated_by_subscriptable_then_unsubscriptable_class(
        self, decorators: str
    ) -> None:
        module = astroid.parse(decorators + """
        @Unsubscriptable
        @Subscriptable
        def decorated():
            ...

        test = decorated[None]
        """)
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
        module = astroid.parse(decorators + """
        @Subscriptable
        @Unsubscriptable
        def decorated():
            ...

        test = decorated[None]
        """)
        subscript = module.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_subscript(subscript)

    def decorated_by_an_unsubscriptable_class(self, decorators: str) -> None:
        module = astroid.parse(decorators + """
        @Unsubscriptable
        def decorated():
            ...

        test = decorated[None]
        """)
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


class TestDataclassFieldAliases(CheckerTestCase):
    """Tests for dataclass field alias support (issue #9090)."""

    CHECKER_CLASS = typecheck.TypeChecker

    def test_dataclass_field_alias_accepted(self) -> None:
        module = astroid.parse("""
        from pydantic import Field
        from pydantic.dataclasses import dataclass

        @dataclass
        class Example:
            number: int = Field(alias='n')

        example = Example(n=5)
        """)
        call_node = module.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_dataclass_field_name_accepted(self) -> None:
        module = astroid.parse("""
        from pydantic import Field
        from pydantic.dataclasses import dataclass

        @dataclass
        class Example:
            number: int = Field(alias='n')

        example = Example(number=5)
        """)
        call_node = module.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_dataclass_both_alias_and_field_name_redundant(self) -> None:
        module = astroid.parse("""
        from pydantic import Field
        from pydantic.dataclasses import dataclass

        @dataclass
        class Example:
            number: int = Field(alias='n')

        example = Example(number=5, n=5)
        """)
        call_node = module.body[-1].value
        with self.assertAddsMessages(
            MessageTest(
                "redundant-keyword-arg",
                node=call_node,
                args=("n", "constructor"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(call_node)

    def test_dataclass_positional_and_alias_redundant(self) -> None:
        module = astroid.parse("""
        from pydantic import Field
        from pydantic.dataclasses import dataclass

        @dataclass
        class Example:
            number: int = Field(alias='n')

        example = Example(5, n=5)
        """)
        call_node = module.body[-1].value
        with self.assertAddsMessages(
            MessageTest(
                "redundant-keyword-arg",
                node=call_node,
                args=("n", "constructor"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(call_node)

    def test_dataclass_unexpected_keyword_still_emitted(self) -> None:
        module = astroid.parse("""
        from pydantic import Field
        from pydantic.dataclasses import dataclass

        @dataclass
        class Example:
            number: int = Field(alias='n')

        example = Example(unknown=5)
        """)
        call_node = module.body[-1].value
        with self.assertAddsMessages(
            MessageTest(
                "unexpected-keyword-arg",
                node=call_node,
                args=("unknown", "constructor"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(call_node)

    def test_dataclass_alias_choices_accepted(self) -> None:
        module = astroid.parse("""
        from pydantic import Field, AliasChoices
        from pydantic.dataclasses import dataclass

        @dataclass
        class ChoicesExample:
            f: str = Field(validation_alias=AliasChoices('f_alias', 'f_alt'))

        c1 = ChoicesExample(f_alias='val')
        c2 = ChoicesExample(f_alt='val')
        """)
        call1 = module.body[-2].value
        call2 = module.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_call(call1)
        with self.assertNoMessages():
            self.checker.visit_call(call2)

    def test_dataclass_inheritance_aliases_accepted(self) -> None:
        module = astroid.parse("""
        from pydantic import Field
        from pydantic.dataclasses import dataclass

        @dataclass
        class Base:
            base_field: str = Field(alias='bf')

        @dataclass
        class Derived(Base):
            derived_field: int = Field(alias='df')

        d = Derived(bf='hello', df=10)
        """)
        call_node = module.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_call(call_node)
