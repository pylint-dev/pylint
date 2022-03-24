# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Basic checker for Python code."""

__all__ = [
    "NameChecker",
    "NamingStyle",
    "KNOWN_NAME_TYPES_WITH_STYLE",
    "SnakeCaseStyle",
    "CamelCaseStyle",
    "UpperCaseStyle",
    "PascalCaseStyle",
    "AnyStyle",
]

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers.base.basic_checker import BasicChecker
from pylint.checkers.base.basic_error_checker import BasicErrorChecker
from pylint.checkers.base.comparison_checker import ComparisonChecker
from pylint.checkers.base.docstring_checker import DocStringChecker
from pylint.checkers.base.name_checker import (
    KNOWN_NAME_TYPES_WITH_STYLE,
    AnyStyle,
    CamelCaseStyle,
    NamingStyle,
    PascalCaseStyle,
    SnakeCaseStyle,
    UpperCaseStyle,
)
from pylint.checkers.base.name_checker.checker import NameChecker
from pylint.checkers.base.pass_checker import PassChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


UNITTEST_CASE = "unittest.case"


LOOPLIKE_NODES = (
    nodes.For,
    nodes.ListComp,
    nodes.SetComp,
    nodes.DictComp,
    nodes.GeneratorExp,
)


def in_loop(node: nodes.NodeNG) -> bool:
    """Return whether the node is inside a kind of for loop."""
    return any(isinstance(parent, LOOPLIKE_NODES) for parent in node.node_ancestors())


def in_nested_list(nested_list, obj):
    """Return true if the object is an element of <nested_list> or of a nested
    list
    """
    for elmt in nested_list:
        if isinstance(elmt, (list, tuple)):
            if in_nested_list(elmt, obj):
                return True
        elif elmt == obj:
            return True
    return False


def register(linter: "PyLinter") -> None:
    linter.register_checker(BasicErrorChecker(linter))
    linter.register_checker(BasicChecker(linter))
    linter.register_checker(NameChecker(linter))
    linter.register_checker(DocStringChecker(linter))
    linter.register_checker(PassChecker(linter))
    linter.register_checker(ComparisonChecker(linter))
