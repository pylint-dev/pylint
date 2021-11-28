# Copyright (c) 2014-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2017 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2018 Bryce Guinta <bryce.guinta@protonmail.com>
# Copyright (c) 2018 Bryce Guinta <bryce.paul.guinta@gmail.com>
# Copyright (c) 2018 mar-chi-pan <mar.polatoglou@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Andrew Simmons <anjsimmo@gmail.com>
# Copyright (c) 2020 Andrew Simmons <a.simmons@deakin.edu.au>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Sergei Lebedev <185856+superbobry@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import os
import re
import sys
from pathlib import Path

import astroid

from pylint.checkers import variables
from pylint.interfaces import HIGH
from pylint.testutils import CheckerTestCase, MessageTest, linter, set_config

REGR_DATA_DIR = str(Path(__file__).parent / ".." / "regrtest_data")


class TestVariablesChecker(CheckerTestCase):

    CHECKER_CLASS = variables.VariablesChecker

    def test_all_elements_without_parent(self) -> None:
        node = astroid.extract_node("__all__ = []")
        node.value.elts.append(astroid.Const("test"))
        root = node.root()
        with self.assertNoMessages():
            self.checker.visit_module(root)
            self.checker.leave_module(root)


class TestVariablesCheckerWithTearDown(CheckerTestCase):

    CHECKER_CLASS = variables.VariablesChecker

    def setup_method(self) -> None:
        super().setup_method()
        self._to_consume_backup = self.checker._to_consume
        self.checker._to_consume = []

    def teardown_method(self) -> None:
        self.checker._to_consume = self._to_consume_backup

    @set_config(callbacks=("callback_", "_callback"))
    def test_custom_callback_string(self) -> None:
        """Test the --calbacks option works."""
        node = astroid.extract_node(
            """
        def callback_one(abc):
             ''' should not emit unused-argument. '''
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)
            self.checker.leave_functiondef(node)

        node = astroid.extract_node(
            """
        def two_callback(abc, defg):
             ''' should not emit unused-argument. '''
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)
            self.checker.leave_functiondef(node)

        node = astroid.extract_node(
            """
        def normal_func(abc):
             ''' should emit unused-argument. '''
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                "unused-argument", node=node["abc"], args="abc", confidence=HIGH
            )
        ):
            self.checker.visit_functiondef(node)
            self.checker.leave_functiondef(node)

        node = astroid.extract_node(
            """
        def cb_func(abc):
             ''' Previous callbacks are overridden. '''
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                "unused-argument", node=node["abc"], args="abc", confidence=HIGH
            )
        ):
            self.checker.visit_functiondef(node)
            self.checker.leave_functiondef(node)

    @set_config(redefining_builtins_modules=("os",))
    def test_redefined_builtin_modname_not_ignored(self) -> None:
        node = astroid.parse(
            """
        from future.builtins import open
        """
        )
        with self.assertAddsMessages(
            MessageTest("redefined-builtin", node=node.body[0], args="open")
        ):
            self.checker.visit_module(node)

    @set_config(redefining_builtins_modules=("os",))
    def test_redefined_builtin_in_function(self) -> None:
        node = astroid.extract_node(
            """
        def test():
            from os import open
        """
        )
        with self.assertNoMessages():
            self.checker.visit_module(node.root())
            self.checker.visit_functiondef(node)

    def test_import_as_underscore(self) -> None:
        node = astroid.parse(
            """
        import math as _
        """
        )
        with self.assertNoMessages():
            self.walk(node)

    def test_lambda_in_classdef(self) -> None:
        # Make sure lambda doesn't raises
        # Undefined-method in class def

        # Issue 1824
        # https://github.com/PyCQA/pylint/issues/1824
        node = astroid.parse(
            """
        class MyObject(object):
            method1 = lambda func: func()
            method2 = lambda function: function()
        """
        )
        with self.assertNoMessages():
            self.walk(node)

    def test_nested_lambda(self) -> None:
        """Make sure variables from parent lambdas
        aren't noted as undefined

        https://github.com/PyCQA/pylint/issues/760
        """
        node = astroid.parse(
            """
        lambda x: lambda: x + 1
        """
        )
        with self.assertNoMessages():
            self.walk(node)

    @set_config(ignored_argument_names=re.compile("arg"))
    def test_ignored_argument_names_no_message(self) -> None:
        """Make sure is_ignored_argument_names properly ignores
        function arguments"""
        node = astroid.parse(
            """
        def fooby(arg):
            pass
        """
        )
        with self.assertNoMessages():
            self.walk(node)

    @set_config(ignored_argument_names=re.compile("args|kwargs"))
    def test_ignored_argument_names_starred_args(self) -> None:
        node = astroid.parse(
            """
        def fooby(*args, **kwargs):
            pass
        """
        )
        with self.assertNoMessages():
            self.walk(node)


class TestMissingSubmodule(CheckerTestCase):
    CHECKER_CLASS = variables.VariablesChecker

    @staticmethod
    def test_package_all() -> None:

        sys.path.insert(0, REGR_DATA_DIR)
        try:
            linter.check([os.path.join(REGR_DATA_DIR, "package_all")])
            got = linter.reporter.finalize().strip()
            assert got == "E:  3: Undefined variable name 'missing' in __all__"
        finally:
            sys.path.pop(0)
