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

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unit tests for the imports checker."""

import os

import astroid

from pylint.checkers import imports
from pylint.interfaces import UNDEFINED
from pylint.testutils import CheckerTestCase, Message, set_config

REGR_DATA = os.path.join(os.path.dirname(__file__), "..", "regrtest_data", "")


class TestImportsChecker(CheckerTestCase):

    CHECKER_CLASS = imports.ImportsChecker

    @set_config(allow_any_import_level=("astroid",))
    def test_import_outside_toplevel(self):
        node = astroid.extract_node(
            """
        def f():
            import astroid
        """
        ).body[0]

        with self.assertNoMessages():
            self.checker.visit_import(node)

        node = astroid.extract_node(
            """
        def g():
            import pylint
        """
        ).body[0]

        with self.assertAddsMessages(
            Message("import-outside-toplevel", node=node, args="pylint")
        ):
            self.checker.visit_import(node)

    @set_config(
        ignored_modules=("external_module", "fake_module.submodule", "foo", "bar")
    )
    def test_import_error_skipped(self):
        """Make sure that imports do not emit an 'import-error' when the
        module is configured to be ignored."""

        node = astroid.extract_node(
            """
        from external_module import anything
        """
        )
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)

        node = astroid.extract_node(
            """
        from external_module.another_module import anything
        """
        )
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)

        node = astroid.extract_node(
            """
        import external_module
        """
        )
        with self.assertNoMessages():
            self.checker.visit_import(node)

        node = astroid.extract_node(
            """
        from fake_module.submodule import anything
        """
        )
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)

        node = astroid.extract_node(
            """
        from fake_module.submodule.deeper import anything
        """
        )
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)

        node = astroid.extract_node(
            """
        import foo, bar
        """
        )
        msg = Message("multiple-imports", node=node, args="foo, bar")
        with self.assertAddsMessages(msg):
            self.checker.visit_import(node)

        node = astroid.extract_node(
            """
        import foo
        import bar
        """
        )
        with self.assertNoMessages():
            self.checker.visit_import(node)

    def test_reimported_same_line(self):
        """
        Test that duplicate imports on single line raise 'reimported'.
        """
        node = astroid.extract_node("from time import sleep, sleep, time")
        msg = Message(msg_id="reimported", node=node, args=("sleep", 1))
        with self.assertAddsMessages(msg):
            self.checker.visit_importfrom(node)

    def test_relative_beyond_top_level(self):
        module = astroid.MANAGER.ast_from_module_name("beyond_top", REGR_DATA)
        import_from = module.body[0]

        msg = Message(msg_id="relative-beyond-top-level", node=import_from)
        with self.assertAddsMessages(msg):
            self.checker.visit_importfrom(import_from)
        with self.assertNoMessages():
            self.checker.visit_importfrom(module.body[1])
        with self.assertNoMessages():
            self.checker.visit_importfrom(module.body[2].body[0])

    def test_wildcard_import_init(self):
        module = astroid.MANAGER.ast_from_module_name("init_wildcard", REGR_DATA)
        import_from = module.body[0]

        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    def test_wildcard_import_non_init(self):
        module = astroid.MANAGER.ast_from_module_name("wildcard", REGR_DATA)
        import_from = module.body[0]

        msg = Message(
            msg_id="wildcard-import",
            node=import_from,
            args="empty",
            confidence=UNDEFINED,
        )
        with self.assertAddsMessages(msg):
            self.checker.visit_importfrom(import_from)
