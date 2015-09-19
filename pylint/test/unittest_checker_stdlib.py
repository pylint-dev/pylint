"""Unit tests for the imports checker."""
import unittest

from astroid import test_utils
from pylint.checkers import stdlib
from pylint.testutils import CheckerTestCase, Message


class StdlibCheckerTC(CheckerTestCase):

    CHECKER_CLASS = stdlib.StdlibChecker

    def test_asyncio_deprecated(self):
        """
        `asyncio.async` is deprecated.
        """
        node = test_utils.extract_node("""
        import asyncio
        asyncio.async()
        """)
        msg = Message(msg_id='deprecated-method', node=node,
                      args=('async', ))
        with self.assertAddsMessages(msg):
            self.checker.visit_call(node)

    def test_base64_deprecated(self):
        """
        `base64.encodestring` and `base64.decodestring` are deprecated.
        """
        node = test_utils.extract_node("""
        import base64
        base64.encodestring('a')
        """)
        msg = Message(msg_id='deprecated-method', node=node,
                      args=('encodestring', ))
        with self.assertAddsMessages(msg):
            self.checker.visit_call(node)

        node = test_utils.extract_node("""
        import base64
        base64.decodestring('a')
        """)
        msg = Message(msg_id='deprecated-method', node=node,
                      args=('decodestring', ))
        with self.assertAddsMessages(msg):
            self.checker.visit_call(node)

    def test_cgi_deprecated(self):
        """
        All deprecated methods in package `cgi`
        """

        node = test_utils.extract_node("""
        from cgi import parse_qs
        parse_qs()
        """)
        msg = Message(msg_id='deprecated-method', node=node,
                      args=('parse_qs', ))
        with self.assertAddsMessages(msg):
            self.checker.visit_call(node)

        node = test_utils.extract_node("""
        import cgi
        cgi.parse_qsl()
        """)
        msg = Message(msg_id='deprecated-method', node=node,
                      args=('parse_qsl', ))
        with self.assertAddsMessages(msg):
            self.checker.visit_call(node)

        node = test_utils.extract_node("""
        from cgi import escape
        escape()
        """)
        msg = Message(msg_id='deprecated-method', node=node,
                      args=('escape', ))
        with self.assertAddsMessages(msg):
            self.checker.visit_call(node)

    def test_unittest_deprecated(self):
        """
        Deprecated methods in package `unittest`
        """
        node = test_utils.extract_node("""
        import unittest
        class TestMe(unittest.TestCase):
            def test(self):
                self.failIf(True)
        """)
        msg = Message(msg_id='deprecated-method', node=node,
                      args=('failIf', ))
        with self.assertAddsMessages(msg):
            self.checker.visit_call(node)

    def test_html_deprecated(self):
        """
        `html` deprecation
        """
        node = test_utils.extract_node("""
        import html.parser
        html.parser.unescape('a')
        """)
        msg = Message(msg_id='deprecated-method', node=node,
                      args=('unescape', ))
        with self.assertAddsMessages(msg):
            self.checker.visit_call(node)

    def test_distutils_deprecated(self):
        """
        `distutil` deprecation
        """
        node = test_utils.extract_node("""
        import distutils
        distutils.command.register.register('a').check_metadata()
        """)
        msg = Message(msg_id='deprecated-method', node=node,
                      args=('check_metadata', ))
        with self.assertAddsMessages(msg):
            self.checker.visit_call(node)

if __name__ == '__main__':
    unittest.main()
