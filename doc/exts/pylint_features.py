# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Script used to generate the features file before building the actual documentation."""

import os
import subprocess
import sys

import sphinx


def builder_inited(app):
    popen = subprocess.Popen([sys.executable, "-m", "pylint", "--full-documentation"],
                             stdout=subprocess.PIPE)
    output, _ = popen.communicate()

    if not output:
        print("Pylint might not be available.")
        return

    features = os.path.join(os.path.dirname('.'), 'features.rst')
    with open(features, 'wb') as stream:
        stream.write(b"Pylint features\n")
        stream.write(b"===============\n\n")
        stream.write(output)


def setup(app):
    app.connect('builder-inited', builder_inited)
    return {'version': sphinx.__display_version__}
