# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors


import astroid

from pylint.checkers import design_analysis
from pylint.testutils import CheckerTestCase, set_config
from pylint.utils.utils import get_global_option


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

        node = astroid.extract_node(
            """
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
        """
        )
        with self.assertNoMessages():
            self.checker.visit_classdef(node)

    @set_config(exclude_too_few_public_methods="toml.*")
    def test_exclude_too_few_methods_with_value(self) -> None:
        """Test exclude-too-few-public-methods option with value."""
        options = get_global_option(self.checker, "exclude-too-few-public-methods")

        assert any(i.match("toml") for i in options)
        assert any(i.match("toml.*") for i in options)
        assert any(i.match("toml.TomlEncoder") for i in options)

    def test_ignore_paths_with_no_value(self) -> None:
        """Test exclude-too-few-public-methods option with no value.
        Compare against actual list to see if validator works.
        """
        options = get_global_option(self.checker, "exclude-too-few-public-methods")

        assert options == []
