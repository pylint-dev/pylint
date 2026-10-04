# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import astroid
import pytest

from pylint import checkers
from pylint.checkers import design_analysis
from pylint.lint import PyLinter
from pylint.testutils import CheckerTestCase, set_config
from pylint.utils import ASTWalker


class TestDesignChecker(CheckerTestCase):
    CHECKER_CLASS = design_analysis.MisdesignChecker

    @set_config(
        ignored_parents=(".Dddd",),
        max_parents=1,
    )
    def test_too_many_ancestors_ignored_parents_are_skipped(self) -> None:
        """Make sure that classes listed in ``ignored-parents`` aren't counted
        by the too-many-ancestors message.
        """
        node = astroid.extract_node("""
        class Aaaa(object):
            pass
        class Bbbb(Aaaa):
            pass
        class Cccc(Bbbb):
            pass
        class Dddd(Cccc):
            pass
        class Eeee(Dddd):
            pass
        """)
        with self.assertNoMessages():
            self.checker.visit_classdef(node)

    @set_config(exclude_too_few_public_methods="toml.*")
    def test_exclude_too_few_methods_with_value(self) -> None:
        """Test exclude-too-few-public-methods option with value."""
        options = self.linter.config.exclude_too_few_public_methods

        assert any(i.match("toml") for i in options)
        assert any(i.match("toml.*") for i in options)
        assert any(i.match("toml.TomlEncoder") for i in options)

    def test_ignore_paths_with_no_value(self) -> None:
        """Test exclude-too-few-public-methods option with no value.
        Compare against actual list to see if validator works.
        """
        options = self.linter.config.exclude_too_few_public_methods

        assert options == []


    @pytest.mark.parametrize(
        "code_snippet",
        [
            # Case 1: Subscripted generic class with custom __class_getitem__
            """
            class Parent:
                def __class_getitem__(cls, item):
                    return super().__class_getitem__(item)
                def method_one(self): pass
                def method_two(self): pass
            class Child(Parent[int]):
                pass
            """,
            # Case 2: Multi-level inheritance through a subscripted generic
            """
            class GrandParent:
                def method_one(self): pass
                def method_two(self): pass
            class Parent(GrandParent):
                def __class_getitem__(cls, item):
                    return super().__class_getitem__(item)
            class Child(Parent[str]):
                pass
            """,
        ],
    )
    def test_too_few_public_methods_subscripted_generic(
        self, code_snippet: str
    ) -> None:
        """Ensure subscripted generic base classes (whose __class_getitem__
        is uninferable) do not trigger false positive too-few-public-methods (R0903).
        """
        node = astroid.extract_node(code_snippet)
        with self.assertNoMessages():
            self.checker.leave_classdef(node)


def test_function_counters_are_popped_with_one_message_enabled() -> None:
    """``leave_functiondef`` must run whenever ``visit_functiondef`` ran.
    Otherwise the counters pushed for each function are never popped, and every
    statement of the run increments all of them.
    """
    linter = PyLinter()
    checkers.initialize(linter)
    checker = next(
        c
        for c in linter.get_checkers()
        if isinstance(c, design_analysis.MisdesignChecker)
    )
    linter.disable("all")
    linter.enable("too-many-positional-arguments")
    walker = ASTWalker(linter)
    walker.add_checker(checker)
    checker.open()
    walker.walk(astroid.parse("def func(arg):\n    return arg\n"))
    assert not checker._returns
    assert not checker._stmts
