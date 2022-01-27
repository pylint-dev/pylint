# Copyright (c) 2016-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016, 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2019, 2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Damien Baty <damien.baty@polyconseil.fr>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Unit tests utils functions in :mod:`pylint.extensions._check_docs_utils`."""
import astroid
import pytest

from pylint.extensions import _check_docs_utils as utils


@pytest.mark.parametrize(
    "string,count",
    [("abc", 0), ("", 0), ("  abc", 2), ("\n  abc", 0), ("   \n  abc", 3)],
)
def test_space_indentation(string: str, count: int) -> None:
    """Test for pylint_plugin.ParamDocChecker"""
    assert utils.space_indentation(string) == count


@pytest.mark.parametrize(
    "raise_node,expected",
    [
        (
            astroid.extract_node(
                """
    def my_func():
        raise NotImplementedError #@
    """
            ),
            {"NotImplementedError"},
        ),
        (
            astroid.extract_node(
                """
    def my_func():
        raise NotImplementedError("Not implemented!") #@
    """
            ),
            {"NotImplementedError"},
        ),
        (
            astroid.extract_node(
                """
    def my_func():
        try:
            fake_func()
        except RuntimeError:
            raise #@
    """
            ),
            {"RuntimeError"},
        ),
        (
            astroid.extract_node(
                """
    def my_func():
        try:
            fake_func()
        except RuntimeError:
            if another_func():
                raise #@
    """
            ),
            {"RuntimeError"},
        ),
        (
            astroid.extract_node(
                """
    def my_func():
        try:
            fake_func()
        except RuntimeError:
            try:
                another_func()
                raise #@
            except NameError:
                pass
    """
            ),
            {"RuntimeError"},
        ),
        (
            astroid.extract_node(
                """
    def my_func():
        try:
            fake_func()
        except RuntimeError:
            try:
                another_func()
            except NameError:
                raise #@
    """
            ),
            {"NameError"},
        ),
        (
            astroid.extract_node(
                """
    def my_func():
        try:
            fake_func()
        except:
            raise #@
    """
            ),
            set(),
        ),
        (
            astroid.extract_node(
                """
    def my_func():
        try:
            fake_func()
        except (RuntimeError, ValueError):
            raise #@
    """
            ),
            {"RuntimeError", "ValueError"},
        ),
        (
            astroid.extract_node(
                """
    import not_a_module
    def my_func():
        try:
            fake_func()
        except not_a_module.Error:
            raise #@
    """
            ),
            set(),
        ),
    ],
)
def test_exception(raise_node, expected):
    found_nodes = utils.possible_exc_types(raise_node)
    for node in found_nodes:
        assert isinstance(node, astroid.nodes.ClassDef)
    assert {node.name for node in found_nodes} == expected
