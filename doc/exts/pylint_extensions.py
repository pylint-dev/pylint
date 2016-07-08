#!/usr/bin/env python
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Script used to generate the extensions file before building the actual documentation."""

import os
import sys

import sphinx

from pylint.lint import PyLinter


def builder_inited(app):
    # PACKAGE/docs/exts/pylint_extensions.py --> PACKAGE/
    base_path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # PACKAGE/ --> PACKAGE/pylint/extensions
    ext_path = os.path.join(base_path, 'pylint', 'extensions')
    modules = []
    for filename in os.listdir(ext_path):
        name, ext = os.path.splitext(filename)
        if ext != '.py' or name[0] == '_':
            continue
        # skip renamed deprecated modules to avoid conflicts with new modules
        if name == "check_docs":
            continue
        modules.append('pylint.extensions.%s' % name)
    if not modules:
        sys.exit("No Pylint extensions found?")

    linter = PyLinter()
    linter.load_plugin_modules(modules)

    extensions_doc = os.path.join(base_path, 'doc', 'extensions.rst')
    with open(extensions_doc, 'w') as stream:
        stream.write("Optional Pylint checkers in the extensions module\n")
        stream.write("=================================================\n\n")
        stream.write("Pylint provides the following optional plugins:\n\n")
        for module in modules:
            stream.write("- :ref:`{0}`\n".format(module))
        stream.write("\n")
        stream.write("You can activate any or all of these extensions "
                     "by adding a ``load-plugins`` line to the ``MASTER`` "
                     "section of your ``.pylintrc``, for example::\n")
        stream.write("\n    load-plugins=pylint.extensions.docparams,"
                     "pylint.extensions.docstyle\n\n")
        linter.print_plugin_documentation(stream)


def setup(app):
    app.connect('builder-inited', builder_inited)
    return {'version': sphinx.__display_version__}


if __name__ == "__main__":
    builder_inited(None)
