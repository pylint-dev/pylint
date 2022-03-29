# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""All alphanumeric unicode character are allowed in Python but due
to similarities in how they look they can be confused.

See: https://www.python.org/dev/peps/pep-0672/#confusable-characters-in-identifiers

The following checkers are intended to make users are aware of these issues.
"""

import sys
from typing import Optional, Union

from astroid import nodes

from pylint import constants, interfaces, lint
from pylint.checkers import base_checker, utils

if sys.version_info[:2] >= (3, 7):
    # pylint: disable-next=fixme
    # TODO: Remove after 3.6 has been deprecated
    Py37Str = str
else:

    class Py37Str(str):
        # Allow Python 3.6 compatibility
        def isascii(self: str) -> bool:
            return all("\u0000" <= x <= "\u007F" for x in self)


NON_ASCII_HELP = (
    "Used when the name contains at least one non-ASCII unicode character. "
    "See https://www.python.org/dev/peps/pep-0672/#confusable-characters-in-identifiers"
    " for a background why this could be bad. \n"
    "If your programming guideline defines that you are programming in "
    "English, then there should be no need for non ASCII characters in "
    "Python Names. If not you can simply disable this check."
)


class NonAsciiNameChecker(base_checker.BaseChecker):
    """A strict name checker only allowing ASCII.

    Note: This check only checks Names, so it ignores the content of
          docstrings and comments!
    """

    __implements__ = interfaces.IAstroidChecker
    priority = -1

    msgs = {
        "C2401": (
            '%s name "%s" contains a non-ASCII character, consider renaming it.',
            "non-ascii-name",
            NON_ASCII_HELP,
            {"old_names": [("C0144", "old-non-ascii-name")]},
        ),
        # First %s will always be "file"
        "W2402": (
            (
                '%s name "%s" contains a non-ASCII character. PEP 3131 only allows '
                "non-ascii identifiers, not file names."
            ),
            "non-ascii-file-name",
            (
                # Some = PyCharm at the time of writing didn't display the non_ascii_name_loł
                # files and had big troubles with git.
                # Probably only a bug shows the problem quite good.
                # That's also why this is a warning and not only a convention!
                "Some editors don't support non-ASCII file names properly. "
                "Even though Python supports UTF-8 files since Python 3.5 this isn't "
                "recommended for interoperability. Further reading:\n"
                "- https://www.python.org/dev/peps/pep-0489/#export-hook-name\n"
                "- https://www.python.org/dev/peps/pep-0672/#confusable-characters-in-identifiers\n"
                "- https://bugs.python.org/issue20485"
            ),
        ),
        # First %s will always be "module"
        "C2403": (
            '%s name "%s" contains a non-ASCII character, use an ASCII-only alias for import.',
            "non-ascii-module-import",
            NON_ASCII_HELP,
        ),
    }

    name = "NonASCII-Checker"

    def _check_name(
        self, node_type: str, name: Optional[str], node: nodes.NodeNG
    ) -> None:
        """Check whether a name is using non-ASCII characters."""

        if name is None:
            # For some nodes i.e. *kwargs from a dict, the name will be empty
            return

        if not (Py37Str(name).isascii()):
            type_label = constants.HUMAN_READABLE_TYPES[node_type]
            args = (type_label.capitalize(), name)

            msg = "non-ascii-name"

            # Some node types have customized messages
            if node_type == "file":
                msg = "non-ascii-file-name"
            elif node_type == "module":
                msg = "non-ascii-module-import"

            self.add_message(msg, node=node, args=args, confidence=interfaces.HIGH)

    @utils.check_messages("non-ascii-name")
    def visit_module(self, node: nodes.Module) -> None:
        self._check_name("file", node.name.split(".")[-1], node)

    @utils.check_messages("non-ascii-name")
    def visit_functiondef(
        self, node: Union[nodes.FunctionDef, nodes.AsyncFunctionDef]
    ) -> None:
        self._check_name("function", node.name, node)

        # Check argument names
        arguments = node.args

        # Check position only arguments
        if arguments.posonlyargs:
            for pos_only_arg in arguments.posonlyargs:
                self._check_name("argument", pos_only_arg.name, pos_only_arg)

        # Check "normal" arguments
        if arguments.args:
            for arg in arguments.args:
                self._check_name("argument", arg.name, arg)

        # Check key word only arguments
        if arguments.kwonlyargs:
            for kwarg in arguments.kwonlyargs:
                self._check_name("argument", kwarg.name, kwarg)

    visit_asyncfunctiondef = visit_functiondef

    @utils.check_messages("non-ascii-name")
    def visit_global(self, node: nodes.Global) -> None:
        for name in node.names:
            self._check_name("const", name, node)

    @utils.check_messages("non-ascii-name")
    def visit_assignname(self, node: nodes.AssignName) -> None:
        """Check module level assigned names."""
        # The NameChecker from which this Checker originates knows a lot of different
        # versions of variables, i.e. constants, inline variables etc.
        # To simplify we use only `variable` here, as we don't need to apply different
        # rules to different types of variables.
        frame = node.frame()

        if isinstance(frame, nodes.FunctionDef):
            if node.parent in frame.body:
                # Only perform the check if the assignment was done in within the body
                # of the function (and not the function parameter definition
                # (will be handled in visit_functiondef)
                # or within a decorator (handled in visit_call)
                self._check_name("variable", node.name, node)
        elif isinstance(frame, nodes.ClassDef):
            self._check_name("attr", node.name, node)
        else:
            # Possibilities here:
            # - isinstance(node.assign_type(), nodes.Comprehension) == inlinevar
            # - isinstance(frame, nodes.Module) == variable (constant?)
            # - some other kind of assigment missed but still most likely a variable
            self._check_name("variable", node.name, node)

    @utils.check_messages("non-ascii-name")
    def visit_classdef(self, node: nodes.ClassDef) -> None:
        self._check_name("class", node.name, node)
        for attr, anodes in node.instance_attrs.items():
            if not any(node.instance_attr_ancestors(attr)):
                self._check_name("attr", attr, anodes[0])

    def _check_module_import(self, node: Union[nodes.ImportFrom, nodes.Import]) -> None:
        for module_name, alias in node.names:
            name = alias or module_name
            self._check_name("module", name, node)

    @utils.check_messages("non-ascii-name")
    def visit_import(self, node: nodes.Import) -> None:
        self._check_module_import(node)

    @utils.check_messages("non-ascii-name")
    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        self._check_module_import(node)

    @utils.check_messages("non-ascii-name")
    def visit_call(self, node: nodes.Call) -> None:
        """Check if the used keyword args are correct."""
        for keyword in node.keywords:
            self._check_name("argument", keyword.arg, keyword)


def register(linter: lint.PyLinter) -> None:
    linter.register_checker(NonAsciiNameChecker(linter))
