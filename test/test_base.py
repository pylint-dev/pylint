"""Unittest for the base checker."""

import re

from astroid import test_utils
from pylint.checkers import base
from pylint.testutils import CheckerTestCase, Message


class DocstringTest(CheckerTestCase):
    CHECKER_CLASS = base.DocStringChecker

    def testMissingDocstringModule(self):
        module = test_utils.build_module("")
        with self.assertAddsMessages(Message('missing-docstring', node=module, args=('module',))):
            self.checker.visit_module(module)

    def testEmptyDocstringModule(self):
        module = test_utils.build_module("''''''")
        with self.assertAddsMessages(Message('empty-docstring', node=module, args=('module',))):
            self.checker.visit_module(module)

    def testEmptyDocstringFunction(self):
        func = test_utils.extract_node("""
        def func(tion):
           pass""")
        with self.assertAddsMessages(Message('missing-docstring', node=func, args=('function',))):
            self.checker.visit_function(func)

    def testShortFunctionNoDocstring(self):
        self.checker.config.docstring_min_length = 2
        func = test_utils.extract_node("""
        def func(tion):
           pass""")
        with self.assertNoMessages():
            self.checker.visit_function(func)

    def testFunctionNoDocstringByName(self):
        self.checker.config.docstring_min_length = 2
        func = test_utils.extract_node("""
        def __fun__(tion):
           pass""")
        with self.assertNoMessages():
            self.checker.visit_function(func)

    def testClassNoDocstring(self):
        klass = test_utils.extract_node("""
        class Klass(object):
           pass""")
        with self.assertAddsMessages(Message('missing-docstring', node=klass, args=('class',))):
            self.checker.visit_class(klass)


class NameCheckerTest(CheckerTestCase):
    CHECKER_CLASS = base.NameChecker
    CONFIG = {
        'bad_names': set(),
        }

    def testPropertyNames(self):
        # If a method is annotated with @property, it's name should
        # match the attr regex. Since by default the attribute regex is the same
        # as the method regex, we override it here.
        self.checker.config.attr_rgx = re.compile('[A-Z]+')
        methods = test_utils.extract_node("""
        import abc

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
        """)
        with self.assertNoMessages():
            self.checker.visit_function(methods[0])
            self.checker.visit_function(methods[2])
        with self.assertAddsMessages(Message('invalid-name', node=methods[1],
                                             args=('attribute', 'bar'))):
            self.checker.visit_function(methods[1])

    def testPropertySetters(self):
        self.checker.config.attr_rgx = re.compile('[A-Z]+')
        method = test_utils.extract_node("""
        class FooClass(object):
          @property
          def foo(self): pass

          @foo.setter
          def FOOSETTER(self): #@
             pass
        """)
        with self.assertNoMessages():
            self.checker.visit_function(method)

    def testModuleLevelNames(self):
        assign = test_utils.extract_node("""
        import collections
        Class = collections.namedtuple("a", ("b", "c")) #@
        """)
        with self.assertNoMessages():
            self.checker.visit_assname(assign.targets[0])

        assign = test_utils.extract_node("""
        class ClassA(object):
            pass
        ClassB = ClassA
        """)
        with self.assertNoMessages():
            self.checker.visit_assname(assign.targets[0])

        module = test_utils.build_module("""
        def A():
          return 1, 2, 3
        CONSTA, CONSTB, CONSTC = A()
        CONSTD = A()""")
        with self.assertNoMessages():
            self.checker.visit_assname(module.body[1].targets[0].elts[0])
            self.checker.visit_assname(module.body[2].targets[0])

        assign = test_utils.extract_node("""
        CONST = "12 34 ".rstrip().split()""")
        with self.assertNoMessages():
            self.checker.visit_assname(assign.targets[0])


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
