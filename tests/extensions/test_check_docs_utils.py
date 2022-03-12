# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

"""Unit tests for utils functions in :mod:`pylint.extensions._check_docs_utils`."""
import astroid
import pytest

from pylint.extensions import _check_docs_utils as utils


@pytest.mark.parametrize(
    "string,count",
    [("abc", 0), ("", 0), ("  abc", 2), ("\n  abc", 0), ("   \n  abc", 3)],
)
def test_space_indentation(string: str, count: int) -> None:
    """Test for pylint_plugin.ParamDocChecker."""
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
