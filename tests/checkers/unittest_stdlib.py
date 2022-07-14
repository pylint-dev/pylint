# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import contextlib
from collections.abc import Callable, Iterator
from typing import Any

import astroid
from astroid import nodes
from astroid.manager import AstroidManager

from pylint.checkers import stdlib
from pylint.testutils import CheckerTestCase


@contextlib.contextmanager
def _add_transform(
    manager: AstroidManager,
    node: type,
    transform: Callable,
    predicate: Any | None = None,
) -> Iterator:
    manager.register_transform(node, transform, predicate)
    try:
        yield
    finally:
        manager.unregister_transform(node, transform, predicate)


class TestStdlibChecker(CheckerTestCase):
    CHECKER_CLASS = stdlib.StdlibChecker

    def test_deprecated_no_qname_on_unexpected_nodes(self) -> None:
        """Test that we don't crash on nodes which don't have a qname method.

        While this test might seem weird since it uses a transform, it's actually testing a crash
        that happened in production, but there was no way to retrieve the code for which this
        occurred (how an AssignAttr got to be the result of a function inference beats me...)
        """

        def infer_func(
            inner_node: nodes.Name,
            context: Any | None = None,  # pylint: disable=unused-argument
        ) -> Iterator[Iterator | Iterator[nodes.AssignAttr]]:
            new_node = nodes.AssignAttr(attrname="alpha", parent=inner_node)
            yield new_node

        manager = astroid.MANAGER
        transform = astroid.inference_tip(infer_func)
        with _add_transform(manager, nodes.Name, transform):
            node = astroid.extract_node(
                """
            call_something()
            """
            )
            with self.assertNoMessages():
                self.checker.visit_call(node)
