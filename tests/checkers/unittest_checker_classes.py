# Copyright (c) 2014-2019 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Bryce Guinta <bryce.paul.guinta@gmail.com>
# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
# Copyright (c) 2019 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2019 Pierre Sassoulas <pierre.sassoulas@gmail.com>

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
