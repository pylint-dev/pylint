# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import astroid

from pylint.extensions import function_return_not_assigned
from pylint.testutils import CheckerTestCase, MessageTest


class TestUnassignedFunctionCall(CheckerTestCase):
    CHECKER_CLASS = function_return_not_assigned.FunctionReturnNotAssignedChecker

    def test_simple_func(self) -> None:
        node = astroid.extract_node(
            """
                def a():
                    return 1
                a()
            """,
        )
        msg = MessageTest(
            msg_id="function-return-not-assigned",
            node=node,
            line=4,
            end_line=4,
            col_offset=0,
            end_col_offset=3,
        )
        with self.assertAddsMessages(msg):
            self.checker.visit_call(node)

    def test_simple_method(self) -> None:
        node = astroid.extract_node(
            """
                class A:
                    def return_self(self):
                        return self
                a = A()
                a.return_self()
            """,
        )
        msg = MessageTest(
            msg_id="function-return-not-assigned",
            node=node,
            line=6,
            end_line=6,
            col_offset=0,
            end_col_offset=15,
        )
        with self.assertAddsMessages(msg):
            self.checker.visit_call(node)

    def test_simple_method_returns_none(self) -> None:
        node = astroid.extract_node(
            """
                class A:
                    def return_none(self):
                        return None
                a = A()
                a.return_self()
            """,
        )

        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_simple_function_returns_none(self) -> None:
        node = astroid.extract_node(
            """
                def a():
                    print("doing some stuff")
                a()
            """,
        )

        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_unassigned_dataclass_replace(self) -> None:
        node = astroid.extract_node(
            """
                from dataclasses import dataclass, replace

                @dataclass
                class A:
                    a: int

                inst = A(1)
                replace(inst, a=3)
            """,
        )

        msg = MessageTest(
            msg_id="function-return-not-assigned",
            node=node,
            line=9,
            end_line=9,
            col_offset=0,
            end_col_offset=18,
        )

        with self.assertAddsMessages(msg):
            self.checker.visit_call(node)

    def test_unassigned_method_call_on_replaced_dataclass_inst(self) -> None:
        node = astroid.extract_node(
            """
                from dataclasses import dataclass, replace

                @dataclass
                class A:
                    a: int

                    def return_something(self):
                        return self.a

                inst = A(1)
                inst = replace(inst, a=3)
                inst.return_something()
            """,
        )

        msg = MessageTest(
            msg_id="function-return-not-assigned",
            node=node,
            line=13,
            end_line=13,
            col_offset=0,
            end_col_offset=23,
        )

        with self.assertAddsMessages(msg):
            self.checker.visit_call(node)
