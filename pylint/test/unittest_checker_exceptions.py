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
"""Tests for pylint.checkers.exceptions."""

import sys
import unittest

from astroid import test_utils
from pylint.checkers import exceptions
from pylint.testutils import CheckerTestCase, Message


class ExceptionsCheckerTest(CheckerTestCase):
    """Tests for pylint.checkers.exceptions."""

    CHECKER_CLASS = exceptions.ExceptionsChecker

    # These tests aren't in the functional test suite,
    # since they will be converted with 2to3 for Python 3
    # and `raise (Error, ...)` will be converted to
    # `raise Error(...)`, so it beats the purpose of the test.

    @unittest.skipUnless(sys.version_info[0] == 3,
                         "The test should emit an error on Python 3.")
    def test_raising_bad_type_python3(self):
        node = test_utils.extract_node('raise (ZeroDivisionError, None)  #@')
        message = Message('raising-bad-type', node=node, args='tuple')
        with self.assertAddsMessages(message):
            self.checker.visit_raise(node)

    @unittest.skipUnless(sys.version_info[0] == 2,
                         "The test is valid only on Python 2.")
    def test_raising_bad_type_python2(self):
        nodes = test_utils.extract_node('''
        raise (ZeroDivisionError, None)  #@
        from something import something
        raise (something, None) #@

        raise (4, None) #@
        ''')
        with self.assertNoMessages():
            self.checker.visit_raise(nodes[0])
        with self.assertNoMessages():
            self.checker.visit_raise(nodes[1])

        message = Message('raising-bad-type', node=nodes[2], args='tuple')
        with self.assertAddsMessages(message):
            self.checker.visit_raise(nodes[2])

    def test_duplicate_except(self):
        node = test_utils.extract_node('''
        try:
            raise ValueError('test')
        except ValueError:
            print(1)
        except ValueError:
            print(2)
        except (OSError, TypeError):
            print(3)
        ''')
        message = Message('duplicate-except', node=node.handlers[1].type,
                          args='ValueError')
        with self.assertAddsMessages(message):
            self.checker.visit_tryexcept(node)


if __name__ == '__main__':
    unittest.main()
