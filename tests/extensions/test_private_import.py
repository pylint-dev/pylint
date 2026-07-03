# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests the local module directory comparison logic which requires mocking file directories."""

from unittest.mock import MagicMock, patch

import astroid

from pylint.extensions import private_import
from pylint.interfaces import HIGH
from pylint.testutils import CheckerTestCase, MessageTest


class TestPrivateImport(CheckerTestCase):
    """The mocked dirname is the directory of the file being linted, the node is code inside that file."""

    CHECKER_CLASS = private_import.PrivateImportChecker

    @patch("pathlib.Path.parent")
    def test_internal_module(self, parent: MagicMock) -> None:
        parent.parts = ("", "dir", "module")
        import_from = astroid.extract_node("""from module import _file""")

        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    @patch("pathlib.Path.parent")
    def test_external_module_nested(self, parent: MagicMock) -> None:
        parent.parts = ("", "dir", "module", "module_files", "util")

        import_from = astroid.extract_node("""from module import _file""")

        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    @patch("pathlib.Path.parent")
    def test_external_module_dot_import(self, parent: MagicMock) -> None:
        parent.parts = ("", "dir", "outer", "inner", "module_files", "util")

        import_from = astroid.extract_node("""from outer.inner import _file""")

        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    @patch("pathlib.Path.parent")
    def test_external_module_dot_import_outer_only(self, parent: MagicMock) -> None:
        parent.parts = ("", "dir", "outer", "extensions")

        import_from = astroid.extract_node("""from outer.inner import _file""")

        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    @patch("pathlib.Path.parent")
    def test_external_module(self, parent: MagicMock) -> None:
        parent.parts = ("", "dir", "other")

        import_from = astroid.extract_node("""from module import _file""")

        msg = MessageTest(
            msg_id="import-private-name",
            node=import_from,
            line=1,
            col_offset=0,
            end_line=1,
            end_col_offset=24,
            args=("object", "_file"),
            confidence=HIGH,
        )
        with self.assertAddsMessages(msg):
            self.checker.visit_importfrom(import_from)
