# Copyright (c) 2015-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Cezar <celnazli@bitdefender.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2017 Martin <MartinBasti@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import contextlib

import astroid

from pylint.checkers import stdlib
from pylint.testutils import CheckerTestCase, Message
from pylint.interfaces import UNDEFINED


@contextlib.contextmanager
def _add_transform(manager, node, transform, predicate=None):
    manager.register_transform(node, transform, predicate)
    try:
        yield
    finally:
        manager.unregister_transform(node, transform, predicate)


class TestStdlibChecker(CheckerTestCase):
    CHECKER_CLASS = stdlib.StdlibChecker

    def test_deprecated_no_qname_on_unexpected_nodes(self):
        # Test that we don't crash on nodes which don't have
        # a qname method. While this test might seem weird since
        # it uses a transform, it's actually testing a crash that
        # happened in production, but there was no way to retrieve
        # the code for which this occurred (how an AssignAttr
        # got to be the result of a function inference
        # beats me..)

        def infer_func(node, context=None):
            new_node = astroid.AssignAttr()
            new_node.parent = node
            yield new_node

        manager = astroid.MANAGER
        transform = astroid.inference_tip(infer_func)
        with _add_transform(manager, astroid.Name, transform):
            node = astroid.extract_node('''
            call_something()
            ''')
            with self.assertNoMessages():
                self.checker.visit_call(node)

    def test_copy_environ(self):
        # shallow copy of os.environ should be reported
        node = astroid.extract_node("""
        import copy, os
        copy.copy(os.environ)
        """)
        with self.assertAddsMessages(
            Message(
                msg_id='shallow-copy-environ', node=node, confidence=UNDEFINED)
        ):
            self.checker.visit_call(node)

    def test_copy_environ_hidden(self):
        # shallow copy of os.environ should be reported
        # hide function names to be sure that checker is not just matching text
        node = astroid.extract_node("""
        from copy import copy as test_cp
        import os as o
        test_cp(o.environ)
        """)
        with self.assertAddsMessages(
            Message(
                msg_id='shallow-copy-environ', node=node, confidence=UNDEFINED)
        ):
            self.checker.visit_call(node)

    def test_copy_dict(self):
        # copy of dict is OK
        node = astroid.extract_node("""
        import copy
        test_dict = {}
        copy.copy(test_dict)
        """)
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_copy_uninferable(self):
        # copy of uninferable object should not raise exception, nor make
        # the checker crash
        node = astroid.extract_node("""
        import copy
        from missing_library import MissingObject
        copy.copy(MissingObject)
        """)
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_deepcopy_environ(self):
        # deepcopy of os.environ is OK
        node = astroid.extract_node("""
        import copy, os
        copy.deepcopy(os.environ)
        """)
        with self.assertNoMessages():
            self.checker.visit_call(node)
