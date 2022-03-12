#!/usr/bin/env python
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

"""Script used to generate the extensions file before building the actual documentation."""

import os
import re
import sys

import sphinx

from pylint.constants import MAIN_CHECKER_NAME
from pylint.lint import PyLinter
from pylint.utils import get_rst_title


def builder_inited(app):
    """Output full documentation in ReST format for all extension modules."""
    # PACKAGE/docs/exts/pylint_extensions.py --> PACKAGE/
    base_path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    # PACKAGE/ --> PACKAGE/pylint/extensions
    ext_path = os.path.join(base_path, "pylint", "extensions")
    modules = []
    doc_files = {}
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
        base_path, "doc", "technical_reference", "extensions.rst"
    )
    with open(extensions_doc, "w") as stream:
        stream.write(
            get_rst_title("Optional Pylint checkers in the extensions module", "=")
        )
        stream.write("Pylint provides the following optional plugins:\n\n")
        for module in modules:
            stream.write(f"- :ref:`{module}`\n")
        stream.write("\n")
        stream.write(
            "You can activate any or all of these extensions "
            "by adding a ``load-plugins`` line to the ``MASTER`` "
            "section of your ``.pylintrc``, for example::\n"
        )
        stream.write(
            "\n    load-plugins=pylint.extensions.docparams,"
            "pylint.extensions.docstyle\n\n"
        )

        # Print checker documentation to stream
        by_checker = get_plugins_info(linter, doc_files)
        for checker, information in sorted(by_checker.items()):
            checker = information["checker"]
            del information["checker"]
            print(checker.get_full_documentation(**information)[:-1], file=stream)


def get_plugins_info(linter, doc_files):
    by_checker = {}
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
            with open(doc_file) as f:
                doc = f.read()
        try:
            by_checker[checker]["checker"] = checker
            by_checker[checker]["options"] += checker.options_and_values()
            by_checker[checker]["msgs"].update(checker.msgs)
            by_checker[checker]["reports"] += checker.reports
            by_checker[checker]["doc"] += doc
            by_checker[checker]["module"] += module
        except KeyError:
            by_checker[checker] = {
                "checker": checker,
                "options": list(checker.options_and_values()),
                "msgs": dict(checker.msgs),
                "reports": list(checker.reports),
                "doc": doc,
                "module": module,
            }
    return by_checker


def setup(app):
    app.connect("builder-inited", builder_inited)
    return {"version": sphinx.__display_version__}


if __name__ == "__main__":
    builder_inited(None)
