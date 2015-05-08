"""Unit tests for the imports checker."""
import unittest

from astroid import test_utils
from pylint.checkers import imports
from pylint.testutils import CheckerTestCase, set_config

class ImportsCheckerTC(CheckerTestCase):

    CHECKER_CLASS = imports.ImportsChecker

    @set_config(ignored_modules=('external_module', 'fake_module.submodule'))
    def test_import_error_skipped(self):
        """Make sure that imports do not emit a 'import-error' when the
        module is configured to be ignored."""

        node = test_utils.extract_node("""
        from external_module import anything
        """)
        with self.assertNoMessages():
            self.checker.visit_from(node)

        node = test_utils.extract_node("""
        from external_module.another_module import anything
        """)
        with self.assertNoMessages():
            self.checker.visit_from(node)

        node = test_utils.extract_node("""
        import external_module
        """)
        with self.assertNoMessages():
            self.checker.visit_import(node)

        node = test_utils.extract_node("""
        from fake_module.submodule import anything
        """)
        with self.assertNoMessages():
            self.checker.visit_from(node)

        node = test_utils.extract_node("""
        from fake_module.submodule.deeper import anything
        """)
        with self.assertNoMessages():
            self.checker.visit_from(node)

if __name__ == '__main__':
    unittest.main()
