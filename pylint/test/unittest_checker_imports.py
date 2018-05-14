# Copyright (c) 2015-2016 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Dmitry Pribysh <dmand@yandex.ru>
# Copyright (c) 2015 Cezar <celnazli@bitdefender.com>
# Copyright (c) 2015 James Morgensen <james.morgensen@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unit tests for the imports checker."""
import os

import astroid
from pylint.checkers import imports
from pylint.testutils import CheckerTestCase, Message, set_config
from pylint.interfaces import UNDEFINED


class TestImportsChecker(CheckerTestCase):

    CHECKER_CLASS = imports.ImportsChecker

    @set_config(ignored_modules=('external_module',
                                 'fake_module.submodule',
                                 'foo',
                                 'bar'))
    def test_import_error_skipped(self):
        """Make sure that imports do not emit an 'import-error' when the
        module is configured to be ignored."""

        node = astroid.extract_node("""
        from external_module import anything
        """)
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)

        node = astroid.extract_node("""
        from external_module.another_module import anything
        """)
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)

        node = astroid.extract_node("""
        import external_module
        """)
        with self.assertNoMessages():
            self.checker.visit_import(node)

        node = astroid.extract_node("""
        from fake_module.submodule import anything
        """)
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)

        node = astroid.extract_node("""
        from fake_module.submodule.deeper import anything
        """)
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)

        node = astroid.extract_node("""
        import foo, bar
        """)
        msg = Message('multiple-imports', node=node, args='foo, bar')
        with self.assertAddsMessages(msg):
            self.checker.visit_import(node)

        node = astroid.extract_node("""
        import foo
        import bar
        """)
        with self.assertNoMessages():
            self.checker.visit_import(node)

    def test_reimported_same_line(self):
        """
        Test that duplicate imports on single line raise 'reimported'.
        """
        node = astroid.extract_node('from time import sleep, sleep, time')
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

    def test_wildcard_import_init(self):
        here = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(
            here, 'regrtest_data', 'init_wildcard', '__init__.py')
        with open(path) as stream:
            data = stream.read()
        module = astroid.parse(data, module_name='__init__', path=path)
        import_from = module.body[0]

        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    def test_wildcard_import_non_init(self):
        here = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(
            here, 'regrtest_data', 'init_wildcard', '__init__.py')
        with open(path) as stream:
            data = stream.read()
        module = astroid.parse(data, module_name='awesome_module', path=path)
        import_from = module.body[0]

        msg = Message(
            msg_id='wildcard-import', node=import_from, args='awesome_module',
            confidence=UNDEFINED)
        with self.assertAddsMessages(msg):
            self.checker.visit_importfrom(import_from)
