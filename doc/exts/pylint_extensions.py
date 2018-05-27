#!/usr/bin/env python
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Script used to generate the extensions file before building the actual documentation."""

import os
import re
import sys

import pkg_resources
import sphinx

from pylint.lint import PyLinter


# Some modules have been renamed and deprecated under their old names.
# Skip documenting these modules since:
# 1) They are deprecated, why document them moving forward?
# 2) We can't load the deprecated module and the newly renamed module at the
#    same time without getting naming conflicts
DEPRECATED_MODULES = [
    'check_docs',  # ==> docparams
]

def builder_inited(app):
    """Output full documentation in ReST format for all extension modules"""
    # PACKAGE/docs/exts/pylint_extensions.py --> PACKAGE/
    base_path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # PACKAGE/ --> PACKAGE/pylint/extensions
    ext_path = os.path.join(base_path, 'pylint', 'extensions')
    modules = []
    doc_files = {}
    for filename in os.listdir(ext_path):
        name, ext = os.path.splitext(filename)
        if name[0] == '_' or name in DEPRECATED_MODULES:
            continue
        if ext == '.py':
            modules.append('pylint.extensions.%s' % name)
        elif ext == '.rst':
            doc_files['pylint.extensions.' + name] = os.path.join(ext_path,
                                                                  filename)
    modules.sort()
    if not modules:
        sys.exit("No Pylint extensions found?")

    linter = PyLinter()
    linter.load_plugin_modules(modules)

    extensions_doc = os.path.join(base_path, 'doc', 'technical_reference', 'extensions.rst')
    with open(extensions_doc, 'w') as stream:
        stream.write("Optional Pylint checkers in the extensions module\n")
        stream.write("=================================================\n\n")
        stream.write("Pylint provides the following optional plugins:\n\n")
        for module in modules:
            stream.write("- :ref:`{}`\n".format(module))
        stream.write("\n")
        stream.write("You can activate any or all of these extensions "
                     "by adding a ``load-plugins`` line to the ``MASTER`` "
                     "section of your ``.pylintrc``, for example::\n")
        stream.write("\n    load-plugins=pylint.extensions.docparams,"
                     "pylint.extensions.docstyle\n\n")
        by_module = get_plugins_info(linter, doc_files)
        for module, info in sorted(by_module.items()):
            linter._print_checker_doc(info['name'], info, stream=stream)


def get_plugins_info(linter, doc_files):
    by_module = {}

    for checker in linter.get_checkers():
        if checker.name == 'master':
            continue
        module = checker.__module__
        # Plugins only - skip over core checkers
        if re.match("pylint.checkers", module):
            continue

        # Find any .rst documentation associated with this plugin
        doc = ""
        doc_file = doc_files.get(module)
        if doc_file:
            with open(doc_file, 'r') as f:
                doc = f.read()

        try:
            by_module[module]['options'] += checker.options_and_values()
            by_module[module]['msgs'].update(checker.msgs)
            by_module[module]['reports'] += checker.reports
            by_module[module]['doc'] += doc
            by_module[module]['name'] += checker.name
            by_module[module]['module'] += module
        except KeyError:
            by_module[module] = {
                'options': list(checker.options_and_values()),
                'msgs':    dict(checker.msgs),
                'reports': list(checker.reports),
                'doc':     doc,
                'name':    checker.name,
                'module':  module,
            }

    return by_module


def setup(app):
    app.connect('builder-inited', builder_inited)
    return {'version': sphinx.__display_version__}


if __name__ == "__main__":
    builder_inited(None)
