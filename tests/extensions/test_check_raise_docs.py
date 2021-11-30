# Copyright (c) 2016-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016, 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2016 Glenn Matthews <glenn@e-dad.net>
# Copyright (c) 2018 Jim Robertson <jrobertson98atx@gmail.com>
# Copyright (c) 2018 Adam Dangoor <adamdangoor@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Danny Hermes <daniel.j.hermes@gmail.com>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Unit tests for the raised exception documentation checking in the
`DocstringChecker` in :mod:`pylint.extensions.check_docs`
"""


import astroid

from pylint.extensions.docparams import DocstringParameterChecker
from pylint.testutils import CheckerTestCase


class TestDocstringCheckerRaise(CheckerTestCase):
    """Tests for pylint_plugin.RaiseDocChecker"""

    CHECKER_CLASS = DocstringParameterChecker

    def test_ignores_returns_use_only_names(self) -> None:
        raise_node = astroid.extract_node(
            '''
        def myfunc():
            """This is a docstring

            :raises NameError: Never
            """
            def inner_func():
                return 42

            raise inner_func() #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_ignores_returns_use_only_exception_instances(self) -> None:
        raise_node = astroid.extract_node(
            '''
        def myfunc():
            """This is a docstring

            :raises MyException: Never
            """
            class MyException(Exception):
                pass
            def inner_func():
                return MyException

            raise inner_func() #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_no_crash_when_inferring_handlers(self) -> None:
        raise_node = astroid.extract_node(
            '''
        import collections

        def test():
           """raises

           :raise U: pass
           """
           try:
              pass
           except collections.U as exc:
              raise #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_no_crash_when_cant_find_exception(self) -> None:
        raise_node = astroid.extract_node(
            '''
        import collections

        def test():
           """raises

           :raise U: pass
           """
           try:
              pass
           except U as exc:
              raise #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_no_error_notimplemented_documented(self) -> None:
        raise_node = astroid.extract_node(
            '''
        def my_func():
            """
            Raises:
                NotImplementedError: When called.
            """
            raise NotImplementedError #@
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)
