# Copyright (c) 2016-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016, 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2016 Glenn Matthews <glenn@e-dad.net>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Unit tests for the yield documentation checking in the
`DocstringChecker` in :mod:`pylint.extensions.check_docs`
"""

import astroid

from pylint.extensions.docparams import DocstringParameterChecker
from pylint.testutils import CheckerTestCase


class TestDocstringCheckerYield(CheckerTestCase):
    """Tests for pylint_plugin.RaiseDocChecker"""

    CHECKER_CLASS = DocstringParameterChecker

    # No such thing as redundant yield documentation for sphinx because it
    # doesn't support yield documentation

    # No such thing as redundant yield documentation for sphinx because it
    # doesn't support yield documentation

    def test_sphinx_missing_yield_type_with_annotations(self) -> None:
        node = astroid.extract_node(
            '''
            import typing

            def generator() -> typing.Iterator[int]:
                """A simple function for checking type hints.

                :returns: The number 0
                """
                yield 0
            '''
        )
        yield_node = node.body[0]
        with self.assertNoMessages():
            self.checker.visit_yield(yield_node)
