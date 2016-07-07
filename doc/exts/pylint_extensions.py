#!/usr/bin/env python
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Script used to generate the extensions file before building the actual documentation."""

import os
import subprocess
import sys

import sphinx


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
    modules_list = ",".join(modules)
    if not modules_list:
        sys.exit("No Pylint extensions found?")

    popen = subprocess.Popen([sys.executable, "-m", "pylint", "--plugins-only",
                              "--plugin-documentation", "--load-plugins",
                              modules_list],
                             stdout=subprocess.PIPE)
    output, _ = popen.communicate()

    if not output:
        sys.exit(popen.returncode)

    extensions_doc = os.path.join(base_path, 'doc', 'extensions.rst')
    with open(extensions_doc, 'wb') as stream:
        stream.write(b"Optional Pylint checkers in the extensions module\n")
        stream.write(b"=================================================\n\n")
        stream.write(b"Pylint provides the following optional plugins:\n\n")
        for module in modules:
            stream.write(b"- :ref:`{0}`\n".format(module))
        stream.write("\n")
        stream.write(b"You can activate any or all of these extensions "
                     b"by adding a ``load-plugins`` line to the ``MASTER`` "
                     b"section of your ``.pylintrc``, for example::\n")
        stream.write(b"\n    load-plugins=pylint.extensions.docparams,"
                     b"pylint.extensions.docstyle\n\n")
        stream.write(output)


def setup(app):
    app.connect('builder-inited', builder_inited)
    return {'version': sphinx.__display_version__}


if __name__ == "__main__":
    builder_inited(None)
