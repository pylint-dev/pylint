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

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import os
import re
import sys
from pathlib import Path

import astroid

from pylint.checkers import variables
from pylint.interfaces import UNDEFINED
from pylint.testutils import CheckerTestCase, Message, linter, set_config

REGR_DATA_DIR = str(Path(__file__).parent / ".." / "regrtest_data")


class TestVariablesChecker(CheckerTestCase):

    CHECKER_CLASS = variables.VariablesChecker

    def test_bitbucket_issue_78(self):
        """ Issue 78 report a false positive for unused-module """
        module = astroid.parse(
            """
        from sys import path
        path += ['stuff']
        def func():
            other = 1
            return len(other)
        """
        )
        with self.assertNoMessages():
            self.walk(module)

    @set_config(ignored_modules=("argparse",))
    def test_no_name_in_module_skipped(self):
        """Make sure that 'from ... import ...' does not emit a
        'no-name-in-module' with a module that is configured
        to be ignored.
        """

        node = astroid.extract_node(
            """
        from argparse import THIS_does_not_EXIST
        """
        )
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)

    def test_all_elements_without_parent(self):
        node = astroid.extract_node("__all__ = []")
        node.value.elts.append(astroid.Const("test"))
        root = node.root()
        with self.assertNoMessages():
            self.checker.visit_module(root)
            self.checker.leave_module(root)

    def test_redefined_builtin_ignored(self):
        node = astroid.parse(
            """
        from future.builtins import open
        """
        )
        with self.assertNoMessages():
            self.checker.visit_module(node)

    @set_config(redefining_builtins_modules=("os",))
    def test_redefined_builtin_custom_modules(self):
        node = astroid.parse(
            """
        from os import open
        """
        )
        with self.assertNoMessages():
            self.checker.visit_module(node)

    @set_config(redefining_builtins_modules=("os",))
    def test_redefined_builtin_modname_not_ignored(self):
        node = astroid.parse(
            """
        from future.builtins import open
        """
        )
        with self.assertAddsMessages(
            Message("redefined-builtin", node=node.body[0], args="open")
        ):
            self.checker.visit_module(node)

    @set_config(redefining_builtins_modules=("os",))
    def test_redefined_builtin_in_function(self):
        node = astroid.extract_node(
            """
        def test():
            from os import open
        """
        )
        with self.assertNoMessages():
            self.checker.visit_module(node.root())
            self.checker.visit_functiondef(node)

    def test_unassigned_global(self):
        node = astroid.extract_node(
            """
            def func():
                global sys  #@
                import sys, lala
        """
        )
        msg = Message("global-statement", node=node, confidence=UNDEFINED)
        with self.assertAddsMessages(msg):
            self.checker.visit_global(node)

    def test_listcomp_in_decorator(self):
        """Make sure class attributes in scope for listcomp in decorator.

        https://github.com/PyCQA/pylint/issues/511
        """
        module = astroid.parse(
            """
        def dec(inp):
            def inner(func):
                print(inp)
                return func
            return inner


        class Cls:

            DATA = "foo"

            @dec([x for x in DATA])
            def fun(self):
                pass
        """
        )
        with self.assertNoMessages():
            self.walk(module)

    def test_listcomp_in_ancestors(self):
        """Ensure list comprehensions in base classes are scoped correctly

        https://github.com/PyCQA/pylint/issues/3434
        """
        module = astroid.parse(
            """
        import collections


        l = ["a","b","c"]


        class Foo(collections.namedtuple("Foo",[x+"_foo" for x in l])):
            pass
        """
        )
        with self.assertNoMessages():
            self.walk(module)

    def test_return_type_annotation(self):
        """Make sure class attributes in scope for return type annotations.

        https://github.com/PyCQA/pylint/issues/1976
        """
        module = astroid.parse(
            """
        class MyObject:
            class MyType:
                pass
            def my_method(self) -> MyType:
                pass
        """
        )
        with self.assertNoMessages():
            self.walk(module)


class TestVariablesCheckerWithTearDown(CheckerTestCase):

    CHECKER_CLASS = variables.VariablesChecker

    def setup_method(self):
        super().setup_method()
        self._to_consume_backup = self.checker._to_consume
        self.checker._to_consume = []

    def teardown_method(self):
        self.checker._to_consume = self._to_consume_backup

    @set_config(callbacks=("callback_", "_callback"))
    def test_custom_callback_string(self):
        """ Test the --calbacks option works. """
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
            Message("unused-argument", node=node["abc"], args="abc")
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
            Message("unused-argument", node=node["abc"], args="abc")
        ):
            self.checker.visit_functiondef(node)
            self.checker.leave_functiondef(node)

    @set_config(redefining_builtins_modules=("os",))
    def test_redefined_builtin_modname_not_ignored(self):
        node = astroid.parse(
            """
        from future.builtins import open
        """
        )
        with self.assertAddsMessages(
            Message("redefined-builtin", node=node.body[0], args="open")
        ):
            self.checker.visit_module(node)

    @set_config(redefining_builtins_modules=("os",))
    def test_redefined_builtin_in_function(self):
        node = astroid.extract_node(
            """
        def test():
            from os import open
        """
        )
        with self.assertNoMessages():
            self.checker.visit_module(node.root())
            self.checker.visit_functiondef(node)

    def test_import_as_underscore(self):
        node = astroid.parse(
            """
        import math as _
        """
        )
        with self.assertNoMessages():
            self.walk(node)

    def test_lambda_in_classdef(self):
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

    def test_nested_lambda(self):
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
    def test_ignored_argument_names_no_message(self):
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
    def test_ignored_argument_names_starred_args(self):
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
    def test_package_all():

        sys.path.insert(0, REGR_DATA_DIR)
        try:
            linter.check(os.path.join(REGR_DATA_DIR, "package_all"))
            got = linter.reporter.finalize().strip()
            assert got == "E:  3: Undefined variable name 'missing' in __all__"
        finally:
            sys.path.pop(0)
