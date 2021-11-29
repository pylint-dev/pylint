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
from pylint.testutils import CheckerTestCase, MessageTest, set_config


class TestDocstringCheckerYield(CheckerTestCase):
    """Tests for pylint_plugin.RaiseDocChecker"""

    CHECKER_CLASS = DocstringParameterChecker

    @set_config(accept_no_yields_doc="no")
    def test_warns_google_yield_list_of_custom_class_without_description(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Yields:
                list(:class:`mymodule.Class`):
            """
            yield [mymodule.Class()]
        '''
        )
        yield_node = node.body[0]
        with self.assertAddsMessages(
            MessageTest(msg_id="missing-yield-doc", node=node)
        ):
            self.checker.visit_yield(yield_node)

    @set_config(accept_no_yields_doc="no")
    def test_warns_numpy_yield_list_of_custom_class_without_description(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Yields
            -------
                list(:class:`mymodule.Class`)
            """
            yield [mymodule.Class()]
        '''
        )
        yield_node = node.body[0]
        with self.assertAddsMessages(
            MessageTest(msg_id="missing-yield-doc", node=node)
        ):
            self.checker.visit_yield(yield_node)

    # No such thing as redundant yield documentation for sphinx because it
    # doesn't support yield documentation

    def test_ignores_google_redundant_yield_doc_multiple_yields(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Yields:
                int or None: One, or sometimes None.
            """
            if a_func():
                yield None
            yield 1
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_ignores_numpy_redundant_yield_doc_multiple_yields(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Yields
            -------
                int
                    One
                None
                    Sometimes
            """
            if a_func():
                yield None
            yield 1
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    # No such thing as redundant yield documentation for sphinx because it
    # doesn't support yield documentation

    def test_warns_google_redundant_yield_doc_return(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Yields:
                int: One
            """
            return 1
        '''
        )
        with self.assertAddsMessages(
            MessageTest(msg_id="redundant-yields-doc", node=node)
        ):
            self.checker.visit_functiondef(node)

    def test_warns_numpy_redundant_yield_doc_return(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Yields
            -------
                int
                    One
            """
            return 1
        '''
        )
        with self.assertAddsMessages(
            MessageTest(msg_id="redundant-yields-doc", node=node)
        ):
            self.checker.visit_functiondef(node)

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

    def test_google_missing_yield_type_with_annotations(self) -> None:
        node = astroid.extract_node(
            '''
            import typing

            def generator() -> typing.Iterator[int]:
                """A simple function for checking type hints.

                Yields:
                    The number 0
                """
                yield 0
            '''
        )
        yield_node = node.body[0]
        with self.assertNoMessages():
            self.checker.visit_yield(yield_node)
