# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Unit tests for utils functions in :mod:`pylint.extensions._check_docs_utils`."""

from __future__ import annotations

import astroid
import pytest
from astroid import nodes

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
def test_exception(raise_node: nodes.NodeNG, expected: set[str]) -> None:
    found_nodes = utils.possible_exc_types(raise_node)
    for node in found_nodes:
        assert isinstance(node, astroid.nodes.ClassDef)
    assert {node.name for node in found_nodes} == expected


def test_possible_exc_types_raising_potential_none() -> None:
    raise_node = astroid.extract_node(
        """
    def a():
        return
    raise a()  #@
    """
    )
    assert utils.possible_exc_types(raise_node) == set()


@pytest.mark.parametrize(
    "code",
    [
        """
    def my_func():
        raise sum  #@
    """,
        """
    import os
    def my_func():
        raise os  #@
    """,
        """
    def my_func():
        try:
            fake_func()
        except sum:
            raise  #@
    """,
    ],
)
def test_possible_exc_types_non_exception(code: str) -> None:
    """Inference is not restricted to exception classes.

    A name can resolve to a function or a module, neither of which implements
    ``ancestors()``; such objects must not be reported as raised exceptions.
    """
    raise_node = astroid.extract_node(code)
    assert utils.possible_exc_types(raise_node) == set()


def test_possible_exc_types_instance() -> None:
    """An exception *instance* is kept.

    It is not a ``ClassDef``, but it proxies ``name`` and ``ancestors`` to the
    class it wraps, so it is still usable by the callers.
    """
    raise_node = astroid.extract_node(
        """
    def my_func():
        err = ValueError("hi")
        raise err  #@
    """
    )
    found_nodes = utils.possible_exc_types(raise_node)
    assert {node.name for node in found_nodes} == {"ValueError"}
    assert {ancestor.name for node in found_nodes for ancestor in node.ancestors()} >= {
        "Exception"
    }
