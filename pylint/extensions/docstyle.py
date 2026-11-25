# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import codecs
from typing import TYPE_CHECKING

from astroid import nodes

from pylint import checkers
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class DocStringStyleChecker(checkers.BaseChecker):
    """Checks format of docstrings based on PEP 0257."""

    name = "docstyle"

    msgs = {
        "C0198": (
            'Bad docstring quotes in %s, expected """, given %s',
            "bad-docstring-quotes",
            "Used when a docstring does not have triple double quotes.",
        ),
        "C0199": (
            "First line empty in %s docstring",
            "docstring-first-line-empty",
            "Used when a blank line is found at the beginning of a docstring.",
        ),
    }

    def open(self) -> None:
        self._source_lines: list[bytes] = []

    @only_required_for_messages("docstring-first-line-empty", "bad-docstring-quotes")
    def visit_module(self, node: nodes.Module) -> None:
        # Keep the checked source, which can differ from the file when linting stdin.
        with node.stream() as stream:
            source = stream.read().removeprefix(codecs.BOM_UTF8)
            # AST line numbers follow universal newlines, including carriage returns.
            source = source.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        self._source_lines = source.split(b"\n")
        self._check_docstring("module", node)

    def visit_classdef(self, node: nodes.ClassDef) -> None:
        self._check_docstring("class", node)

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        ftype = "method" if node.is_method() else "function"
        self._check_docstring(ftype, node)

    visit_asyncfunctiondef = visit_functiondef

    def _check_docstring(
        self, node_type: str, node: nodes.Module | nodes.ClassDef | nodes.FunctionDef
    ) -> None:
        docstring = node.doc_node.value if node.doc_node else None
        if docstring and docstring[0] == "\n":
            self.add_message(
                "docstring-first-line-empty",
                node=node,
                args=(node_type,),
                confidence=HIGH,
            )

        if docstring:
            line = self._source_lines[node.fromlineno].lstrip()
            if line.startswith(b'"""'):
                return
            if b"'''" in line:
                quotes = "'''"
            elif line.startswith(b'"'):
                quotes = '"'
            elif line.startswith(b"'"):
                quotes = "'"
            else:
                quotes = ""
            if quotes:
                self.add_message(
                    "bad-docstring-quotes",
                    node=node,
                    args=(node_type, quotes),
                    confidence=HIGH,
                )


def register(linter: PyLinter) -> None:
    linter.register_checker(DocStringStyleChecker(linter))
