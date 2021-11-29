# Copyright (c) 2016-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016, 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2016 Glenn Matthews <glenn@e-dad.net>
# Copyright (c) 2016 Moises Lopez <moylop260@vauxoo.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Zeb Nicholls <zebedee.nicholls@climate-energy-college.org>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Unit tests for the return documentation checking in the
`DocstringChecker` in :mod:`pylint.extensions.check_docs`
"""


import astroid

from pylint.extensions.docparams import DocstringParameterChecker
from pylint.testutils import CheckerTestCase, MessageTest


class TestDocstringCheckerReturn(CheckerTestCase):
    """Tests for pylint_plugin.RaiseDocChecker"""

    CHECKER_CLASS = DocstringParameterChecker

    def test_ignores_google_redundant_return_doc_multiple_returns(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns:
                int or None: One, or sometimes None.
            """
            if a_func():
                return None
            return 1
        '''
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_warns_google_redundant_return_doc_yield(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns:
                int: One
            """
            yield 1
        '''
        )
        with self.assertAddsMessages(
            MessageTest(msg_id="redundant-returns-doc", node=node)
        ):
            self.checker.visit_functiondef(node)

    def test_warns_numpy_redundant_return_doc_yield(self) -> None:
        node = astroid.extract_node(
            '''
        def my_func(self):
            """This is a docstring.

            Returns
            -------
                int
                    One
            """
            yield 1
        '''
        )
        with self.assertAddsMessages(
            MessageTest(msg_id="redundant-returns-doc", node=node)
        ):
            self.checker.visit_functiondef(node)
