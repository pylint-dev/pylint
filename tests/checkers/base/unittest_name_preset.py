# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Unittest for the NameChecker."""

from __future__ import annotations

import unittest

from pylint.checkers import base


class TestNamePresets(unittest.TestCase):
    SNAKE_CASE_NAMES = {"tést_snake_case", "test_snake_case11", "test_https_200"}
    CAMEL_CASE_NAMES = {"téstCamelCase", "testCamelCase11", "testHTTP200"}
    UPPER_CASE_NAMES = {"TÉST_UPPER_CASE", "TEST_UPPER_CASE11", "TEST_HTTP_200"}
    PASCAL_CASE_NAMES = {"TéstPascalCase", "TestPascalCase11", "TestHTTP200"}
    ALL_NAMES = (
        SNAKE_CASE_NAMES | CAMEL_CASE_NAMES | UPPER_CASE_NAMES | PASCAL_CASE_NAMES
    )

    def _test_name_is_correct_for_all_name_types(
        self, naming_style: type[base.NamingStyle], name: str
    ) -> None:
        for name_type in base.KNOWN_NAME_TYPES_WITH_STYLE:
            self._test_is_correct(naming_style, name, name_type)

    def _test_name_is_incorrect_for_all_name_types(
        self, naming_style: type[base.NamingStyle], name: str
    ) -> None:
        for name_type in base.KNOWN_NAME_TYPES_WITH_STYLE:
            self._test_is_incorrect(naming_style, name, name_type)

    def _test_should_always_pass(self, naming_style: type[base.NamingStyle]) -> None:
        always_pass_data = [
            ("__add__", "method"),
            ("__set_name__", "method"),
            ("__version__", "const"),
            ("__author__", "const"),
        ]
        for name, name_type in always_pass_data:
            self._test_is_correct(naming_style, name, name_type)

    @staticmethod
    def _test_is_correct(
        naming_style: type[base.NamingStyle], name: str, name_type: str
    ) -> None:
        rgx = naming_style.get_regex(name_type)
        fail = f"{name!r} does not match pattern {rgx!r} (style: {naming_style}, type: {name_type})"
        assert rgx.match(name), fail

    @staticmethod
    def _test_is_incorrect(
        naming_style: type[base.NamingStyle], name: str, name_type: str
    ) -> None:
        rgx = naming_style.get_regex(name_type)
        fail = f"{name!r} not match pattern {rgx!r} (style: {naming_style}, type: {name_type})"
        assert not rgx.match(name), fail

    def test_snake_case(self) -> None:
        naming_style = base.SnakeCaseStyle

        for name in self.SNAKE_CASE_NAMES:
            self._test_name_is_correct_for_all_name_types(naming_style, name)
        for name in self.ALL_NAMES - self.SNAKE_CASE_NAMES:
            self._test_name_is_incorrect_for_all_name_types(naming_style, name)

        self._test_should_always_pass(naming_style)

    def test_camel_case(self) -> None:
        naming_style = base.CamelCaseStyle

        for name in self.CAMEL_CASE_NAMES:
            self._test_name_is_correct_for_all_name_types(naming_style, name)
        for name in self.ALL_NAMES - self.CAMEL_CASE_NAMES:
            self._test_name_is_incorrect_for_all_name_types(naming_style, name)

        self._test_should_always_pass(naming_style)

    def test_upper_case(self) -> None:
        naming_style = base.UpperCaseStyle

        for name in self.UPPER_CASE_NAMES:
            self._test_name_is_correct_for_all_name_types(naming_style, name)
        for name in self.ALL_NAMES - self.UPPER_CASE_NAMES:
            self._test_name_is_incorrect_for_all_name_types(naming_style, name)
        self._test_name_is_incorrect_for_all_name_types(naming_style, "UPPERcase")

        self._test_should_always_pass(naming_style)

    def test_pascal_case(self) -> None:
        naming_style = base.PascalCaseStyle

        for name in self.PASCAL_CASE_NAMES:
            self._test_name_is_correct_for_all_name_types(naming_style, name)
        for name in self.ALL_NAMES - self.PASCAL_CASE_NAMES:
            self._test_name_is_incorrect_for_all_name_types(naming_style, name)

        self._test_should_always_pass(naming_style)
