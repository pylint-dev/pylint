"""Unit tests for the imports checker."""
import os
import unittest

import astroid
from astroid import test_utils
from pylint.checkers import imports
from pylint.testutils import CheckerTestCase, Message, set_config


class ImportsCheckerTC(CheckerTestCase):

    CHECKER_CLASS = imports.ImportsChecker

    @set_config(ignored_modules=('external_module',
                                 'fake_module.submodule',
                                 'foo',
                                 'bar'))
    def test_import_error_skipped(self):
        """Make sure that imports do not emit a 'import-error' when the
        module is configured to be ignored."""

        node = test_utils.extract_node("""
        from external_module import anything
        """)
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)

        node = test_utils.extract_node("""
        from external_module.another_module import anything
        """)
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)

        node = test_utils.extract_node("""
        import external_module
        """)
        with self.assertNoMessages():
            self.checker.visit_import(node)

        node = test_utils.extract_node("""
        from fake_module.submodule import anything
        """)
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)

        node = test_utils.extract_node("""
        from fake_module.submodule.deeper import anything
        """)
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)

        node = test_utils.extract_node("""
        import foo, bar
        """)
        msg = Message('multiple-imports', node=node, args='foo, bar')
        with self.assertAddsMessages(msg):
            self.checker.visit_import(node)

        node = test_utils.extract_node("""
        import foo
        import bar
        """)
        with self.assertNoMessages():
            self.checker.visit_import(node)

    def test_reimported_same_line(self):
        """
        Test that duplicate imports on single line raise 'reimported'.
        """
        node = test_utils.extract_node('from time import sleep, sleep, time')
        msg = Message(msg_id='reimported', node=node, args=('sleep', 1))
        with self.assertAddsMessages(msg):
            self.checker.visit_importfrom(node)

    def test_relative_beyond_top_level(self):
        here = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(here, 'regrtest_data', 'beyond_top', '__init__.py')
        with open(path) as stream:
            data = stream.read()
        module = astroid.parse(data, module_name='beyond_top', path=path)
        import_from = module.body[0]

        msg = Message(msg_id='relative-beyond-top-level',
                      node=import_from)
        with self.assertAddsMessages(msg):
            self.checker.visit_importfrom(import_from)    
        with self.assertNoMessages():
            self.checker.visit_importfrom(module.body[1])
        with self.assertNoMessages():
            self.checker.visit_importfrom(module.body[2].body[0])


if __name__ == '__main__':
    unittest.main()
