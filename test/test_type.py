"""Unittest for the type checker."""

import re

from astroid import test_utils
from pylint.checkers import typecheck
from pylint.testutils import CheckerTestCase, Message, set_config


class TypeCheckerTest(CheckerTestCase):
    CHECKER_CLASS = typecheck.TypeChecker
    CONFIG = {
        'bad_names': set(),
        }

#    @set_config(include_naming_hint=True,
#            const_name_hint='CONSTANT')
    def test_naming_hint_configured_hint(self):
        const = test_utils.extract_node("""
        import argparse
        argparse.THIS_does_not_EXIST 
        """)
        with self.assertAddsMessages(Message('no-member', node=const, args=('Module', 'argparse', 'THIS_does_not_EXIST'))):
            self.checker.visit_getattr(const)


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
