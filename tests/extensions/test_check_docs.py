# Copyright (c) 2014-2015 Bruno Daniel <bruno.daniel@blue-yonder.com>
# Copyright (c) 2015-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016-2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2016 Glenn Matthews <glenn@e-dad.net>
# Copyright (c) 2016 Glenn Matthews <glmatthe@cisco.com>
# Copyright (c) 2017, 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2017 Mitar <mitar.github@tnode.com>
# Copyright (c) 2017 John Paraskevopoulos <io.paraskev@gmail.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2018 Adrian Chirieac <chirieacam@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2020 Luigi <luigi.cristofolini@q-ctrl.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Konstantina Saketou <56515303+ksaketou@users.noreply.github.com>
# Copyright (c) 2021 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Logan Miller <14319179+komodo472@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Unit tests for the pylint checkers in :mod:`pylint.extensions.check_docs`,
in particular the parameter documentation checker `DocstringChecker`
"""


import re

import astroid
from astroid import nodes

from pylint.extensions.docparams import DocstringParameterChecker
from pylint.testutils import CheckerTestCase, MessageTest, set_config
from pylint.testutils.decorator import set_config_directly


class TestParamDocChecker(CheckerTestCase):
    """Tests for pylint_plugin.ParamDocChecker"""

    CHECKER_CLASS = DocstringParameterChecker
    CONFIG = {
        "accept_no_param_doc": False,
        "no_docstring_rgx": re.compile("^$"),
        "docstring_min_length": -1,
    }

    @set_config(accept_no_param_doc=True)
    def test_tolerate_no_param_documentation_at_all(self) -> None:
        """Example of a function with no parameter documentation at all

        No error message is emitted.
        """
        node = astroid.extract_node(
            """
        def function_foo(x, y):
            '''docstring ...

            missing parameter documentation'''
            pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_don_t_tolerate_no_param_documentation_at_all(self) -> None:
        """Example of a function with no parameter documentation at all

        Missing documentation error message is emitted.
        """
        node = astroid.extract_node(
            """
        def function_foo(x, y):
            '''docstring ...

            missing parameter documentation'''
            pass
        """
        )
        with self.assertAddsMessages(
            MessageTest(msg_id="missing-any-param-doc", node=node, args=(node.name)),
        ):
            self.checker.visit_functiondef(node)

    def test_see_tolerate_no_param_documentation_at_all(self) -> None:
        """Example for the usage of "For the parameters, see"
        to suppress missing-param warnings.
        """
        node = astroid.extract_node(
            """
        def function_foo(x, y):
            '''docstring ...

            For the parameters, see :func:`blah`
            '''
            pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def _visit_methods_of_class(self, node: nodes.ClassDef) -> None:
        """Visit all methods of a class node

        :param node: class node
        :type node: :class:`nodes.Class`
        """
        for body_item in node.body:
            if isinstance(body_item, nodes.FunctionDef) and hasattr(body_item, "name"):
                self.checker.visit_functiondef(body_item)

    def test_see_sentence_for_constr_params_in_class(self) -> None:
        """Example usage of "For the parameters, see" in class docstring"""
        node = astroid.extract_node(
            """
        class ClassFoo(object):
            '''docstring foo

            For the parameters, see :func:`bla`
            '''

            def __init__(self, x, y):
                '''init'''
                pass

        """
        )
        with self.assertNoMessages():
            self._visit_methods_of_class(node)

    def test_see_sentence_for_constr_params_in_init(self) -> None:
        """Example usage of "For the parameters, see" in init docstring"""
        node = astroid.extract_node(
            """
        class ClassFoo(object):
            '''foo'''

            def __init__(self, x, y):
                '''docstring foo constructor

                For the parameters, see :func:`bla`
                '''
                pass

        """
        )
        with self.assertNoMessages():
            self._visit_methods_of_class(node)

    def test_kwonlyargs_are_taken_in_account(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(arg, *, kwonly, missing_kwonly):
            """The docstring

            :param int arg: The argument.
            :param bool kwonly: A keyword-arg.
            """
        '''
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-param-doc", node=node, args=("missing_kwonly",)
            ),
            MessageTest(msg_id="missing-type-doc", node=node, args=("missing_kwonly",)),
        ):
            self.checker.visit_functiondef(node)

    def test_finds_short_name_exception(self) -> None:
        node = astroid.extract_node(
            '''
        from fake_package import BadError

        def do_something(): #@
            """Do something.

            Raises:
                ~fake_package.exceptions.BadError: When something bad happened.
            """
            raise BadError("A bad thing happened.")
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    @set_config_directly(no_docstring_rgx=re.compile(r"^_(?!_).*$"))
    def test_skip_no_docstring_rgx(self) -> None:
        """Example of a function that matches the default 'no-docstring-rgx' config option

        No error message is emitted.
        """
        node = astroid.extract_node(
            """
        def _private_function_foo(x, y):
            '''docstring ...

            missing parameter documentation'''
            pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_all_docstring_rgx(self) -> None:
        """Function that matches "check all functions" 'no-docstring-rgx' config option
        No error message is emitted.
        """
        node = astroid.extract_node(
            """
        #pylint disable=missing-module-docstring, too-few-public-methods,
        class MyClass:
            def __init__(self, my_param: int) -> None:
                '''
                My init docstring
                :param my_param: My first param
                '''
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node.body[0])

    def test_fail_empty_docstring_rgx(self) -> None:
        """Function that matches "check all functions" 'no-docstring-rgx' config option
        An error message is emitted.
        """
        node = astroid.extract_node(
            """
        #pylint disable=missing-module-docstring, too-few-public-methods,
        class MyClass:
            def __init__(self, my_param: int) -> None:
                '''
                My init docstring
                '''
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-param-doc", node=node.body[0], args=("my_param",)
            ),
        ):
            self.checker.visit_functiondef(node.body[0])

    @set_config_directly(no_docstring_rgx=re.compile("^(?!__init__$)_"))
    def test_fail_docparams_check_init(self) -> None:
        """Check that __init__ is checked correctly, but other private methods aren't"""
        node = astroid.extract_node(
            """
        #pylint disable=missing-module-docstring, too-few-public-methods,
        class MyClass:
            def __init__(self, my_param: int) -> None:
                '''
                My init docstring
                '''

            def _private_method(self, my_param: int) -> None:
                '''
                My private method
                '''
        """
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="missing-param-doc", node=node.body[0], args=("my_param",)
            )
        ):
            self.checker.visit_functiondef(node.body[0])

    @set_config_directly(no_docstring_rgx=re.compile(""))
    def test_no_docstring_rgx(self) -> None:
        """Function that matches "check no functions" 'no-docstring-rgx' config option
        No error message is emitted.
        """
        node = astroid.extract_node(
            """
        #pylint disable=missing-module-docstring, too-few-public-methods,
        class MyClass:
            def __init__(self, my_param: int) -> None:
                '''
                My init docstring
                '''
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node.body[0])

    @set_config_directly(docstring_min_length=3)
    def test_skip_docstring_min_length(self) -> None:
        """Example of a function that is less than 'docstring-min-length' config option

        No error message is emitted.
        """
        node = astroid.extract_node(
            """
        def function_foo(x, y):
            '''function is too short and is missing parameter documentation'''
            pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)
