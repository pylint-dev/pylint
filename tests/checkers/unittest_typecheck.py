# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014 Holger Peters <email@holger-peters.de>
# Copyright (c) 2015-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Dmitry Pribysh <dmand@yandex.ru>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2016 Filipe Brandenburger <filbranden@google.com>
# Copyright (c) 2017 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2018 Bryce Guinta <bryce.paul.guinta@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2019 Martin Vielsmaier <martin.vielsmaier@gmail.com>
# Copyright (c) 2019 Federico Bond <federicobond@gmail.com>
# Copyright (c) 2020 Julien Palard <julien@palard.fr>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Damien Baty <damien.baty@polyconseil.fr>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2021 David Gilman <davidgilman1@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import astroid
import pytest

from pylint.checkers import typecheck
from pylint.interfaces import UNDEFINED
from pylint.testutils import CheckerTestCase, Message, set_config

try:
    from coverage import tracer as _  # pylint: disable=unused-import

    C_EXTENTIONS_AVAILABLE = True
except ImportError:
    _ = None
    C_EXTENTIONS_AVAILABLE = False

needs_c_extension = pytest.mark.skipif(
    not C_EXTENTIONS_AVAILABLE, reason="Requires coverage (source of C-extension)"
)


class TestTypeChecker(CheckerTestCase):
    "Tests for pylint.checkers.typecheck"
    CHECKER_CLASS = typecheck.TypeChecker

    def test_no_member_in_getattr(self):
        """Make sure that a module attribute access is checked by pylint."""

        node = astroid.extract_node(
            """
        import optparse
        optparse.THIS_does_not_EXIST
        """
        )
        with self.assertAddsMessages(
            Message(
                "no-member",
                node=node,
                args=("Module", "optparse", "THIS_does_not_EXIST", ""),
            )
        ):
            self.checker.visit_attribute(node)

    @set_config(ignored_modules=("argparse",))
    def test_no_member_in_getattr_ignored(self):
        """Make sure that a module attribute access check is omitted with a
        module that is configured to be ignored.
        """

        node = astroid.extract_node(
            """
        import argparse
        argparse.THIS_does_not_EXIST
        """
        )
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    @set_config(ignored_modules=("xml.etree.",))
    def test_ignored_modules_invalid_pattern(self):
        node = astroid.extract_node(
            """
        import xml
        xml.etree.Lala
        """
        )
        message = Message(
            "no-member", node=node, args=("Module", "xml.etree", "Lala", "")
        )
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    @set_config(ignored_modules=("xml",))
    def test_ignored_modules_root_one_applies_as_well(self):
        # Check that when a root module is completely ignored, submodules are skipped.
        node = astroid.extract_node(
            """
        import xml
        xml.etree.Lala
        """
        )
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    @set_config(ignored_modules=("xml.etree*",))
    def test_ignored_modules_patterns(self):
        node = astroid.extract_node(
            """
        import xml
        xml.etree.portocola #@
        """
        )
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    @set_config(ignored_classes=("xml.*",))
    def test_ignored_classes_no_recursive_pattern(self):
        node = astroid.extract_node(
            """
        import xml
        xml.etree.ElementTree.Test
        """
        )
        message = Message(
            "no-member", node=node, args=("Module", "xml.etree.ElementTree", "Test", "")
        )
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    @set_config(ignored_classes=("optparse.Values",))
    def test_ignored_classes_qualified_name(self):
        """Test that ignored-classes supports qualified name for ignoring."""
        node = astroid.extract_node(
            """
        import optparse
        optparse.Values.lala
        """
        )
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    @set_config(ignored_classes=("Values",))
    def test_ignored_classes_only_name(self):
        """Test that ignored_classes works with the name only."""
        node = astroid.extract_node(
            """
        import optparse
        optparse.Values.lala
        """
        )
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    @set_config(suggestion_mode=False)
    @needs_c_extension
    def test_nomember_on_c_extension_error_msg(self):
        node = astroid.extract_node(
            """
        from coverage import tracer
        tracer.CTracer  #@
        """
        )
        message = Message(
            "no-member", node=node, args=("Module", "coverage.tracer", "CTracer", "")
        )
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    @set_config(suggestion_mode=True)
    @needs_c_extension
    def test_nomember_on_c_extension_info_msg(self):
        node = astroid.extract_node(
            """
        from coverage import tracer
        tracer.CTracer  #@
        """
        )
        message = Message(
            "c-extension-no-member",
            node=node,
            args=("Module", "coverage.tracer", "CTracer", ""),
        )
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    @set_config(
        contextmanager_decorators=(
            "contextlib.contextmanager",
            ".custom_contextmanager",
        )
    )
    def test_custom_context_manager(self):
        """Test that @custom_contextmanager is recognized as configured."""
        node = astroid.extract_node(
            """
        from contextlib import contextmanager
        def custom_contextmanager(f):
            return contextmanager(f)
        @custom_contextmanager
        def dec():
            yield
        with dec():
            pass
        """
        )
        with self.assertNoMessages():
            self.checker.visit_with(node)

    def test_invalid_metaclass(self):
        module = astroid.parse(
            """
        class InvalidAsMetaclass(object):
            pass

        class FirstInvalid(object, metaclass=int):
            pass

        class SecondInvalid(object, metaclass=InvalidAsMetaclass):
            pass

        class ThirdInvalid(object, metaclass=2):
            pass
        """
        )
        for class_obj, metaclass_name in (
            ("ThirdInvalid", "2"),
            ("SecondInvalid", "InvalidAsMetaclass"),
            ("FirstInvalid", "int"),
        ):
            classdef = module[class_obj]
            message = Message(
                "invalid-metaclass", node=classdef, args=(metaclass_name,)
            )
            with self.assertAddsMessages(message):
                self.checker.visit_classdef(classdef)

    def test_invalid_metaclass_function_metaclasses(self):
        module = astroid.parse(
            """
        def invalid_metaclass_1(name, bases, attrs):
            return int
        def invalid_metaclass_2(name, bases, attrs):
            return 1
        class Invalid(metaclass=invalid_metaclass_1):
            pass
        class InvalidSecond(metaclass=invalid_metaclass_2):
            pass
        """
        )
        for class_obj, metaclass_name in (("Invalid", "int"), ("InvalidSecond", "1")):
            classdef = module[class_obj]
            message = Message(
                "invalid-metaclass", node=classdef, args=(metaclass_name,)
            )
            with self.assertAddsMessages(message):
                self.checker.visit_classdef(classdef)

    def test_typing_namedtuple_not_callable_issue1295(self):
        module = astroid.parse(
            """
        import typing
        Named = typing.NamedTuple('Named', [('foo', int), ('bar', int)])
        named = Named(1, 2)
        """
        )
        call = module.body[-1].value
        callables = call.func.inferred()
        assert len(callables) == 1
        assert callables[0].callable()
        with self.assertNoMessages():
            self.checker.visit_call(call)

    def test_typing_namedtuple_unsubscriptable_object_issue1295(self):
        module = astroid.parse(
            """
        import typing
        MyType = typing.Tuple[str, str]
        """
        )
        subscript = module.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_subscript(subscript)

    def test_staticmethod_multiprocessing_call(self):
        """Make sure not-callable isn't raised for descriptors

        astroid can't process descriptors correctly so
        pylint needs to ignore not-callable for them
        right now

        Test for https://github.com/PyCQA/pylint/issues/1699
        """
        call = astroid.extract_node(
            """
        import multiprocessing
        multiprocessing.current_process() #@
        """
        )
        with self.assertNoMessages():
            self.checker.visit_call(call)

    def test_not_callable_uninferable_property(self):
        """Make sure not-callable isn't raised for uninferable
        properties
        """
        call = astroid.extract_node(
            """
        class A:
            @property
            def call(self):
                return undefined

        a = A()
        a.call() #@
        """
        )
        with self.assertNoMessages():
            self.checker.visit_call(call)

    def test_descriptor_call(self):
        call = astroid.extract_node(
            """
        def func():
            pass

        class ADescriptor:
            def __get__(self, instance, owner):
                return func

        class AggregateCls:
            a = ADescriptor()

        AggregateCls().a() #@
        """
        )
        with self.assertNoMessages():
            self.checker.visit_call(call)

    def test_unknown_parent(self):
        """Make sure the callable check does not crash when a node's parent
        cannot be determined.
        """
        call = astroid.extract_node(
            """
        def get_num(n):
            return 2 * n
        get_num(10)()
        """
        )
        with self.assertAddsMessages(
            Message("not-callable", node=call, args="get_num(10)")
        ):
            self.checker.visit_call(call)


class TestTypeCheckerOnDecorators(CheckerTestCase):
    "Tests for pylint.checkers.typecheck on decorated functions."
    CHECKER_CLASS = typecheck.TypeChecker

    def test_issue3882_class_decorators(self):
        decorators = """
        class Unsubscriptable:
            def __init__(self, f):
                self.f = f

        class Subscriptable:
            def __init__(self, f):
                self.f = f

            def __getitem__(self, item):
                return item
        """
        for generic in "Optional", "List", "ClassVar", "Final", "Literal":
            self.typing_objects_are_subscriptable(generic)

        self.getitem_on_modules()
        self.decorated_by_a_subscriptable_class(decorators)
        self.decorated_by_an_unsubscriptable_class(decorators)

        self.decorated_by_subscriptable_then_unsubscriptable_class(decorators)
        self.decorated_by_unsubscriptable_then_subscriptable_class(decorators)

    def getitem_on_modules(self):
        """Mainly validate the code won't crash if we're not having a function."""
        module = astroid.parse(
            """
        import collections
        test = collections[int]
        """
        )
        subscript = module.body[-1].value
        with self.assertAddsMessages(
            Message(
                "unsubscriptable-object",
                node=subscript.value,
                args="collections",
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_subscript(subscript)

    def typing_objects_are_subscriptable(self, generic):
        module = astroid.parse(
            f"""
        import typing
        test = typing.{generic}[int]
        """
        )
        subscript = module.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_subscript(subscript)

    def decorated_by_a_subscriptable_class(self, decorators):
        module = astroid.parse(
            decorators
            + """
        @Subscriptable
        def decorated():
            ...

        test = decorated[None]
        """
        )
        subscript = module.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_subscript(subscript)

    def decorated_by_subscriptable_then_unsubscriptable_class(self, decorators):
        module = astroid.parse(
            decorators
            + """
        @Unsubscriptable
        @Subscriptable
        def decorated():
            ...

        test = decorated[None]
        """
        )
        subscript = module.body[-1].value
        with self.assertAddsMessages(
            Message(
                "unsubscriptable-object",
                node=subscript.value,
                args="decorated",
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_subscript(subscript)

    def decorated_by_unsubscriptable_then_subscriptable_class(self, decorators):
        module = astroid.parse(
            decorators
            + """
        @Subscriptable
        @Unsubscriptable
        def decorated():
            ...

        test = decorated[None]
        """
        )
        subscript = module.body[-1].value
        with self.assertNoMessages():
            self.checker.visit_subscript(subscript)

    def decorated_by_an_unsubscriptable_class(self, decorators):
        module = astroid.parse(
            decorators
            + """
        @Unsubscriptable
        def decorated():
            ...

        test = decorated[None]
        """
        )
        subscript = module.body[-1].value
        with self.assertAddsMessages(
            Message(
                "unsubscriptable-object",
                node=subscript.value,
                args="decorated",
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_subscript(subscript)
