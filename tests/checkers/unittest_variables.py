# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import os
import re
import sys
from pathlib import Path

import astroid
import pytest
from astroid import nodes

from pylint.checkers import variables
from pylint.interfaces import HIGH
from pylint.testutils import CheckerTestCase, MessageTest, linter, set_config
from pylint.testutils.reporter_for_tests import GenericTestReporter

REGR_DATA_DIR = str(Path(__file__).parent / ".." / "regrtest_data")


class TestVariablesChecker(CheckerTestCase):
    CHECKER_CLASS = variables.VariablesChecker

    @pytest.mark.parametrize(
        "expression, expected",
        [
            ("(i for _ in [1, 2])", ["i"]),
            ("(value for value in [1, 2] if value == i)", ["i"]),
            ("(value for value in range(i))", []),
            ("(i for i in range(i))", []),
            ("list(i for _ in [1, 2])", []),
            ("collect(i for _ in [1, 2])", []),
            ("tuple(i for _ in [1, 2])", []),
            ("set(i for _ in [1, 2])", []),
            ("frozenset(i for _ in [1, 2])", []),
            ("dict((i, i) for _ in [1, 2])", []),
            ("sum(i for _ in [1, 2])", []),
            ("sum((i for _ in [1, 2]), 0)", []),
            ("sum([], (i for _ in [1, 2]))", ["i"]),
            ("min(i for _ in [1, 2])", []),
            ("max(i for _ in [1, 2])", []),
            ("min((i for _ in [1]), (i for _ in [1]), key=id)", ["i", "i"]),
            ("max((i for _ in [1]), (i for _ in [1]), key=id)", ["i", "i"]),
            ("any(i for _ in [1, 2])", []),
            ("all(i for _ in [1, 2])", []),
            ("sorted(i for _ in [1, 2])", []),
            ("next(i for _ in [1])", []),
            ("next((i for _ in []), None)", []),
            ("next(iter([]), (i for _ in [1]))", ["i"]),
            ("','.join(str(i) for _ in [1])", []),
            ("[].extend(i for _ in [1])", []),
            ("(yield from (i for _ in [1]))", []),
            ("enumerate(i for _ in [1, 2])", ["i"]),
            ("iter(i for _ in [1, 2])", ["i"]),
            ("consume(i for _ in [1, 2])", ["i"]),
            ("unknown(i for _ in [1, 2])", ["i"]),
            ("(value for value in (i for _ in [1, 2]))", ["i"]),
        ],
    )
    def test_generator_loop_captures(
        self, expression: str, expected: list[str]
    ) -> None:
        node = astroid.parse(
            "from builtins import list as collect\n"
            f"def func(consume):\n    for i in [1, 2]:\n        result = {expression}"
        )
        self.walk(node)
        assert [
            message.args
            for message in self.linter.release_messages()
            if message.msg_id == "cell-var-from-loop"
        ] == expected

    def test_generator_passed_to_shadowed_consumer(self) -> None:
        node = astroid.parse("""
        def list(values):
            return values
        class Collector:
            def extend(self, values):
                return values
            join = extend
        for i in [1, 2]:
            result = list(i for _ in [1, 2])
            result = Collector().extend(i for _ in [1, 2])
            result = Collector().join(i for _ in [1, 2])
        """)
        self.walk(node)
        assert [
            message.args
            for message in self.linter.release_messages()
            if message.msg_id == "cell-var-from-loop"
        ] == ["i", "i", "i"]

    def test_generator_in_comprehension_filter_is_not_iterated(self) -> None:
        node = astroid.extract_node("[1 for _ in [1] if (i for _ in [1])]")
        generator = next(node.nodes_of_class(nodes.GeneratorExp))
        assert not self.checker._is_generator_consumed(generator)

    def test_all_elements_without_parent(self) -> None:
        node = astroid.extract_node("__all__ = []")
        node.value.elts.append(nodes.Const("test", parent=None))
        root = node.root()
        with self.assertNoMessages():
            self.checker.visit_module(root)
            self.checker.leave_module(root)


class TestVariablesCheckerWithTearDown(CheckerTestCase):
    CHECKER_CLASS = variables.VariablesChecker

    def setup_method(self) -> None:
        super().setup_method()
        self._to_consume_backup = self.checker._to_consume
        self.checker._to_consume = []

    def teardown_method(self) -> None:
        self.checker._to_consume = self._to_consume_backup

    @set_config(callbacks=("callback_", "_callback"))
    def test_custom_callback_string(self) -> None:
        """Test the --callbacks option works."""
        node = astroid.extract_node("""
        def callback_one(abc):
             ''' should not emit unused-argument. '''
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)
            self.checker.leave_functiondef(node)

        node = astroid.extract_node("""
        def two_callback(abc, defg):
             ''' should not emit unused-argument. '''
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)
            self.checker.leave_functiondef(node)

        node = astroid.extract_node("""
        def normal_func(abc):
             ''' should emit unused-argument. '''
        """)
        with self.assertAddsMessages(
            MessageTest(
                "unused-argument",
                node=node["abc"],
                args="abc",
                confidence=HIGH,
                line=2,
                col_offset=16,
                end_line=2,
                end_col_offset=19,
            )
        ):
            self.checker.visit_functiondef(node)
            self.checker.leave_functiondef(node)

        node = astroid.extract_node("""
        def cb_func(abc):
             ''' Previous callbacks are overridden. '''
        """)
        with self.assertAddsMessages(
            MessageTest(
                "unused-argument",
                node=node["abc"],
                args="abc",
                confidence=HIGH,
                line=2,
                col_offset=12,
                end_line=2,
                end_col_offset=15,
            )
        ):
            self.checker.visit_functiondef(node)
            self.checker.leave_functiondef(node)

    @set_config(redefining_builtins_modules=("os",))
    def test_redefined_builtin_modname_not_ignored(self) -> None:
        node = astroid.parse("""
        from future.builtins import open
        """)
        with self.assertAddsMessages(
            MessageTest(
                "redefined-builtin",
                node=node.body[0],
                args="open",
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=32,
            )
        ):
            self.checker.visit_module(node)

    @set_config(redefining_builtins_modules=("os",))
    def test_redefined_builtin_in_function(self) -> None:
        node = astroid.extract_node("""
        def test():
            from os import open
        """)
        with self.assertNoMessages():
            self.checker.visit_module(node.root())
            self.checker.visit_functiondef(node)

    def test_import_as_underscore(self) -> None:
        node = astroid.parse("""
        import math as _
        """)
        with self.assertNoMessages():
            self.walk(node)

    def test_lambda_in_classdef(self) -> None:
        # Make sure lambda doesn't raises
        # Undefined-method in class def

        # Issue 1824
        # https://github.com/pylint-dev/pylint/issues/1824
        node = astroid.parse("""
        class MyObject(object):
            method1 = lambda func: func()
            method2 = lambda function: function()
        """)
        with self.assertNoMessages():
            self.walk(node)

    def test_nested_lambda(self) -> None:
        """Make sure variables from parent lambdas
        aren't noted as undefined.

        https://github.com/pylint-dev/pylint/issues/760
        """
        node = astroid.parse("""
        lambda x: lambda: x + 1
        """)
        with self.assertNoMessages():
            self.walk(node)

    @set_config(ignored_argument_names=re.compile("arg"))
    def test_ignored_argument_names_no_message(self) -> None:
        """Make sure is_ignored_argument_names properly ignores
        function arguments.
        """
        node = astroid.parse("""
        def fooby(arg):
            pass
        """)
        with self.assertNoMessages():
            self.walk(node)

    @set_config(ignored_argument_names=re.compile("args|kwargs"))
    def test_ignored_argument_names_starred_args(self) -> None:
        node = astroid.parse("""
        def fooby(*args, **kwargs):
            pass
        """)
        with self.assertNoMessages():
            self.walk(node)


class TestMissingSubmodule(CheckerTestCase):
    CHECKER_CLASS = variables.VariablesChecker

    @staticmethod
    def test_package_all() -> None:
        sys.path.insert(0, REGR_DATA_DIR)
        try:
            linter.check([os.path.join(REGR_DATA_DIR, "package_all")])
            assert isinstance(linter.reporter, GenericTestReporter)
            got = linter.reporter.finalize().strip()
            assert got == "E:  3: Undefined variable name 'missing' in __all__"
        finally:
            sys.path.pop(0)


class TestShadowedModuleAlias(CheckerTestCase):
    CHECKER_CLASS = variables.VariablesChecker

    @staticmethod
    def test_no_name_in_module_alias_shadowing() -> None:
        """Regression test for https://github.com/pylint-dev/pylint/issues/10193.

        No false `no-name-in-module` when an alias shadows its base module and
        a function named `format` is called on the alias.
        """
        package_dir = os.path.join(REGR_DATA_DIR, "shadowed_module_alias")
        sys.path.insert(0, package_dir)
        try:
            linter.check([os.path.join(package_dir, "main.py")])
            assert isinstance(linter.reporter, GenericTestReporter)
            assert linter.reporter.finalize().strip() == ""
        finally:
            sys.path.pop(0)


class TestUnusedArgumentInStubFile(CheckerTestCase):
    """A ``.pyi`` body is ``...``, so it cannot use its arguments (#9417)."""

    CHECKER_CLASS = variables.VariablesChecker

    CODE = """
    class TestClient:
        def simulate_get(self, path: str) -> str: ...

    def module_function(value: int) -> int: ...
    """

    def test_no_unused_argument_in_a_stub(self) -> None:
        node = astroid.parse(self.CODE, path="client.pyi")
        with self.assertNoMessages():
            self.walk(node)

    def test_the_same_code_in_a_py_file_still_warns(self) -> None:
        node = astroid.parse(self.CODE, path="client.py")
        self.walk(node)
        assert {
            (message.msg_id, message.args) for message in self.linter.release_messages()
        } == {("unused-argument", "path"), ("unused-argument", "value")}
