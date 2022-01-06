import sys

import astroid
import pytest
from astroid import nodes

import pylint.checkers.non_ascii_names
import pylint.interfaces
import pylint.testutils


class TestNonAsciiChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = pylint.checkers.non_ascii_names.NonAsciiNamesChecker
    checker: pylint.checkers.non_ascii_names.NonAsciiNamesChecker

    EXPECTED_MSG = "non-ascii-name"

    def test_get_module_names(self):
        """The static function _get_modules_names shall resolve module names correctly"""
        assert self.CHECKER_CLASS._get_module_names("foo.bar.test") == [
            "foo",
            "bar",
            "test",
        ]
        assert self.CHECKER_CLASS._get_module_names("foo.bar", "test") == [
            "foo",
            "bar",
            "test",
        ]

    @pytest.mark.skipif(
        sys.version_info < (3, 8), reason="requires python3.8 or higher"
    )
    def test_kwargs_and_position_only(self):
        """Even the new position only and keyword only should be found"""
        node = astroid.extract_node(
            """
                def name(
                    ok,
                    not_økay,
                    not_okay_defaułt=None,
                    /,
                    p_or_kw_okay=None,
                    p_or_kw_not_økay=None,
                    *,
                    kw_arg_okay,
                    kw_arg_not_økay,
                ):
                    ...
            """
        )
        assert isinstance(node, nodes.FunctionDef)
        arguments: nodes.Arguments = node.args

        posargs = list(arguments.posonlyargs)
        args = list(arguments.args)
        kwargs = list(arguments.kwonlyargs)

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id=self.EXPECTED_MSG,
                node=posargs[1],
                args=("Argument", "not_økay"),
                confidence=pylint.interfaces.HIGH,
            ),
            pylint.testutils.MessageTest(
                msg_id=self.EXPECTED_MSG,
                node=posargs[2],
                args=("Argument", "not_okay_defaułt"),
                confidence=pylint.interfaces.HIGH,
            ),
            pylint.testutils.MessageTest(
                msg_id=self.EXPECTED_MSG,
                node=args[1],
                args=("Argument", "p_or_kw_not_økay"),
                confidence=pylint.interfaces.HIGH,
            ),
            pylint.testutils.MessageTest(
                msg_id=self.EXPECTED_MSG,
                node=kwargs[1],
                args=("Argument", "kw_arg_not_økay"),
                confidence=pylint.interfaces.HIGH,
            ),
            ignore_position=True,
        ):
            self.checker.visit_functiondef(node)

    @pytest.mark.parametrize(
        "code, assign_type",
        [
            pytest.param(
                """
                try:
                    ...
                except ValueError as łol: #@
                    ...
                """,
                "Variable",
                id="try-except",
            ),
            pytest.param(
                """
                class FooBar:
                    łol = "test" #@
                """,
                "Attribute",
                id="class_attribute",
            ),
            pytest.param(
                """
                łol = "test" #@
                """,
                "Variable",
                id="global_assign",
            ),
            pytest.param(
                """
                def foobar():
                    łol="test"  #@
                """,
                "Variable",
                id="function_variable",
            ),
            pytest.param(
                """
                for łol in os.listdir("."):  #@
                    ...
                """,
                "Variable",
                id="for_loop_variable",
            ),
            pytest.param(
                """
                [łoł
                    for łol in os.listdir(".")  #@
                ]
                """,
                "Variable",
                id="inline_for_loop_variable",
            ),
        ],
    )
    def test_assignname(
        self,
        code: str,
        assign_type: str,
    ):
        """Variables defined no matter where, should be checked for non ascii"""
        assign_node = astroid.extract_node(code)

        if not isinstance(assign_node, nodes.AssignName):
            # For some elements we can't directly extract the assign
            # node, so we have to manually look in the children for it
            for child in assign_node.get_children():
                if isinstance(child, nodes.AssignName):
                    assign_node = child
                    break

        # Just to make sure we found the correct node
        assert isinstance(assign_node, nodes.AssignName)

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id=self.EXPECTED_MSG,
                node=assign_node,
                args=(assign_type, "łol"),
                confidence=pylint.interfaces.HIGH,
            ),
            ignore_position=True,
        ):
            self.checker.visit_assignname(assign_node)

    def test_class_definition(self):
        node = astroid.extract_node(
            """
            class FooBär: #@
                ...
            """
        )
        assert isinstance(node, nodes.ClassDef)

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id=self.EXPECTED_MSG,
                node=node,
                args=("Class", "FooBär"),
                confidence=pylint.interfaces.HIGH,
                line=2,
                col_offset=0,
                # pylint: disable-next=fixme
                # TODO: Maybe we have to select something different
                #       here, as line 3 is not that thing we expect
                end_line=3,
                end_col_offset=7,
            )
        ):
            self.checker.visit_classdef(node)

    def test_import_ignore_star(self):
        """Special case from xyz import *, where '*' is not A-Za-z0-9 but still valid"""
        node = astroid.parse("from urllib.parse import *")

        with self.assertAddsMessages():
            self.walk(node)
