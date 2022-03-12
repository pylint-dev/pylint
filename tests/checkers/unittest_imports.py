# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

"""Unit tests for the imports checker."""

import os

import astroid

from pylint import epylint as lint
from pylint.checkers import imports
from pylint.interfaces import UNDEFINED
from pylint.testutils import CheckerTestCase, MessageTest

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
    def test_relative_beyond_top_level_two() -> None:
        output, errors = lint.py_run(
            f"{os.path.join(REGR_DATA, 'beyond_top_two')} -d all -e relative-beyond-top-level",
            return_std=True,
        )
        top_level_function = os.path.join(
            REGR_DATA, "beyond_top_two/namespace_package/top_level_function.py"
        )
        output2, errors2 = lint.py_run(
            f"{top_level_function} -d all -e relative-beyond-top-level",
            return_std=True,
        )

        assert len(output.readlines()) == len(output2.readlines())
        assert errors.readlines() == errors2.readlines()

    @staticmethod
    def test_relative_beyond_top_level_three() -> None:
        output, errors = lint.py_run(
            f"{os.path.join(REGR_DATA, 'beyond_top_three/a.py')} -d all -e relative-beyond-top-level",
            return_std=True,
        )
        assert len(output.readlines()) == 5
        assert errors.readlines() == []

    @staticmethod
    def test_relative_beyond_top_level_four() -> None:
        output, errors = lint.py_run(
            f"{os.path.join(REGR_DATA, 'beyond_top_four/module')} -d missing-docstring,unused-import",
            return_std=True,
        )
        assert len(output.readlines()) == 5
        assert errors.readlines() == []

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
