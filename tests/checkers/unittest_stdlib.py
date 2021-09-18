# Copyright (c) 2015-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Cezar <celnazli@bitdefender.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2017 Martin <MartinBasti@users.noreply.github.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import contextlib
from typing import Any, Callable, Iterator, Optional, Union

import astroid
from astroid import nodes
from astroid.manager import AstroidManager
from astroid.nodes.node_classes import AssignAttr, Name

from pylint.checkers import stdlib
from pylint.interfaces import UNDEFINED
from pylint.testutils import CheckerTestCase, OutputMessage


@contextlib.contextmanager
def _add_transform(
    manager: AstroidManager,
    node: type,
    transform: Callable,
    predicate: Optional[Any] = None,
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
        occurred (how an AssignAttr got to be the result of a function inference beats me..)"""

        def infer_func(
            node: Name, context: Optional[Any] = None
        ) -> Iterator[
            Union[Iterator, Iterator[AssignAttr]]
        ]:  # pylint: disable=unused-argument
            new_node = nodes.AssignAttr(attrname="alpha", parent=node)
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

    def test_copy_environ(self) -> None:
        # shallow copy of os.environ should be reported
        node = astroid.extract_node(
            """
        import copy, os
        copy.copy(os.environ)
        """
        )
        with self.assertAddsMessages(
            OutputMessage(
                msg_id="shallow-copy-environ", node=node, confidence=UNDEFINED
            )
        ):
            self.checker.visit_call(node)

    def test_copy_environ_hidden(self) -> None:
        # shallow copy of os.environ should be reported
        # hide function names to be sure that checker is not just matching text
        node = astroid.extract_node(
            """
        from copy import copy as test_cp
        import os as o
        test_cp(o.environ)
        """
        )
        with self.assertAddsMessages(
            OutputMessage(
                msg_id="shallow-copy-environ", node=node, confidence=UNDEFINED
            )
        ):
            self.checker.visit_call(node)

    def test_copy_dict(self) -> None:
        # copy of dict is OK
        node = astroid.extract_node(
            """
        import copy
        test_dict = {}
        copy.copy(test_dict)
        """
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_copy_uninferable(self) -> None:
        # copy of uninferable object should not raise exception, nor make
        # the checker crash
        node = astroid.extract_node(
            """
        import copy
        from missing_library import MissingObject
        copy.copy(MissingObject)
        """
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_deepcopy_environ(self) -> None:
        # deepcopy of os.environ is OK
        node = astroid.extract_node(
            """
        import copy, os
        copy.deepcopy(os.environ)
        """
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)
