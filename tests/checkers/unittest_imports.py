# Copyright (c) 2015-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Dmitry Pribysh <dmand@yandex.ru>
# Copyright (c) 2015 Cezar <celnazli@bitdefender.com>
# Copyright (c) 2015 James Morgensen <james.morgensen@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Hornwitser <github@hornwitser.no>
# Copyright (c) 2018 Marianna Polatoglou <mpolatoglou@bloomberg.net>
# Copyright (c) 2018 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Nick Drozd <nicholasdrozd@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

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

        msg = MessageTest(msg_id="relative-beyond-top-level", node=import_from)
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
        output2, errors2 = lint.py_run(
            f"{os.path.join(REGR_DATA, 'beyond_top_two/namespace_package/top_level_function.py')} -d all -e relative-beyond-top-level",
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
        )
        with self.assertAddsMessages(msg):
            self.checker.visit_importfrom(import_from)
