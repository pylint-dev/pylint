# Copyright (c) 2013-2015 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2015-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Dmitry Pribysh <dmand@yandex.ru>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2016 Yannack <yannack@users.noreply.github.com>
# Copyright (c) 2017, 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2017, 2019 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2017 ttenhoeve-aa <ttenhoeve@appannie.com>
# Copyright (c) 2017 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2018 Fureigh <fureigh@users.noreply.github.com>
# Copyright (c) 2018 glmdgrielson <32415403+glmdgrielson@users.noreply.github.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020-2021 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 ethan-leba <ethanleba5@gmail.com>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2020 bernie gray <bfgray3@users.noreply.github.com>
# Copyright (c) 2021 Or Bahari <orbahari@mail.tau.ac.il>
# Copyright (c) 2021 David Gilman <davidgilman1@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unittest for the base checker."""

import re
import sys
import unittest
from typing import Dict, Type

import astroid

from pylint.checkers import BaseChecker, base
from pylint.testutils import CheckerTestCase, Message, set_config


class TestDocstring(CheckerTestCase):
    CHECKER_CLASS: Type = base.DocStringChecker

    def test_missing_docstring_module(self):
        module = astroid.parse("something")
        message = Message("missing-module-docstring", node=module)
        with self.assertAddsMessages(message):
            self.checker.visit_module(module)

    def test_missing_docstring_empty_module(self):
        module = astroid.parse("")
        with self.assertNoMessages():
            self.checker.visit_module(module)

    def test_empty_docstring_module(self):
        module = astroid.parse("''''''")
        message = Message("empty-docstring", node=module, args=("module",))
        with self.assertAddsMessages(message):
            self.checker.visit_module(module)

    def test_empty_docstring_function(self):
        func = astroid.extract_node(
            """
        def func(tion):
           pass"""
        )
        message = Message("missing-function-docstring", node=func)
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(func)

    @set_config(docstring_min_length=2)
    def test_short_function_no_docstring(self):
        func = astroid.extract_node(
            """
        def func(tion):
           pass"""
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(func)

    @set_config(docstring_min_length=2)
    def test_long_function_no_docstring(self):
        func = astroid.extract_node(
            """
        def func(tion):
            pass
            pass
           """
        )
        message = Message("missing-function-docstring", node=func)
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(func)

    @set_config(docstring_min_length=2)
    def test_long_function_nested_statements_no_docstring(self):
        func = astroid.extract_node(
            """
        def func(tion):
            try:
                pass
            except:
                pass
           """
        )
        message = Message("missing-function-docstring", node=func)
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(func)

    @set_config(docstring_min_length=2)
    def test_function_no_docstring_by_name(self):
        func = astroid.extract_node(
            """
        def __fun__(tion):
           pass"""
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(func)

    def test_class_no_docstring(self):
        klass = astroid.extract_node(
            """
        class Klass(object):
           pass"""
        )
        message = Message("missing-class-docstring", node=klass)
        with self.assertAddsMessages(message):
            self.checker.visit_classdef(klass)

    def test_inner_function_no_docstring(self):
        func = astroid.extract_node(
            """
        def func(tion):
            \"""Documented\"""
            def inner(fun):
                # Not documented
                pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(func)


class TestNameChecker(CheckerTestCase):
    CHECKER_CLASS: Type = base.NameChecker
    CONFIG: Dict = {"bad_names": set()}

    @set_config(
        attr_rgx=re.compile("[A-Z]+"),
        property_classes=("abc.abstractproperty", ".custom_prop"),
    )
    def test_property_names(self):
        # If a method is annotated with @property, its name should
        # match the attr regex. Since by default the attribute regex is the same
        # as the method regex, we override it here.
        methods = astroid.extract_node(
            """
        import abc

        def custom_prop(f):
          return property(f)

        class FooClass(object):
          @property
          def FOO(self): #@
            pass

          @property
          def bar(self): #@
            pass

          @abc.abstractproperty
          def BAZ(self): #@
            pass

          @custom_prop
          def QUX(self): #@
            pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(methods[0])
            self.checker.visit_functiondef(methods[2])
            self.checker.visit_functiondef(methods[3])
        with self.assertAddsMessages(
            Message(
                "invalid-name",
                node=methods[1],
                args=("Attribute", "bar", "'[A-Z]+' pattern"),
            )
        ):
            self.checker.visit_functiondef(methods[1])

    @set_config(attr_rgx=re.compile("[A-Z]+"))
    def test_property_setters(self):
        method = astroid.extract_node(
            """
        class FooClass(object):
          @property
          def foo(self): pass

          @foo.setter
          def FOOSETTER(self): #@
             pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(method)

    def test_module_level_names(self):
        assign = astroid.extract_node(
            """
        import collections
        Class = collections.namedtuple("a", ("b", "c")) #@
        """
        )
        with self.assertNoMessages():
            self.checker.visit_assignname(assign.targets[0])

        assign = astroid.extract_node(
            """
        class ClassA(object):
            pass
        ClassB = ClassA
        """
        )
        with self.assertNoMessages():
            self.checker.visit_assignname(assign.targets[0])

        module = astroid.parse(
            """
        def A():
          return 1, 2, 3
        CONSTA, CONSTB, CONSTC = A()
        CONSTD = A()"""
        )
        with self.assertNoMessages():
            self.checker.visit_assignname(module.body[1].targets[0].elts[0])
            self.checker.visit_assignname(module.body[2].targets[0])

        assign = astroid.extract_node(
            """
        CONST = "12 34 ".rstrip().split()"""
        )
        with self.assertNoMessages():
            self.checker.visit_assignname(assign.targets[0])

    @unittest.skipIf(sys.version_info >= (3, 7), reason="Needs Python 3.6 or earlier")
    @set_config(const_rgx=re.compile(".+"))
    @set_config(function_rgx=re.compile(".+"))
    @set_config(class_rgx=re.compile(".+"))
    def test_assign_to_new_keyword_py3(self):
        ast = astroid.extract_node(
            """
        async = "foo"  #@
        await = "bar"  #@
        def async():   #@
            pass
        class async:   #@
            pass
        """
        )
        with self.assertAddsMessages(
            Message(
                msg_id="assign-to-new-keyword",
                node=ast[0].targets[0],
                args=("async", "3.7"),
            )
        ):
            self.checker.visit_assignname(ast[0].targets[0])
        with self.assertAddsMessages(
            Message(
                msg_id="assign-to-new-keyword",
                node=ast[1].targets[0],
                args=("await", "3.7"),
            )
        ):
            self.checker.visit_assignname(ast[1].targets[0])
        with self.assertAddsMessages(
            Message(msg_id="assign-to-new-keyword", node=ast[2], args=("async", "3.7"))
        ):
            self.checker.visit_functiondef(ast[2])
        with self.assertAddsMessages(
            Message(msg_id="assign-to-new-keyword", node=ast[3], args=("async", "3.7"))
        ):
            self.checker.visit_classdef(ast[3])


class TestMultiNamingStyle(CheckerTestCase):
    CHECKER_CLASS = base.NameChecker

    MULTI_STYLE_RE = re.compile("(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$")

    @set_config(class_rgx=MULTI_STYLE_RE)
    def test_multi_name_detection_majority(self):
        classes = astroid.extract_node(
            """
        class classb(object): #@
            pass
        class CLASSA(object): #@
            pass
        class CLASSC(object): #@
            pass
        """
        )
        message = Message(
            "invalid-name",
            node=classes[0],
            args=("Class", "classb", "'(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$' pattern"),
        )
        with self.assertAddsMessages(message):
            cls = None
            for cls in classes:
                self.checker.visit_classdef(cls)
            if cls:
                self.checker.leave_module(cls.root)

    @set_config(class_rgx=MULTI_STYLE_RE)
    def test_multi_name_detection_first_invalid(self):
        classes = astroid.extract_node(
            """
        class class_a(object): #@
            pass
        class classb(object): #@
            pass
        class CLASSC(object): #@
            pass
        """
        )
        messages = [
            Message(
                "invalid-name",
                node=classes[0],
                args=(
                    "Class",
                    "class_a",
                    "'(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$' pattern",
                ),
            ),
            Message(
                "invalid-name",
                node=classes[2],
                args=(
                    "Class",
                    "CLASSC",
                    "'(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$' pattern",
                ),
            ),
        ]
        with self.assertAddsMessages(*messages):
            cls = None
            for cls in classes:
                self.checker.visit_classdef(cls)
            if cls:
                self.checker.leave_module(cls.root)

    @set_config(
        method_rgx=MULTI_STYLE_RE,
        function_rgx=MULTI_STYLE_RE,
        name_group=("function:method",),
    )
    def test_multi_name_detection_group(self):
        function_defs = astroid.extract_node(
            """
        class First(object):
            def func(self): #@
                pass

        def FUNC(): #@
            pass
        """,
            module_name="test",
        )
        message = Message(
            "invalid-name",
            node=function_defs[1],
            args=("Function", "FUNC", "'(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$' pattern"),
        )
        with self.assertAddsMessages(message):
            func = None
            for func in function_defs:
                self.checker.visit_functiondef(func)
            if func:
                self.checker.leave_module(func.root)

    @set_config(
        function_rgx=re.compile("(?:(?P<ignore>FOO)|(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$")
    )
    def test_multi_name_detection_exempt(self):
        function_defs = astroid.extract_node(
            """
        def FOO(): #@
            pass
        def lower(): #@
            pass
        def FOO(): #@
            pass
        def UPPER(): #@
            pass
        """
        )
        message = Message(
            "invalid-name",
            node=function_defs[3],
            args=(
                "Function",
                "UPPER",
                "'(?:(?P<ignore>FOO)|(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$' pattern",
            ),
        )
        with self.assertAddsMessages(message):
            func = None
            for func in function_defs:
                self.checker.visit_functiondef(func)
            if func:
                self.checker.leave_module(func.root)


class TestComparison(CheckerTestCase):
    CHECKER_CLASS = base.ComparisonChecker

    def test_comparison(self):
        node = astroid.extract_node("foo == True")
        message = Message(
            "singleton-comparison",
            node=node,
            args=(
                "'foo == True'",
                "'foo is True' if checking for the singleton value True, or 'bool(foo)' if testing for truthiness",
            ),
        )
        with self.assertAddsMessages(message):
            self.checker.visit_compare(node)

        node = astroid.extract_node("foo == False")
        message = Message(
            "singleton-comparison",
            node=node,
            args=(
                "'foo == False'",
                "'foo is False' if checking for the singleton value False, or 'not foo' if testing for falsiness",
            ),
        )
        with self.assertAddsMessages(message):
            self.checker.visit_compare(node)

        node = astroid.extract_node("foo == None")
        message = Message(
            "singleton-comparison", node=node, args=("'foo == None'", "'foo is None'")
        )
        with self.assertAddsMessages(message):
            self.checker.visit_compare(node)

        node = astroid.extract_node("foo is float('nan')")
        message = Message(
            "nan-comparison",
            node=node,
            args=("'foo is float('nan')'", "'math.isnan(foo)'"),
        )
        with self.assertAddsMessages(message):
            self.checker.visit_compare(node)

        node = astroid.extract_node(
            """
                                import numpy
                                foo != numpy.NaN
                                """
        )
        message = Message(
            "nan-comparison",
            node=node,
            args=("'foo != numpy.NaN'", "'not math.isnan(foo)'"),
        )
        with self.assertAddsMessages(message):
            self.checker.visit_compare(node)

        node = astroid.extract_node(
            """
                                import numpy as nmp
                                foo is not nmp.NaN
                                """
        )
        message = Message(
            "nan-comparison",
            node=node,
            args=("'foo is not nmp.NaN'", "'not math.isnan(foo)'"),
        )
        with self.assertAddsMessages(message):
            self.checker.visit_compare(node)

        node = astroid.extract_node("True == foo")
        messages = (
            Message("misplaced-comparison-constant", node=node, args=("foo == True",)),
            Message(
                "singleton-comparison",
                node=node,
                args=(
                    "'True == foo'",
                    "'True is foo' if checking for the singleton value True, or 'bool(foo)' if testing for truthiness",
                ),
            ),
        )
        with self.assertAddsMessages(*messages):
            self.checker.visit_compare(node)

        node = astroid.extract_node("False == foo")
        messages = (
            Message("misplaced-comparison-constant", node=node, args=("foo == False",)),
            Message(
                "singleton-comparison",
                node=node,
                args=(
                    "'False == foo'",
                    "'False is foo' if checking for the singleton value False, or 'not foo' if testing for falsiness",
                ),
            ),
        )
        with self.assertAddsMessages(*messages):
            self.checker.visit_compare(node)

        node = astroid.extract_node("None == foo")
        messages = (
            Message("misplaced-comparison-constant", node=node, args=("foo == None",)),
            Message(
                "singleton-comparison",
                node=node,
                args=("'None == foo'", "'None is foo'"),
            ),
        )
        with self.assertAddsMessages(*messages):
            self.checker.visit_compare(node)


class TestNamePresets(unittest.TestCase):
    SNAKE_CASE_NAMES = {"tést_snake_case", "test_snake_case11", "test_https_200"}
    CAMEL_CASE_NAMES = {"téstCamelCase", "testCamelCase11", "testHTTP200"}
    UPPER_CASE_NAMES = {"TÉST_UPPER_CASE", "TEST_UPPER_CASE11", "TEST_HTTP_200"}
    PASCAL_CASE_NAMES = {"TéstPascalCase", "TestPascalCase11", "TestHTTP200"}
    ALL_NAMES = (
        SNAKE_CASE_NAMES | CAMEL_CASE_NAMES | UPPER_CASE_NAMES | PASCAL_CASE_NAMES
    )

    def _test_name_is_correct_for_all_name_types(self, naming_style, name):
        for name_type in base.KNOWN_NAME_TYPES:
            self._test_is_correct(naming_style, name, name_type)

    def _test_name_is_incorrect_for_all_name_types(self, naming_style, name):
        for name_type in base.KNOWN_NAME_TYPES:
            self._test_is_incorrect(naming_style, name, name_type)

    def _test_should_always_pass(self, naming_style):
        always_pass_data = [
            ("__add__", "method"),
            ("__set_name__", "method"),
            ("__version__", "const"),
            ("__author__", "const"),
        ]
        for name, name_type in always_pass_data:
            self._test_is_correct(naming_style, name, name_type)

    @staticmethod
    def _test_is_correct(naming_style, name, name_type):
        rgx = naming_style.get_regex(name_type)
        fail = f"{name!r} does not match pattern {rgx!r} (style: {naming_style}, type: {name_type})"
        assert rgx.match(name), fail

    @staticmethod
    def _test_is_incorrect(naming_style, name, name_type):
        rgx = naming_style.get_regex(name_type)
        fail = f"{name!r} not match pattern {rgx!r} (style: {naming_style}, type: {name_type})"
        assert not rgx.match(name), fail

    def test_snake_case(self):
        naming_style = base.SnakeCaseStyle

        for name in self.SNAKE_CASE_NAMES:
            self._test_name_is_correct_for_all_name_types(naming_style, name)
        for name in self.ALL_NAMES - self.SNAKE_CASE_NAMES:
            self._test_name_is_incorrect_for_all_name_types(naming_style, name)

        self._test_should_always_pass(naming_style)

    def test_camel_case(self):
        naming_style = base.CamelCaseStyle

        for name in self.CAMEL_CASE_NAMES:
            self._test_name_is_correct_for_all_name_types(naming_style, name)
        for name in self.ALL_NAMES - self.CAMEL_CASE_NAMES:
            self._test_name_is_incorrect_for_all_name_types(naming_style, name)

        self._test_should_always_pass(naming_style)

    def test_upper_case(self):
        naming_style = base.UpperCaseStyle

        for name in self.UPPER_CASE_NAMES:
            self._test_name_is_correct_for_all_name_types(naming_style, name)
        for name in self.ALL_NAMES - self.UPPER_CASE_NAMES:
            self._test_name_is_incorrect_for_all_name_types(naming_style, name)
        self._test_name_is_incorrect_for_all_name_types(naming_style, "UPPERcase")

        self._test_should_always_pass(naming_style)

    def test_pascal_case(self):
        naming_style = base.PascalCaseStyle

        for name in self.PASCAL_CASE_NAMES:
            self._test_name_is_correct_for_all_name_types(naming_style, name)
        for name in self.ALL_NAMES - self.PASCAL_CASE_NAMES:
            self._test_name_is_incorrect_for_all_name_types(naming_style, name)

        self._test_should_always_pass(naming_style)


class TestBaseChecker(unittest.TestCase):
    def test_doc(self):
        class OtherBasicChecker(BaseChecker):
            name = "basic"
            msgs = {
                "W0001": (
                    "Basic checker has an example.",
                    "basic-checker-example",
                    "Used nowhere and serves no purpose.",
                )
            }

        class LessBasicChecker(OtherBasicChecker):
            options = (
                (
                    "example-args",
                    {
                        "default": 42,
                        "type": "int",
                        "metavar": "<int>",
                        "help": "Example of integer argument for the checker.",
                    },
                ),
            )

        basic = OtherBasicChecker()
        expected_beginning = """\
Basic checker
~~~~~~~~~~~~~

Verbatim name of the checker is ``basic``.

"""
        expected_middle = """\
Basic checker Options
^^^^^^^^^^^^^^^^^^^^^
:example-args:
  Example of integer argument for the checker.

  Default: ``42``

"""
        expected_end = """\
Basic checker Messages
^^^^^^^^^^^^^^^^^^^^^^
:basic-checker-example (W0001): *Basic checker has an example.*
  Used nowhere and serves no purpose.


"""
        self.assertEqual(str(basic), expected_beginning + expected_end)
        self.assertEqual(repr(basic), "Checker 'basic' (responsible for 'W0001')")
        less_basic = LessBasicChecker()

        self.assertEqual(
            str(less_basic), expected_beginning + expected_middle + expected_end
        )
        self.assertEqual(repr(less_basic), repr(basic))


class TestNoSix(unittest.TestCase):
    @unittest.skip("too many dependencies need six :(")
    def test_no_six(self):
        try:
            has_six = True
        except ImportError:
            has_six = False

        self.assertFalse(has_six, "pylint must be able to run without six")
