# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from collections.abc import Iterable

import astroid
import pytest
from astroid import nodes

import pylint.checkers.non_ascii_names
import pylint.interfaces
import pylint.testutils


class TestNonAsciiChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = pylint.checkers.non_ascii_names.NonAsciiNameChecker
    checker: pylint.checkers.non_ascii_names.NonAsciiNameChecker

    def test_kwargs_and_position_only(self) -> None:
        """Even the new position only and keyword only should be found."""
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
        arguments = node.args

        posargs = list(arguments.posonlyargs)
        args = list(arguments.args)
        kwargs = list(arguments.kwonlyargs)

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="non-ascii-name",
                node=posargs[1],
                args=("Argument", "not_økay"),
                confidence=pylint.interfaces.HIGH,
            ),
            pylint.testutils.MessageTest(
                msg_id="non-ascii-name",
                node=posargs[2],
                args=("Argument", "not_okay_defaułt"),
                confidence=pylint.interfaces.HIGH,
            ),
            pylint.testutils.MessageTest(
                msg_id="non-ascii-name",
                node=args[1],
                args=("Argument", "p_or_kw_not_økay"),
                confidence=pylint.interfaces.HIGH,
            ),
            pylint.testutils.MessageTest(
                msg_id="non-ascii-name",
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
    ) -> None:
        """Variables defined no matter where, should be checked for non ascii."""
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
                msg_id="non-ascii-name",
                node=assign_node,
                args=(assign_type, "łol"),
                confidence=pylint.interfaces.HIGH,
            ),
            ignore_position=True,
        ):
            self.checker.visit_assignname(assign_node)

    @pytest.mark.parametrize(
        "import_statement, wrong_name",
        [
            pytest.param("import fürimma", "fürimma", id="bad_single_main_module"),
            pytest.param(
                "import fürimma as okay",
                None,
                id="bad_single_main_module_with_okay_alias",
            ),
            pytest.param(
                "import fürimma, pathlib",
                "fürimma",
                id="bad_single_main_module_with_stdlib_import",
            ),
            pytest.param(
                "import pathlib, os, foobar, fürimma",
                "fürimma",
                id="stdlib_with_bad_single_main_module",
            ),
            pytest.param(
                "import pathlib, os, foobar, sys as systëm",
                "systëm",
                id="stdlib_with_bad_alias",
            ),
            pytest.param(
                "import fürimma as okay, pathlib",
                None,
                id="bad_single_main_module_with_okay_alias_with_stdlib_import",
            ),
            pytest.param(
                "import fürimma.submodule", "fürimma.submodule", id="bad_main_module"
            ),
            pytest.param(
                "import fürimma.submodule as submodule",
                None,
                id="bad_main_module_with_okay_alias",
            ),
            pytest.param(
                "import main_module.fürimma", "main_module.fürimma", id="bad_submodule"
            ),
            pytest.param(
                "import main_module.fürimma as okay",
                None,
                id="bad_submodule_with_okay_alias",
            ),
            pytest.param(
                "import main_module.fürimma as not_økay",
                "not_økay",
                id="bad_submodule_with_bad_alias",
            ),
            pytest.param(
                "from foo.bar import function", None, id="from_okay_module_import_okay"
            ),
            pytest.param(
                "from foo.bär import function", None, id="from_bad_module_import_okay"
            ),
            pytest.param(
                "from foo.bar import functiøn",
                "functiøn",
                id="from_okay_module_import_bad",
            ),
            pytest.param(
                "from foo.bar import functiøn as function",
                None,
                id="from_okay_module_import_bad_as_good",
            ),
            pytest.param(
                "from foo.bär import functiøn as function",
                None,
                id="from_bad_module_import_bad_as_good",
            ),
            pytest.param(
                "from foo.bar import functiøn as føl",
                "føl",
                id="from_okay_module_import_bad_as_bad",
            ),
            pytest.param(
                "from foo.bar import functiøn as good, bäd",
                "bäd",
                id="from_okay_module_import_bad_as_good_and_bad",
            ),
            pytest.param(
                "from foo.bar import functiøn as good, bäd",
                "bäd",
                id="from_okay_module_import_bad_as_good_and_bad",
            ),
            pytest.param(
                "from foo.bar import functiøn as good, *",
                # We still have functiøn within our namespace and could detect this
                # But to do this properly we would need to check all `*` imports
                # -> Too much effort!
                "functiøn",
                id="from_okay_module_import_bad_as_good_and_star",
                marks=pytest.mark.xfail(
                    reason="We don't know what is imported when using star"
                ),
            ),
        ],
    )
    def test_check_import(self, import_statement: str, wrong_name: str | None) -> None:
        """We expect that for everything that user can change there is a message."""
        node = astroid.extract_node(f"{import_statement} #@")

        expected_msgs: Iterable[pylint.testutils.MessageTest] = tuple()

        if wrong_name:
            expected_msgs = (
                pylint.testutils.MessageTest(
                    msg_id="non-ascii-module-import",
                    node=node,
                    args=("Module", wrong_name),
                    confidence=pylint.interfaces.HIGH,
                ),
            )
        with self.assertAddsMessages(*expected_msgs, ignore_position=True):
            if import_statement.startswith("from"):
                assert isinstance(node, nodes.ImportFrom)
                self.checker.visit_importfrom(node)
            else:
                assert isinstance(node, nodes.Import)
                self.checker.visit_import(node)
