# Copyright (c) 2003-2015 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import contextlib
import unittest

import astroid
from astroid import test_utils

from pylint.checkers import stdlib
from pylint.testutils import CheckerTestCase


@contextlib.contextmanager
def _add_transform(manager, node, transform, predicate=None):
    manager.register_transform(node, transform, predicate)
    try:
        yield
    finally:
        manager.unregister_transform(node, transform, predicate)


class StdlibCheckerTest(CheckerTestCase):
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
            node = test_utils.extract_node('''
            call_something()
            ''')
            with self.assertNoMessages():
                self.checker.visit_call(node)
 


if __name__ == '__main__':
    unittest.main()
