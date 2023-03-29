# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Unittest for the NameChecker."""

import re

import astroid

from pylint.checkers import base
from pylint.interfaces import HIGH
from pylint.testutils import CheckerTestCase, MessageTest, set_config


class TestMultiNamingStyle(CheckerTestCase):
    CHECKER_CLASS = base.NameChecker

    MULTI_STYLE_RE = re.compile("(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$")

    @set_config(class_rgx=MULTI_STYLE_RE)
    def test_multi_name_detection_majority(self) -> None:
        classes = astroid.extract_node(
            """
        class classb(object): #@
            pass
        class CLASSA(object): #@
            pass
        class CLASSC(object): #@
            pass
        """
        )
        message = MessageTest(
            "invalid-name",
            node=classes[0],
            args=(
                "Class",
                "classb",
                "the `UP` group in the '(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$' pattern",
            ),
            confidence=HIGH,
            line=2,
            col_offset=0,
            end_line=2,
            end_col_offset=12,
        )
        with self.assertAddsMessages(message):
            cls = None
            for cls in classes:
                self.checker.visit_classdef(cls)
            if cls:
                self.checker.leave_module(cls.root)

    @set_config(class_rgx=MULTI_STYLE_RE)
    def test_multi_name_detection_first_invalid(self) -> None:
        classes = astroid.extract_node(
            """
        class class_a(object): #@
            pass
        class classb(object): #@
            pass
        class CLASSC(object): #@
            pass
        """
        )
        messages = [
            MessageTest(
                "invalid-name",
                node=classes[0],
                args=(
                    "Class",
                    "class_a",
                    "'(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$' pattern",
                ),
                confidence=HIGH,
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=13,
            ),
            MessageTest(
                "invalid-name",
                node=classes[2],
                args=(
                    "Class",
                    "CLASSC",
                    "the `down` group in the '(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$' pattern",
                ),
                confidence=HIGH,
                line=6,
                col_offset=0,
                end_line=6,
                end_col_offset=12,
            ),
        ]
        with self.assertAddsMessages(*messages):
            cls = None
            for cls in classes:
                self.checker.visit_classdef(cls)
            if cls:
                self.checker.leave_module(cls.root)

    @set_config(
        method_rgx=MULTI_STYLE_RE,
        function_rgx=MULTI_STYLE_RE,
        name_group=("function:method",),
    )
    def test_multi_name_detection_group(self) -> None:
        function_defs = astroid.extract_node(
            """
        class First(object):
            def func(self): #@
                pass

        def FUNC(): #@
            pass
        """,
            module_name="test",
        )
        message = MessageTest(
            "invalid-name",
            node=function_defs[1],
            args=(
                "Function",
                "FUNC",
                "the `down` group in the '(?:(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$' pattern",
            ),
            confidence=HIGH,
            line=6,
            col_offset=0,
            end_line=6,
            end_col_offset=8,
        )
        with self.assertAddsMessages(message):
            func = None
            for func in function_defs:
                self.checker.visit_functiondef(func)
            if func:
                self.checker.leave_module(func.root)

    @set_config(
        function_rgx=re.compile("(?:(?P<ignore>FOO)|(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$")
    )
    def test_multi_name_detection_exempt(self) -> None:
        function_defs = astroid.extract_node(
            """
        def FOO(): #@
            pass
        def lower(): #@
            pass
        def FOO(): #@
            pass
        def UPPER(): #@
            pass
        """
        )
        message = MessageTest(
            "invalid-name",
            node=function_defs[3],
            args=(
                "Function",
                "UPPER",
                "the `down` group in the '(?:(?P<ignore>FOO)|(?P<UP>[A-Z]+)|(?P<down>[a-z]+))$' pattern",
            ),
            confidence=HIGH,
            line=8,
            col_offset=0,
            end_line=8,
            end_col_offset=9,
        )
        with self.assertAddsMessages(message):
            func = None
            for func in function_defs:
                self.checker.visit_functiondef(func)
            if func:
                self.checker.leave_module(func.root)
