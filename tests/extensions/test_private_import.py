"""Tests the local module directory comparison logic which requires mocking file directories"""

import os
from unittest.mock import patch

import astroid

from pylint.extensions import private_import
from pylint.testutils import CheckerTestCase, MessageTest


class TestPrivateImport(CheckerTestCase):
    """The mocked dirname is the directory of the file being linted, the node is code inside that file"""

    CHECKER_CLASS = private_import.PrivateImportChecker

    @patch("os.path.dirname")
    def test_internal_module(self, dirname) -> None:
        dirname.return_value = os.path.join("", "dir", "module")

        import_from = astroid.extract_node("""from module import _file""")

        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    @patch("os.path.dirname")
    def test_external_module_nested(self, dirname) -> None:
        dirname.return_value = os.path.join("", "dir", "module", "module_files", "util")

        import_from = astroid.extract_node("""from module import _file""")

        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    @patch("os.path.dirname")
    def test_external_module_dot_import(self, dirname) -> None:
        dirname.return_value = os.path.join(
            "", "dir", "outer", "inner", "module_files", "util"
        )

        import_from = astroid.extract_node("""from outer.inner import _file""")

        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    @patch("os.path.dirname")
    def test_external_module_dot_import_outer_only(self, dirname) -> None:
        dirname.return_value = os.path.join("", "dir", "outer", "extensions")

        import_from = astroid.extract_node("""from outer.inner import _file""")

        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    @patch("os.path.dirname")
    def test_external_module(self, dirname) -> None:
        dirname.return_value = os.path.join("", "dir", "other")

        import_from = astroid.extract_node("""from module import _file""")

        msg = MessageTest(
            msg_id="import-private-name",
            node=import_from,
            line=1,
            col_offset=0,
            end_line=1,
            end_col_offset=24,
            args=("object", "_file"),
        )
        with self.assertAddsMessages(msg):
            self.checker.visit_importfrom(import_from)
