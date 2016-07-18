# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unit tests for the raised exception documentation checking in the
`DocstringChecker` in :mod:`pylint.extensions.check_docs`
"""
from __future__ import division, print_function, absolute_import

import unittest

import astroid
from astroid import test_utils
from pylint.testutils import CheckerTestCase, Message, set_config

from pylint.extensions.docparams import DocstringParameterChecker


class DocstringCheckerRaiseTest(CheckerTestCase):
    """Tests for pylint_plugin.RaiseDocChecker"""
    CHECKER_CLASS = DocstringParameterChecker

    def test_ignores_no_docstring(self):
        raise_node = test_utils.extract_node('''
        def my_func(self):
            raise RuntimeError('hi') #@
        ''')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_ignores_unknown_style(self):
        node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring."""
            raise RuntimeError('hi')
        ''')
        raise_node = node.body[0]
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    @set_config(accept_no_raise_doc=False)
    def test_warns_unknown_style(self):
        node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring."""
            raise RuntimeError('hi')
        ''')
        raise_node = node.body[0]
        with self.assertAddsMessages(
            Message(
                msg_id='missing-raises-doc',
                node=node,
                args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_missing_sphinx_raises(self):
        node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            :raises NameError: Never
            """
            raise RuntimeError('hi')
            raise NameError('hi')
        ''')
        raise_node = node.body[0]
        with self.assertAddsMessages(
            Message(
                msg_id='missing-raises-doc',
                node=node,
                args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_missing_google_raises(self):
        node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            Raises:
                NameError: Never
            """
            raise RuntimeError('hi')
            raise NameError('hi')
        ''')
        raise_node = node.body[0]
        with self.assertAddsMessages(
            Message(
                msg_id='missing-raises-doc',
                node=node,
                args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_missing_numpy_raises(self):
        node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            Raises
            ------
            NameError
                Never
            """
            raise RuntimeError('hi')
            raise NameError('hi')
        ''')
        raise_node = node.body[0]
        with self.assertAddsMessages(
            Message(
                msg_id='missing-raises-doc',
                node=node,
                args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_all_sphinx_raises(self):
        raise_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            :raises RuntimeError: Always
            :raises NameError: Never
            """
            raise RuntimeError('hi') #@
            raise NameError('hi')
        ''')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_find_all_google_raises(self):
        raise_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            Raises:
                RuntimeError: Always
                NameError: Never
            """
            raise RuntimeError('hi') #@
            raise NameError('hi')
        ''')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_find_all_numpy_raises(self):
        raise_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            Raises
            ------
            RuntimeError
                Always
            NameError
                Never
            """
            raise RuntimeError('hi') #@
            raise NameError('hi')
        ''')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_finds_rethrown_sphinx_raises(self):
        raise_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            :raises NameError: Sometimes
            """
            try:
                fake_func()
            except RuntimeError:
                raise #@

            raise NameError('hi')
        ''')
        node = raise_node.frame()
        with self.assertAddsMessages(
            Message(
                msg_id='missing-raises-doc',
                node=node,
                args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_rethrown_google_raises(self):
        raise_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            Raises:
                NameError: Sometimes
            """
            try:
                fake_func()
            except RuntimeError:
                raise #@

            raise NameError('hi')
        ''')
        node = raise_node.frame()
        with self.assertAddsMessages(
            Message(
                msg_id='missing-raises-doc',
                node=node,
                args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_rethrown_numpy_raises(self):
        raise_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            Raises
            ------
            NameError
                Sometimes
            """
            try:
                fake_func()
            except RuntimeError:
                raise #@

            raise NameError('hi')
        ''')
        node = raise_node.frame()
        with self.assertAddsMessages(
            Message(
                msg_id='missing-raises-doc',
                node=node,
                args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_finds_rethrown_sphinx_mutiple_raises(self):
        raise_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            :raises NameError: Sometimes
            """
            try:
                fake_func()
            except (RuntimeError, ValueError):
                raise #@

            raise NameError('hi')
        ''')
        node = raise_node.frame()
        with self.assertAddsMessages(
            Message(
                msg_id='missing-raises-doc',
                node=node,
                args=('RuntimeError, ValueError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_rethrown_google_multiple_raises(self):
        raise_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            Raises:
                NameError: Sometimes
            """
            try:
                fake_func()
            except (RuntimeError, ValueError):
                raise #@

            raise NameError('hi')
        ''')
        node = raise_node.frame()
        with self.assertAddsMessages(
            Message(
                msg_id='missing-raises-doc',
                node=node,
                args=('RuntimeError, ValueError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_rethrown_numpy_multiple_raises(self):
        raise_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            Raises
            ------
            NameError
                Sometimes
            """
            try:
                fake_func()
            except (RuntimeError, ValueError):
                raise #@

            raise NameError('hi')
        ''')
        node = raise_node.frame()
        with self.assertAddsMessages(
            Message(
                msg_id='missing-raises-doc',
                node=node,
                args=('RuntimeError, ValueError', ))):
            self.checker.visit_raise(raise_node)

    def test_ignores_caught_sphinx_raises(self):
        raise_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            :raises NameError: Sometimes
            """
            try:
                raise RuntimeError('hi') #@
            except RuntimeError:
                pass

            raise NameError('hi')
        ''')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_ignores_caught_google_raises(self):
        raise_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            Raises:
                NameError: Sometimes
            """
            try:
                raise RuntimeError('hi') #@
            except RuntimeError:
                pass

            raise NameError('hi')
        ''')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_ignores_caught_numpy_raises(self):
        raise_node = test_utils.extract_node('''
        def my_func(self):
            """This is a docstring.

            Raises
            ------
            NameError
                Sometimes
            """
            try:
                raise RuntimeError('hi') #@
            except RuntimeError:
                pass

            raise NameError('hi')
        ''')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_no_crash_when_inferring_handlers(self):
        raise_node = test_utils.extract_node('''
        import collections

        def test():
           """raises

           :raise U: pass
           """
           try:
              pass
           except collections.U as exc:
              raise #@
        ''')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_no_crash_when_cant_find_exception(self):
        raise_node = test_utils.extract_node('''
        import collections

        def test():
           """raises

           :raise U: pass
           """
           try:
              pass
           except U as exc:
              raise #@
        ''')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)


if __name__ == '__main__':
    unittest.main()
