#!/usr/bin/env python

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Script used to generate the extensions file before building the actual documentation."""

from __future__ import annotations

import os
import re
import sys
from typing import Any, TypedDict

import sphinx
from sphinx.application import Sphinx

from pylint.checkers import BaseChecker
from pylint.constants import MAIN_CHECKER_NAME
from pylint.lint import PyLinter
from pylint.typing import MessageDefinitionTuple, OptionDict, ReportsCallable
from pylint.utils import get_rst_title


class _CheckerInfo(TypedDict):
    """Represents data about a checker."""

    checker: BaseChecker
    options: list[tuple[str, OptionDict, Any]]
    msgs: dict[str, MessageDefinitionTuple]
    reports: list[tuple[str, str, ReportsCallable]]
    doc: str
    module: str


# pylint: disable-next=unused-argument
def builder_inited(app: Sphinx | None) -> None:
    """Output full documentation in ReST format for all extension modules."""
    # PACKAGE/docs/exts/pylint_extensions.py --> PACKAGE/
    base_path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    # PACKAGE/ --> PACKAGE/pylint/extensions
    ext_path = os.path.join(base_path, "pylint", "extensions")
    modules = []
    doc_files: dict[str, str] = {}
    for filename in os.listdir(ext_path):
        name, ext = os.path.splitext(filename)
        if name[0] == "_":
            continue
        if ext == ".py":
            modules.append(f"pylint.extensions.{name}")
        elif ext == ".rst":
            doc_files["pylint.extensions." + name] = os.path.join(ext_path, filename)
    modules.sort()
    if not modules:
        sys.exit("No Pylint extensions found?")

    linter = PyLinter()
    linter.load_plugin_modules(modules)

    extensions_doc = os.path.join(
        base_path, "doc", "user_guide", "checkers", "extensions.rst"
    )
    with open(extensions_doc, "w", encoding="utf-8") as stream:
        stream.write(get_rst_title("Optional checkers", "="))
        stream.write(
            """
.. This file is auto-generated. Make any changes to the associated
.. docs extension in 'doc/exts/pylint_extensions.py'.

"""
        )
        stream.write("Pylint provides the following optional plugins:\n\n")
        for module in modules:
            stream.write(f"- :ref:`{module}`\n")
        stream.write("\n")
        stream.write(
            "You can activate any or all of these extensions "
            "by adding a ``load-plugins`` line to the ``MAIN`` "
            "section of your ``.pylintrc``, for example::\n"
        )
        stream.write(
            "\n    load-plugins=pylint.extensions.docparams,"
            "pylint.extensions.docstyle\n\n"
        )

        # Print checker documentation to stream
        by_checker = get_plugins_info(linter, doc_files)
        max_len = len(by_checker)
        for i, checker_information in enumerate(sorted(by_checker.items())):
            checker, information = checker_information
            j = -1
            checker = information["checker"]
            if i == max_len - 1:
                # Remove the \n\n at the end of the file
                j = -3
            print(
                checker.get_full_documentation(
                    msgs=information["msgs"],
                    options=information["options"],
                    reports=information["reports"],
                    doc=information["doc"],
                    module=information["module"],
                    show_options=False,
                )[:j],
                file=stream,
            )


def get_plugins_info(
    linter: PyLinter, doc_files: dict[str, str]
) -> dict[BaseChecker, _CheckerInfo]:
    by_checker: dict[BaseChecker, _CheckerInfo] = {}
    for checker in linter.get_checkers():
        if checker.name == MAIN_CHECKER_NAME:
            continue
        module = checker.__module__
        # Plugins only - skip over core checkers
        if re.match("pylint.checkers", module):
            continue
        # Find any .rst documentation associated with this plugin
        doc = ""
        doc_file = doc_files.get(module)
        if doc_file:
            with open(doc_file, encoding="utf-8") as f:
                doc = f.read()
        try:
            by_checker[checker]["checker"] = checker
            by_checker[checker]["options"] += checker._options_and_values()
            by_checker[checker]["msgs"].update(checker.msgs)
            by_checker[checker]["reports"] += checker.reports
            by_checker[checker]["doc"] += doc
            by_checker[checker]["module"] += module
        except KeyError:
            by_checker[checker] = _CheckerInfo(
                checker=checker,
                options=list(checker._options_and_values()),
                msgs=dict(checker.msgs),
                reports=list(checker.reports),
                doc=doc,
                module=module,
            )
    return by_checker


def setup(app: Sphinx) -> dict[str, str | bool]:
    app.connect("builder-inited", builder_inited)
    return {"version": sphinx.__display_version__, "parallel_read_safe": True}


if __name__ == "__main__":
    builder_inited(None)
