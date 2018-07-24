# Copyright (c) 2018 Alex Itkes

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the accept-expanded-kwargs option for DocstringParameterChecker
"""

import unittest

import astroid
from pylint.testutils import CheckerTestCase, Message, set_config

from pylint.extensions.docparams import DocstringParameterChecker

class TestExpandedKwargsChecker(CheckerTestCase):
    """Tests the accept-expanded-kwargs option for DocstringParameterChecker"""
    CHECKER_CLASS = DocstringParameterChecker
    CONFIG = {
        'accept_expanded_kwargs': True,
    }

    @set_config(accept_expanded_kwargs=False)
    def test_reject_expanded_kwargs(self):
        """Checks whether the checkers works properly with accept_expanded_kwargs=False"""
        node = astroid.extract_node("""
        def doSomething(mandatory, **kwargs):
            '''
            Does something

            :param int mandatory:
                The mandatory argument

            :param dict kwargs:
                Optional parameters, described below.

            :param int alpha:
                First optional argument

            :param int beta:
                Second optional argument

            :returns:
                mandatory * alpha * beta

            :rtype:
                int
            '''
            return mandatory * kwargs.get('alpha', 1) * kwargs.get('beta', 1)
        """)
        with self.assertAddsMessages(
            Message(
                msg_id='differing-param-doc',
                node=node,
                args=('alpha, beta',)),
            Message(
                msg_id='differing-type-doc',
                node=node,
                args=('alpha, beta',)),
        ):
            self.checker.visit_functiondef(node)

    @set_config(accept_expanded_kwargs=True)
    def test_accept_expanded_kwargs(self):
        """Checks whether the checkers works properly with accept_expanded_kwargs=True"""
        node = astroid.extract_node("""
        def doSomething(mandatory, **kwargs):
            '''
            Does something

            :param int mandatory:
                The mandatory argument

            :param dict kwargs:
                Optional parameters, described below.

            :param int alpha:
                First optional argument

            :param int beta:
                Second optional argument

            :returns:
                mandatory * alpha * beta

            :rtype:
                int
            '''
            return mandatory * kwargs.get('alpha', 1) * kwargs.get('beta', 1)
        """)
        with self.assertAddsMessages(
        ):
            self.checker.visit_functiondef(node)

    @set_config(accept_expanded_kwargs=True)
    def test_real_warning(self):
        """Checks whether the checker still detects differing-param-doc if there is no kwargs param"""
        node = astroid.extract_node("""
        def doSomething(mandatory):
            '''
            Does something

            :param int mandatory:
                The mandatory argument

            :param int alpha:
                First optional argument

            :param int beta:
                Second optional argument

            :returns:
                mandatory argument

            :rtype:
                int
            '''
            return mandatory
        """)
        with self.assertAddsMessages(
            Message(
                msg_id='differing-param-doc',
                node=node,
                args=('alpha, beta',)),
            Message(
                msg_id='differing-type-doc',
                node=node,
                args=('alpha, beta',)),
        ):
            self.checker.visit_functiondef(node)
