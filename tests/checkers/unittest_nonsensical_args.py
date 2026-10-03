# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the mixin that third party checkers extend."""

from __future__ import annotations

from collections.abc import Iterable

import astroid

from pylint.checkers import BaseChecker, NonsensicalArgument, NonsensicalArgumentsMixin
from pylint.interfaces import INFERENCE
from pylint.testutils import CheckerTestCase, MessageTest

# What a plugin for a library of our own would register. "juice" is
# keyword-only and rejects both values, "slices" is positional and only
# rejects infinity.
SQUEEZE = (
    NonsensicalArgument(
        None,
        "juice",
        on_inf="an endless glass of juice is never filled",
        on_nan="a glass of NaN juice is not a glass of juice",
    ),
    NonsensicalArgument(
        1, "slices", on_inf="an orange has a countable number of slices"
    ),
)


class _FruitChecker(NonsensicalArgumentsMixin, BaseChecker):
    name = "fruit"
    msgs = {**NonsensicalArgumentsMixin.NONSENSICAL_ARGUMENT_MESSAGE}

    def nonsensical_arguments(self, qname: str) -> Iterable[NonsensicalArgument]:
        return SQUEEZE if qname == "fruit.squeeze" else ()


class TestNonsensicalArgumentsMixin(CheckerTestCase):
    CHECKER_CLASS = _FruitChecker

    @staticmethod
    def _call(source: str) -> astroid.nodes.Call:
        node = astroid.extract_node(f"""
        import math

        def squeeze(orange, slices=8, *, juice=1.0):
            return orange, slices, juice

        {source}  #@
        """)
        node.root().name = "fruit"
        assert isinstance(node, astroid.nodes.Call)
        return node

    def test_keyword_only_argument_is_checked(self) -> None:
        node = self._call("squeeze('orange', juice=math.inf)")
        with self.assertAddsMessages(
            MessageTest(
                msg_id="nonsensical-float-arg",
                args=(
                    "math.inf",
                    "juice",
                    "squeeze",
                    "an endless glass of juice is never filled",
                ),
                node=node.keywords[0].value,
                confidence=INFERENCE,
                line=7,
                col_offset=24,
                end_line=7,
                end_col_offset=32,
            )
        ):
            self.checker.visit_call(node)

    def test_positional_argument_is_checked(self) -> None:
        node = self._call("squeeze('orange', math.inf)")
        with self.assertAddsMessages(
            MessageTest(
                msg_id="nonsensical-float-arg",
                args=(
                    "math.inf",
                    "slices",
                    "squeeze",
                    "an orange has a countable number of slices",
                ),
                node=node.args[1],
                confidence=INFERENCE,
                line=7,
                col_offset=18,
                end_line=7,
                end_col_offset=26,
            )
        ):
            self.checker.visit_call(node)

    def test_value_the_entry_allows_is_ignored(self) -> None:
        # "slices" leaves on_nan unset, so NaN is not reported for it.
        node = self._call("squeeze('orange', math.nan)")
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_finite_arguments_are_ignored(self) -> None:
        node = self._call("squeeze('orange', 4, juice=0.5)")
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_unregistered_call_is_ignored(self) -> None:
        node = astroid.extract_node("""
        import math

        def peel(fruit, juice=1.0):
            return fruit, juice

        peel('banana', juice=math.inf)  #@
        """)
        with self.assertNoMessages():
            self.checker.visit_call(node)
