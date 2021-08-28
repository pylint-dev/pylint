# Copyright (c) 2021 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2021 Rebecca Turner <rbt@sent.as>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE


import astroid

from pylint.checkers import design_analysis
from pylint.testutils import CheckerTestCase, set_config


class TestDesignChecker(CheckerTestCase):

    CHECKER_CLASS = design_analysis.MisdesignChecker

    @set_config(
        ignored_parents=(".Dddd",),
        max_parents=1,
    )
    def test_too_many_ancestors_ignored_parents_are_skipped(self):
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
