# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import astroid

from pylint.checkers import design_analysis
from pylint.testutils import CheckerTestCase, MessageTest, set_config


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


class TestUnusedSelfChecker(CheckerTestCase):
    CHECKER_CLASS = design_analysis.MisdesignChecker

    def test_method_with_unused_self(self):
        module_node = astroid.parse(
            """
            class MyClass:
                def my_method(self, arg):
                    return
        """
        )
        self.linter.config.ignored_argument_names = None
        self.walk(module_node)
        method_node = module_node.body[0].body[0]
        class_node = module_node.body[0]

        expected_messages = [
            MessageTest(
                msg_id="unused-self",
                line=3,
                node=method_node,
                col_offset=4,
                end_line=3,
                end_col_offset=17,
            ),
            MessageTest(
                msg_id="too-few-public-methods",
                line=2,
                node=class_node,
                args=(1, 2),
                end_col_offset=13,
                col_offset=0,
                end_line=2,
            ),
        ]

        with self.assertAddsMessages(*expected_messages):
            pass

    def test_method_using_self(self):
        # This method should not trigger the 'unused-self' warning
        module_node = astroid.parse(
            """
            class MyClass:
                def my_method(self, arg):  #@
                    print(self)
                    return arg
            """
        )
        class_node = module_node.body[0]
        # Manually visit the class definition node
        self.checker.visit_classdef(class_node)
        with self.assertNoMessages():
            pass
