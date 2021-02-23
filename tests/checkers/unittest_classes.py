# Copyright (c) 2014-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Bryce Guinta <bryce.paul.guinta@gmail.com>
# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019-2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unit tests for the variables checker."""
import astroid

from pylint.checkers import classes
from pylint.testutils import CheckerTestCase, Message, set_config


class TestVariablesChecker(CheckerTestCase):

    CHECKER_CLASS = classes.ClassChecker

    def test_bitbucket_issue_164(self):
        """Issue 164 report a false negative for access-member-before-definition"""
        n1, n2 = astroid.extract_node(
            """
        class MyClass1:
          def __init__(self):
            self.first += 5 #@
            self.first = 0  #@
        """
        )
        message = Message(
            "access-member-before-definition", node=n1.target, args=("first", n2.lineno)
        )
        with self.assertAddsMessages(message):
            self.walk(n1.root())

    @set_config(exclude_protected=("_meta", "_manager"))
    def test_exclude_protected(self):
        """Test that exclude-protected can be used to
        exclude names from protected-access warning.
        """

        node = astroid.parse(
            """
        class Protected:
            '''empty'''
            def __init__(self):
                self._meta = 42
                self._manager = 24
                self._teta = 29
        OBJ = Protected()
        OBJ._meta
        OBJ._manager
        OBJ._teta
        """
        )
        with self.assertAddsMessages(
            Message("protected-access", node=node.body[-1].value, args="_teta")
        ):
            self.walk(node.root())

    def test_regression_non_parent_init_called_tracemalloc(self):
        # This used to raise a non-parent-init-called on Pylint 1.3
        # See issue https://bitbucket.org/logilab/pylint/issue/308/
        # for reference.
        node = astroid.extract_node(
            """
        from tracemalloc import Sequence
        class _Traces(Sequence):
            def __init__(self, traces): #@
                Sequence.__init__(self)
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_super_init_not_called_regression(self):
        # This should not emit a super-init-not-called
        # warning. It previously did this, because
        # ``next(node.infer())`` was used in that checker's
        # logic and the first inferred node was an Uninferable object,
        # leading to this false positive.
        node = astroid.extract_node(
            """
        import ctypes

        class Foo(ctypes.BigEndianStructure):
            def __init__(self): #@
                ctypes.BigEndianStructure.__init__(self)
        """
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_uninferable_attribute(self):
        """Make sure protect-access doesn't raise an exception Uninferable attributes"""

        node = astroid.extract_node(
            """
        class MC():
            @property
            def nargs(self):
                return 1 if self._nargs else 2

        class Application(metaclass=MC):
            def __no_special__(cls):
                nargs = obj._nargs #@
        """
        )
        with self.assertAddsMessages(
            Message("protected-access", node=node.value, args="_nargs")
        ):
            self.checker.visit_attribute(node.value)

    @set_config(check_protected_access_in_special_methods=True)
    def test_check_protected_access_in_special_methods(self):
        """Test that check-protected-access-in-special-methods can be used to
        trigger protected-access message emission for single underscore prefixed names
        inside special methods
        """

        node = astroid.parse(
            """
        class Protected:
            '''empty'''
            def __init__(self):
                self._protected = 42
                self.public = "A"
                self.__private = None
            def __eq__(self, other):
                self._protected = other._protected
            def _fake_special_(self, other):
                a = other.public
                self.public = other._protected
                self.__private = other.__private
        """
        )
        classdef = node.body[-1]
        assign_attribute_in_eq = classdef.instance_attr("_protected")[-1]
        attribute_in_eq = list(assign_attribute_in_eq.assigned_stmts())[-1]
        assign_attribute_in_fake_1 = classdef.instance_attr("public")[-1]
        attribute_in_fake_1 = list(assign_attribute_in_fake_1.assigned_stmts())[-1]
        assign_attribute_in_fake_2 = classdef.instance_attr("__private")[-1]
        attribute_in_fake_2 = list(assign_attribute_in_fake_2.assigned_stmts())[-1]
        with self.assertAddsMessages(
            Message("protected-access", node=attribute_in_eq, args="_protected"),
            Message("protected-access", node=attribute_in_fake_1, args="_protected"),
            Message("protected-access", node=attribute_in_fake_2, args="__private"),
        ):
            self.walk(node.root())

    @set_config(check_protected_access_in_special_methods=False)
    def test_check_protected_access_in_special_methods_deact(self):
        """Test that when check-protected-access-in-special-methods is False (default)
        no protected-access message emission for single underscore prefixed names
        inside special methods occur
        """

        node = astroid.parse(
            """
        class Protected:
            '''empty'''
            def __init__(self):
                self._protected = 42
                self.public = "A"
                self.__private = None
            def __eq__(self, other):
                self._protected = other._protected
            def _fake_special_(self, other):
                a = other.public
                self.public = other._protected
                self.__private = other.__private
        """
        )
        classdef = node.body[-1]
        assign_attribute_in_fake_1 = classdef.instance_attr("public")[-1]
        attribute_in_fake_1 = list(assign_attribute_in_fake_1.assigned_stmts())[-1]
        assign_attribute_in_fake_2 = classdef.instance_attr("__private")[-1]
        attribute_in_fake_2 = list(assign_attribute_in_fake_2.assigned_stmts())[-1]
        with self.assertAddsMessages(
            Message("protected-access", node=attribute_in_fake_1, args="_protected"),
            Message("protected-access", node=attribute_in_fake_2, args="__private"),
        ):
            self.walk(node.root())
