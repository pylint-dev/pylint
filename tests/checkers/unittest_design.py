# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2021 Rebecca Turner <rbt@sent.as>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE


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

    def test_too_few_public_methods(self) -> None:
        """Tests the default ``min-public-methods`` config value of 2
        triggers too-few-public-methods"""
        node = astroid.extract_node(
            """
            class SomeModel:
                def dummy(self):
                    pass
            """
        )
        message = MessageTest(
            "too-few-public-methods",
            node=node,
            args=(1, 2),
        )
        with self.assertAddsMessages(message):
            self.checker.leave_classdef(node)

    @set_config(exclude_too_few_public_methods=("toml.*"))
    @set_config(min_public_methods=20)  # to combat inherited methods
    def test_exclude_too_few_methods(self) -> None:
        """Tests config setting ``exclude-too-few-public-methods`` with a
        comma-separated regular expression suppresses the message for
        `too-few-public-methods` on classes that match the regular expression.
        """
        node = astroid.extract_node(
            """
            from toml import TomlEncoder

            class MyTomlEncoder(TomlEncoder):
                ...
            """
        )
        with self.assertNoMessages():
            self.checker.leave_classdef(node)
