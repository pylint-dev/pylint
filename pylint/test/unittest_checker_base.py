"""Unittest for the base checker."""

import re
import sys
import unittest

import astroid
from astroid import test_utils
from pylint.checkers import base
from pylint.testutils import CheckerTestCase, Message, set_config


def python33_and_newer(test):
    """
    Decorator for any tests that will fail if launched not with Python 3.3+.
    """
    return unittest.skipIf(sys.version_info < (3, 3),
                           'Python 3.2 and older')(test)

class DocstringTest(CheckerTestCase):
    CHECKER_CLASS = base.DocStringChecker

    def test_missing_docstring_module(self):
        module = astroid.parse("something")
        message = Message('missing-docstring', node=module, args=('module',))
        with self.assertAddsMessages(message):
            self.checker.visit_module(module)

    def test_missing_docstring_emtpy_module(self):
        module = astroid.parse("")
        with self.assertNoMessages():
            self.checker.visit_module(module)

    def test_empty_docstring_module(self):
        module = astroid.parse("''''''")
        message = Message('empty-docstring', node=module, args=('module',))
        with self.assertAddsMessages(message):
            self.checker.visit_module(module)

    def test_empty_docstring_function(self):
        func = test_utils.extract_node("""
        def func(tion):
           pass""")
        message = Message('missing-docstring', node=func, args=('function',))
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(func)

    @set_config(docstring_min_length=2)
    def test_short_function_no_docstring(self):
        func = test_utils.extract_node("""
        def func(tion):
           pass""")
        with self.assertNoMessages():
            self.checker.visit_functiondef(func)

    @set_config(docstring_min_length=2)
    def test_function_no_docstring_by_name(self):
        func = test_utils.extract_node("""
        def __fun__(tion):
           pass""")
        with self.assertNoMessages():
            self.checker.visit_functiondef(func)

    def test_class_no_docstring(self):
        klass = test_utils.extract_node("""
        class Klass(object):
           pass""")
        message = Message('missing-docstring', node=klass, args=('class',))
        with self.assertAddsMessages(message):
            self.checker.visit_classdef(klass)


class NameCheckerTest(CheckerTestCase):
    CHECKER_CLASS = base.NameChecker
    CONFIG = {
        'bad_names': set(),
        }

    @set_config(include_naming_hint=True)
    def test_naming_hint(self):
        const = test_utils.extract_node("""
        const = "CONSTANT" #@
        """)
        message = Message(
           'invalid-name', node=const.targets[0],
           args=('constant', 'const',
                 ' (hint: (([A-Z_][A-Z0-9_]*)|(__.*__))$)'))
        with self.assertAddsMessages(message):
            self.checker.visit_assignname(const.targets[0])

    @set_config(include_naming_hint=True, const_name_hint='CONSTANT')
    def test_naming_hint_configured_hint(self):
        const = test_utils.extract_node("""
        const = "CONSTANT" #@
        """)
        with self.assertAddsMessages(
            Message('invalid-name', node=const.targets[0],
                    args=('constant', 'const', ' (hint: CONSTANT)'))):
            self.checker.visit_assignname(const.targets[0])

    @set_config(attr_rgx=re.compile('[A-Z]+'))
    def test_property_names(self):
        # If a method is annotated with @property, it's name should
        # match the attr regex. Since by default the attribute regex is the same
        # as the method regex, we override it here.
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
            self.checker.visit_functiondef(methods[0])
            self.checker.visit_functiondef(methods[2])
        with self.assertAddsMessages(Message('invalid-name', node=methods[1],
                                             args=('attribute', 'bar', ''))):
            self.checker.visit_functiondef(methods[1])

    @set_config(attr_rgx=re.compile('[A-Z]+'))
    def test_property_setters(self):
        method = test_utils.extract_node("""
        class FooClass(object):
          @property
          def foo(self): pass

          @foo.setter
          def FOOSETTER(self): #@
             pass
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(method)

    def test_module_level_names(self):
        assign = test_utils.extract_node("""
        import collections
        Class = collections.namedtuple("a", ("b", "c")) #@
        """)
        with self.assertNoMessages():
            self.checker.visit_assignname(assign.targets[0])

        assign = test_utils.extract_node("""
        class ClassA(object):
            pass
        ClassB = ClassA
        """)
        with self.assertNoMessages():
            self.checker.visit_assignname(assign.targets[0])

        module = astroid.parse("""
        def A():
          return 1, 2, 3
        CONSTA, CONSTB, CONSTC = A()
        CONSTD = A()""")
        with self.assertNoMessages():
            self.checker.visit_assignname(module.body[1].targets[0].elts[0])
            self.checker.visit_assignname(module.body[2].targets[0])

        assign = test_utils.extract_node("""
        CONST = "12 34 ".rstrip().split()""")
        with self.assertNoMessages():
            self.checker.visit_assignname(assign.targets[0])


class MultiNamingStyleTest(CheckerTestCase):
    CHECKER_CLASS = base.NameChecker

    MULTI_STYLE_RE = re.compile('(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$')

    @set_config(class_rgx=MULTI_STYLE_RE)
    def test_multi_name_detection_majority(self):
        classes = test_utils.extract_node("""
        class classb(object): #@
            pass
        class CLASSA(object): #@
            pass
        class CLASSC(object): #@
            pass
        """)
        message = Message('invalid-name',
                          node=classes[0],
                          args=('class', 'classb', ''))
        with self.assertAddsMessages(message):
            for cls in classes:
                self.checker.visit_classdef(cls)
            self.checker.leave_module(cls.root)

    @set_config(class_rgx=MULTI_STYLE_RE)
    def test_multi_name_detection_first_invalid(self):
        classes = test_utils.extract_node("""
        class class_a(object): #@
            pass
        class classb(object): #@
            pass
        class CLASSC(object): #@
            pass
        """)
        messages = [
            Message('invalid-name', node=classes[0],
                    args=('class', 'class_a', '')),
            Message('invalid-name', node=classes[2],
                    args=('class', 'CLASSC', ''))
        ]
        with self.assertAddsMessages(*messages):
            for cls in classes:
                self.checker.visit_classdef(cls)
            self.checker.leave_module(cls.root)

    @set_config(method_rgx=MULTI_STYLE_RE,
                function_rgx=MULTI_STYLE_RE,
                name_group=('function:method',))
    def test_multi_name_detection_group(self):
        function_defs = test_utils.extract_node("""
        class First(object):
            def func(self): #@
                pass

        def FUNC(): #@
            pass
        """, module_name='test')
        message = Message('invalid-name', node=function_defs[1],
                          args=('function', 'FUNC', ''))
        with self.assertAddsMessages(message):
            for func in function_defs:
                self.checker.visit_functiondef(func)
            self.checker.leave_module(func.root)

    @set_config(function_rgx=re.compile('(?:(?P<ignore>FOO)|(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$'))
    def test_multi_name_detection_exempt(self):
        function_defs = test_utils.extract_node("""
        def FOO(): #@
            pass
        def lower(): #@
            pass
        def FOO(): #@
            pass
        def UPPER(): #@
            pass
        """)
        message = Message('invalid-name', node=function_defs[3],
                          args=('function', 'UPPER', ''))
        with self.assertAddsMessages(message):
            for func in function_defs:
                self.checker.visit_functiondef(func)
            self.checker.leave_module(func.root)

class ComparisonTest(CheckerTestCase):
    CHECKER_CLASS = base.ComparisonChecker

    def test_singleton_comparison(self):
        node = test_utils.extract_node("foo == True")
        message = Message('singleton-comparison',
                          node=node,
                          args=(True, "just 'expr' or 'expr is True'"))
        with self.assertAddsMessages(message):
            self.checker.visit_compare(node)

        node = test_utils.extract_node("foo == False")
        message = Message('singleton-comparison',
                          node=node,
                          args=(False, "'not expr' or 'expr is False'"))
        with self.assertAddsMessages(message):
            self.checker.visit_compare(node)

        node = test_utils.extract_node("foo == None")
        message = Message('singleton-comparison',
                          node=node,
                          args=(None, "'expr is None'"))
        with self.assertAddsMessages(message):
            self.checker.visit_compare(node)

        node = test_utils.extract_node("True == foo")
        message = Message('singleton-comparison',
                          node=node,
                          args=(True, "just 'expr' or 'expr is True'"))
        with self.assertAddsMessages(message):
            self.checker.visit_compare(node)

        node = test_utils.extract_node("False == foo")
        message = Message('singleton-comparison',
                          node=node,
                          args=(False, "'not expr' or 'expr is False'"))
        with self.assertAddsMessages(message):
            self.checker.visit_compare(node)

        node = test_utils.extract_node("None == foo")
        message = Message('singleton-comparison',
                          node=node,
                          args=(None, "'expr is None'"))
        with self.assertAddsMessages(message):
            self.checker.visit_compare(node)


class IterableTest(CheckerTestCase):
    CHECKER_CLASS = base.IterableChecker

    def test_non_iterable_in_for(self):
        node = test_utils.extract_node("""
        for i in 42:
            print(i)
        """)
        message = Message('not-an-iterable', node=node, args='42')
        with self.assertAddsMessages(message):
            self.checker.visit_for(node)

        node = test_utils.extract_node("""
        for i in [1,2,3]:
            print(i)
        """)
        with self.assertNoMessages():
            self.checker.visit_for(node)

        node = test_utils.extract_node("""
        def count():
            i = 0
            while True:
                yield i
                i += 1

        for i in count():
            print(i)
        """)
        with self.assertNoMessages():
            self.walk(node.root())

        node = test_utils.extract_node("""
        for i in "aeiou":
            print(i)
        """)
        with self.assertNoMessages():
            self.checker.visit_for(node)

    @python33_and_newer
    def test_non_iterable_in_yield_from(self):
        node = test_utils.extract_node("""
        yield from 42
        """)
        message = Message('not-an-iterable', node=node, args='42')
        with self.assertAddsMessages(message):
            self.checker.visit_yieldfrom(node)

        node = test_utils.extract_node("""
        yield from [1,2,3]
        """)
        with self.assertNoMessages():
            self.checker.visit_yieldfrom(node)

    def test_non_iterable_in_funcall_starargs(self):
        node = test_utils.extract_node("""
        foo(*123)
        """)
        message = Message('not-an-iterable', node=node, args='123')
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

        node = test_utils.extract_node("""
        stuff = [1,2,3]
        foo(*stuff)
        """)
        with self.assertNoMessages():
            self.walk(node.root())

    def test_non_mapping_in_funcall_kwargs(self):
        node = test_utils.extract_node("""
        foo(**123)
        """)
        message = Message('not-a-mapping', node=node, args='123')
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

        node = test_utils.extract_node("""
        foo(**retdict())
        """)
        with self.assertNoMessages():
            self.walk(node.root())

    def test_non_iterable_in_listcomp(self):
        node = test_utils.extract_node("""
        [x ** 2 for x in 10]
        """)
        message = Message('not-an-iterable', node=node, args='10')
        with self.assertAddsMessages(message):
            self.checker.visit_listcomp(node)

        node = test_utils.extract_node("""
        [x ** 2 for x in range(10)]
        """)
        with self.assertNoMessages():
            self.checker.visit_listcomp(node)

    def test_non_iterable_in_dictcomp(self):
        node = test_utils.extract_node("""
        {x: chr(x) for x in 256}
        """)
        message = Message('not-an-iterable', node=node, args='256')
        with self.assertAddsMessages(message):
            self.checker.visit_dictcomp(node)

        node = test_utils.extract_node("""
        {ord(x): x for x in "aoeui"}
        """)
        with self.assertNoMessages():
            self.checker.visit_dictcomp(node)

    def test_non_iterable_in_setcomp(self):
        node = test_utils.extract_node("""
        {2 ** x for x in 10}
        """)
        message = Message('not-an-iterable', node=node, args='10')
        with self.assertAddsMessages(message):
            self.checker.visit_setcomp(node)

        node = test_utils.extract_node("""
        {2 ** x for x in range(10)}
        """)
        with self.assertNoMessages():
            self.checker.visit_setcomp(node)

    def test_non_iterable_in_generator(self):
        node = test_utils.extract_node("__(x for x in 123)")
        message = Message('not-an-iterable', node=node, args='123')
        with self.assertAddsMessages(message):
            self.walk(node.root())

        node = test_utils.extract_node("__(chr(x) for x in range(25))")
        with self.assertNoMessages():
            self.walk(node.root())


if __name__ == '__main__':
    unittest.main()
