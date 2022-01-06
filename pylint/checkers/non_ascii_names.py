# Copyright (c) 2021-2022 Carli Freudenberg <carli.freudenberg@energymeteo.de>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
"""All alphanumeric unicode character are allowed in Python but due
to similarities in how they look they can be confused.

See: https://www.python.org/dev/peps/pep-0672/#confusable-characters-in-identifiers

The following checkers are intended to make users are aware of these issues.
"""

import re
import sys
from typing import Iterable, List, Optional, Union

from astroid import nodes

import pylint.checkers.utils
from pylint import interfaces
from pylint.constants import HUMAN_READABLE_TYPES
from pylint.lint import PyLinter

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol


if sys.version_info[:2] >= (3, 7):
    # pylint: disable-next=fixme
    # TODO: Remove after 3.6 has been deprecated
    Py37Str = str
else:

    class Py37Str(str):
        # Allow Python 3.6 compatibility
        def isascii(self: str) -> bool:
            return all("\u0000" <= x <= "\u007F" for x in self)


class _AsciiOnlyCheckedNode(Protocol):
    _is_ascii_only: bool


class NonAsciiNamesChecker(pylint.checkers.BaseChecker):
    """A strict name checker only allowing ASCII

    If your programming guideline defines that you are programming in English,
    then there should be no need for non ASCII characters in Python Names.
    Everybody else can simply not use this check.

    Note: This check only checks Names, so it ignores the content of
          docstrings and comments!
    """

    __implements__ = interfaces.IAstroidChecker
    priority = -1

    msgs = {
        "C0144": (
            '%s name "%s" contains a non-ASCII character, rename it or use an alias for import',
            "non-ascii-name",
            (
                "Used when the name contains at least one non-ASCII unicode character. "
                "See https://www.python.org/dev/peps/pep-0672/#confusable-characters-in-identifiers"
                " for a background why this could be bad."
            ),
        ),
    }

    name = "NonASCII-Checker"

    def __init__(self, linter: PyLinter) -> None:
        super().__init__(linter)
        self._non_ascii_rgx_compiled = re.compile("[^A-Za-z0-9_]")

    def _raise_name_warning(
        self,
        node: nodes.NodeNG,
        node_type: str,
        name: str,
    ) -> None:
        type_label = HUMAN_READABLE_TYPES[node_type]
        args = (type_label.capitalize(), name)

        self.add_message(
            "non-ascii-name", node=node, args=args, confidence=interfaces.HIGH
        )

    def _check_name(
        self,
        node_type: str,
        names: Union[str, List[str]],
        node: Union[nodes.NodeNG, _AsciiOnlyCheckedNode],
    ) -> None:
        """Check whether a name is using non-ASCII characters.

        Also set the dynamic attribute ``_is_ascii_only`` that is used to
        determine if a node has been already checked, so we don't have to handle
        too many edge cases.
        """
        if not isinstance(names, list):
            names = [names]

        current_state = getattr(node, "_is_ascii_only", True)
        for name in names:
            if name is None:
                # For some nodes i.e. *kwargs from a dict, the name will be empty
                continue
            if not (
                Py37Str(name).isascii()
                and self._non_ascii_rgx_compiled.match(name) is None
            ):
                # Note that we require the `.isascii` method as it is fast and
                # handles the complexities of unicode, so we can use simple regex.
                self._raise_name_warning(node, node_type, name)
                current_state = False

        node._is_ascii_only = current_state  # pylint: disable=protected-access

    def _recursive_check_names(self, args: Iterable[nodes.AssignName]) -> None:
        """check names in a possibly recursive list <arg>"""
        for arg in args:
            if isinstance(arg, nodes.AssignName):
                self._check_name("argument", arg.name, arg)
            else:
                # pylint: disable-next=fixme
                # TODO: Check if we can remove this branch because of
                #       the up to date astroid version used
                self._recursive_check_names(arg.elts)

    @pylint.checkers.utils.check_messages("non-ascii-name")
    def visit_module(self, node: nodes.Module) -> None:
        # pylint: disable-next=fixme
        # TODO check how the node name is defined when calling the real checker
        #      in the test using the astroid manager the node.name attribute corresponds
        #      to the filename -> so we always have ".py" as result of the following
        #      function.
        #      It would be nice if we could check for an ASCII filename, if not done
        #      already by other checkers...
        self._check_name("module", node.name.split(".")[-1], node)

    @pylint.checkers.utils.check_messages("non-ascii-name")
    def visit_functiondef(
        self, node: Union[nodes.FunctionDef, nodes.AsyncFunctionDef]
    ) -> None:
        self._check_name("function", node.name, node)

        # Check argument names
        arguments = node.args

        # Check position only arguments
        if arguments.posonlyargs is not None:
            for pos_only_arg in arguments.posonlyargs:
                self._check_name("argument", pos_only_arg.name, pos_only_arg)

        # Check "normal" arguments
        args = arguments.args
        if args is not None:
            self._recursive_check_names(args)

        # Check key word only arguments
        if arguments.kwonlyargs is not None:
            for kwarg in arguments.kwonlyargs:
                self._check_name("argument", kwarg.name, kwarg)

    visit_asyncfunctiondef = visit_functiondef

    @pylint.checkers.utils.check_messages("non-ascii-name")
    def visit_global(self, node: nodes.Global) -> None:
        for name in node.names:
            self._check_name("const", name, node)

    @pylint.checkers.utils.check_messages("non-ascii-name")
    def visit_assignname(self, node: nodes.AssignName) -> None:
        """check module level assigned names"""
        # The NameChecker from which this Checker originates knows a lot of different
        # versions of variables, i.e. constants, inline variables etc.
        # To simplify we use only `variable` here, as we don't need to apply different
        # rules to different types of variables.
        frame = node.frame()
        assign_type = node.assign_type()
        if isinstance(assign_type, nodes.Comprehension):
            # called inlinevar in NamesChecker
            self._check_name("variable", node.name, node)
        elif isinstance(frame, nodes.Module):
            self._check_name("variable", node.name, node)
        elif isinstance(frame, nodes.FunctionDef):
            if not hasattr(node, "_is_ascii_only"):
                # only check if not already done
                self._check_name("variable", node.name, node)
        elif isinstance(frame, nodes.ClassDef):
            self._check_name("attr", node.name, node)
        else:
            # Just to make sure we check EVERYTHING (!)
            self._check_name("variable", node.name, node)

    @pylint.checkers.utils.check_messages("non-ascii-name")
    def visit_classdef(self, node: nodes.ClassDef) -> None:
        self._check_name("class", node.name, node)
        for attr, anodes in node.instance_attrs.items():
            if not any(node.instance_attr_ancestors(attr)):
                self._check_name("attr", attr, anodes[0])

    @staticmethod
    def _get_module_names(module_name: str, alias: Optional[str] = None) -> List[str]:
        result = module_name.split(".")
        if alias is not None:
            result.append(alias)
        return result

    def _check_module_import(
        self, node: Union[nodes.ImportFrom, nodes.Import], is_import_from: bool = False
    ):
        names = []
        for module_name, alias in node.names:
            names += self._get_module_names(module_name, alias)
        if not (is_import_from and names == ["*"]):
            # Ignore ``from xyz import *``
            self._check_name("module", names, node)

    @pylint.checkers.utils.check_messages("non-ascii-name")
    def visit_import(self, node: nodes.Import) -> None:
        self._check_module_import(node)

    @pylint.checkers.utils.check_messages("non-ascii-name")
    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        self._check_name("module", self._get_module_names(node.modname), node)
        self._check_module_import(node, is_import_from=True)

    @pylint.checkers.utils.check_messages("non-ascii-name")
    def visit_call(self, node: nodes.Call) -> None:
        # lets check if the used keyword args are correct
        for keyword in node.keywords:
            self._check_name("argument", keyword.arg, keyword)


def register(linter: PyLinter) -> None:
    linter.register_checker(NonAsciiNamesChecker(linter))
