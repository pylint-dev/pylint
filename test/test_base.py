"""Unittest for the base checker."""

from astroid import test_utils
from pylint.checkers import base

from pylint.testutils import CheckerTestCase, Message


class DocstringTest(CheckerTestCase):
    CHECKER_CLASS = base.DocStringChecker

    def testMissingDocstringModule(self):
        module = test_utils.build_module("")
        with self.assertAddsMessages(Message('C0111', node=module, args=('module',))):
            self.checker.visit_module(module)

    def testEmptyDocstringModule(self):
        module = test_utils.build_module("''''''")
        with self.assertAddsMessages(Message('C0112', node=module, args=('module',))):
            self.checker.visit_module(module)

    def testEmptyDocstringFunction(self):
        func = test_utils.extract_node("""
        def func(tion):
           pass""")
        with self.assertAddsMessages(Message('C0111', node=func, args=('function',))):
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
        with self.assertAddsMessages(Message('C0111', node=klass, args=('class',))):
            self.checker.visit_class(klass)
