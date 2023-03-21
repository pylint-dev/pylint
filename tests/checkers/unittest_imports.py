# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Unit tests for the imports checker."""

import os

import astroid
from pytest import CaptureFixture

from pylint.checkers import imports
from pylint.interfaces import UNDEFINED
from pylint.testutils import CheckerTestCase, MessageTest
from pylint.testutils._run import _Run as Run

REGR_DATA = os.path.join(os.path.dirname(__file__), "..", "regrtest_data", "")


class TestImportsChecker(CheckerTestCase):
    CHECKER_CLASS = imports.ImportsChecker

    def test_relative_beyond_top_level(self) -> None:
        module = astroid.MANAGER.ast_from_module_name("beyond_top", REGR_DATA)
        import_from = module.body[0]

        msg = MessageTest(
            msg_id="relative-beyond-top-level",
            node=import_from,
            line=1,
            col_offset=0,
            end_line=1,
            end_col_offset=25,
        )
        with self.assertAddsMessages(msg):
            self.checker.visit_importfrom(import_from)
        with self.assertNoMessages():
            self.checker.visit_importfrom(module.body[1])
        with self.assertNoMessages():
            self.checker.visit_importfrom(module.body[2].body[0])

    @staticmethod
    def test_relative_beyond_top_level_two(capsys: CaptureFixture[str]) -> None:
        Run(
            [
                f"{os.path.join(REGR_DATA, 'beyond_top_two')}",
                "-d all",
                "-e relative-beyond-top-level",
            ],
            exit=False,
        )
        output, errors = capsys.readouterr()

        top_level_function = os.path.join(
            REGR_DATA, "beyond_top_two/namespace_package/top_level_function.py"
        )
        Run(
            [top_level_function, "-d all", "-e relative-beyond-top-level"],
            exit=False,
        )
        output2, errors2 = capsys.readouterr()

        assert len(output.split("\n")) == 5
        assert len(output2.split("\n")) == 5
        assert errors == errors2

    @staticmethod
    def test_relative_beyond_top_level_three(capsys: CaptureFixture[str]) -> None:
        Run(
            [
                f"{os.path.join(REGR_DATA, 'beyond_top_three/a.py')}",
                "-d all",
                "-e relative-beyond-top-level",
            ],
            exit=False,
        )
        output, errors = capsys.readouterr()
        assert len(output.split("\n")) == 5
        assert errors == ""

    @staticmethod
    def test_relative_beyond_top_level_four(capsys: CaptureFixture[str]) -> None:
        Run(
            [
                f"{os.path.join(REGR_DATA, 'beyond_top_four/module')}",
                "-d missing-docstring,unused-import",
            ],
            exit=False,
        )
        output, errors = capsys.readouterr()
        assert len(output.split("\n")) == 5
        assert errors == ""

    def test_wildcard_import_init(self) -> None:
        module = astroid.MANAGER.ast_from_module_name("init_wildcard", REGR_DATA)
        import_from = module.body[0]

        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    def test_wildcard_import_non_init(self) -> None:
        module = astroid.MANAGER.ast_from_module_name("wildcard", REGR_DATA)
        import_from = module.body[0]

        msg = MessageTest(
            msg_id="wildcard-import",
            node=import_from,
            args="empty",
            confidence=UNDEFINED,
            line=1,
            col_offset=0,
            end_line=1,
            end_col_offset=19,
        )
        with self.assertAddsMessages(msg):
            self.checker.visit_importfrom(import_from)

    @staticmethod
    def test_preferred_module(capsys: CaptureFixture[str]) -> None:
        """
        Tests preferred-module configuration option
        """
        # test preferred-modules case with base module import
        Run(
            [
                f"{os.path.join(REGR_DATA, 'preferred_module/unpreferred_module.py')}",
                "-d all",
                "-e preferred-module",
                # prefer sys instead of os (for triggering test)
                "--preferred-modules=os:sys",
            ],
            exit=False,
        )
        output, errors = capsys.readouterr()

        # assert that we saw preferred-modules triggered
        assert "Prefer importing 'sys' instead of 'os'" in output
        # assert there were no errors
        assert len(errors) == 0

        # test preferred-modules trigger case with submodules
        Run(
            [
                f"{os.path.join(REGR_DATA, 'preferred_module/unpreferred_submodule.py')}",
                "-d all",
                "-e preferred-module",
                # prefer os.path instead of pathlib (for triggering test)
                "--preferred-modules=os.path:pathlib",
            ],
            exit=False,
        )
        output, errors = capsys.readouterr()

        # assert that we saw preferred-modules triggered
        assert "Prefer importing 'pathlib' instead of 'os.path'" in output
        # assert there were no errors
        assert len(errors) == 0

        # test preferred-modules ignore case with submodules
        Run(
            [
                f"{os.path.join(REGR_DATA, 'preferred_module/unpreferred_submodule.py')}",
                "-d all",
                "-e preferred-module",
                # prefer pathlib instead of os.stat (for untriggered test)
                "--preferred-modules=os.stat:pathlib",
            ],
            exit=False,
        )
        output, errors = capsys.readouterr()

        # assert that we didn't see preferred-modules triggered
        assert "Your code has been rated at 10.00/10" in output
        # assert there were no errors
        assert len(errors) == 0

        # test preferred-modules base module for implemented submodule (from ... import)
        Run(
            [
                f"{os.path.join(REGR_DATA, 'preferred_module/unpreferred_submodule.py')}",
                "-d all",
                "-e preferred-module",
                # prefer pathlib instead of os (for triggering test)
                "--preferred-modules=os:pathlib",
            ],
            exit=False,
        )
        output, errors = capsys.readouterr()

        # assert that we saw preferred-modules triggered with base module
        assert "Prefer importing 'pathlib' instead of 'os'" in output
        # assert there were no errors
        assert len(errors) == 0

        # Test for challenges with preferred modules indefinite matches
        Run(
            [
                f"{os.path.join(REGR_DATA, 'preferred_module/unpreferred_submodule.py')}",
                "-d all",
                "-e preferred-module",
                # prefer pathlib instead of random (testing to avoid regression)
                # pathlib shouldn't match with path, which is in the test file
                "--preferred-modules=random:pathlib",
            ],
            exit=False,
        )
        _, errors = capsys.readouterr()

        # Assert there were no errors
        assert len(errors) == 0

    @staticmethod
    def test_allow_reexport_package(capsys: CaptureFixture[str]) -> None:
        """Test --allow-reexport-from-package option."""

        # Option disabled - useless-import-alias should always be emitted
        Run(
            [
                f"{os.path.join(REGR_DATA, 'allow_reexport')}",
                "--allow-reexport-from-package=no",
                "-sn",
            ],
            exit=False,
        )
        output, errors = capsys.readouterr()
        assert len(output.split("\n")) == 7, f"Expected 7 line breaks in:{output}"
        assert (
            "__init__.py:1:0: C0414: Import alias does not rename original package (useless-import-alias)"
            in output
        )
        assert (
            "file.py:2:0: C0414: Import alias does not rename original package (useless-import-alias)"
            in output
        )
        assert len(errors) == 0

        # Option enabled - useless-import-alias should only be emitted for 'file.py'
        Run(
            [
                f"{os.path.join(REGR_DATA, 'allow_reexport')}",
                "--allow-reexport-from-package=yes",
                "--disable=missing-module-docstring",
                "-sn",
            ],
            exit=False,
        )
        output, errors = capsys.readouterr()
        assert len(output.split("\n")) == 3
        assert "__init__.py" not in output
        assert (
            "file.py:2:0: C0414: Import alias does not rename original package (useless-import-alias)"
            in output
        )
        assert len(errors) == 0
