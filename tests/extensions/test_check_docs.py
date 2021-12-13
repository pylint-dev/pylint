# Copyright (c) 2014-2015 Bruno Daniel <bruno.daniel@blue-yonder.com>
# Copyright (c) 2015-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016-2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2016 Glenn Matthews <glenn@e-dad.net>
# Copyright (c) 2016 Glenn Matthews <glmatthe@cisco.com>
# Copyright (c) 2017, 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2017 Mitar <mitar.github@tnode.com>
# Copyright (c) 2017 John Paraskevopoulos <io.paraskev@gmail.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2018 Adrian Chirieac <chirieacam@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2020 Luigi <luigi.cristofolini@q-ctrl.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Konstantina Saketou <56515303+ksaketou@users.noreply.github.com>
# Copyright (c) 2021 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Logan Miller <14319179+komodo472@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Unit tests for the pylint checkers in :mod:`pylint.extensions.check_docs`,
in particular the parameter documentation checker `DocstringChecker`
"""


import re

import astroid
from astroid import nodes

from pylint.extensions.docparams import DocstringParameterChecker
from pylint.testutils import CheckerTestCase


class TestParamDocChecker(CheckerTestCase):
    """Tests for pylint_plugin.ParamDocChecker"""

    CHECKER_CLASS = DocstringParameterChecker
    CONFIG = {
        "accept_no_param_doc": False,
        "no_docstring_rgx": re.compile("^$"),
        "docstring_min_length": -1,
    }

    def _visit_methods_of_class(self, node: nodes.ClassDef) -> None:
        """Visit all methods of a class node

        :param node: class node
        :type node: :class:`nodes.Class`
        """
        for body_item in node.body:
            if isinstance(body_item, nodes.FunctionDef) and hasattr(body_item, "name"):
                self.checker.visit_functiondef(body_item)

    def test_see_sentence_for_constr_params_in_class(self) -> None:
        """Example usage of "For the parameters, see" in class docstring"""
        node = astroid.extract_node(
            """
        class ClassFoo(object):
            '''docstring foo

            For the parameters, see :func:`bla`
            '''

            def __init__(self, x, y):
                '''init'''
                pass

        """
        )
        with self.assertNoMessages():
            self._visit_methods_of_class(node)

    def test_see_sentence_for_constr_params_in_init(self) -> None:
        """Example usage of "For the parameters, see" in init docstring"""
        node = astroid.extract_node(
            """
        class ClassFoo(object):
            '''foo'''

            def __init__(self, x, y):
                '''docstring foo constructor

                For the parameters, see :func:`bla`
                '''
                pass

        """
        )
        with self.assertNoMessages():
            self._visit_methods_of_class(node)
