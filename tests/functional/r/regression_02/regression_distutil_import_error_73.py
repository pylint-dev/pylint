"""
Regression test to check that distutils can be imported
See https://github.com/PyCQA/pylint/issues/73

See also:
https://github.com/PyCQA/pylint/issues/2955
https://github.com/PyCQA/astroid/pull/1321
"""

# pylint: disable=unused-import, deprecated-module

import distutils.version
from distutils.util import strtobool
from distutils import doesnottexists # [no-name-in-module]
from distutils.doesnottexists import nope # [no-name-in-module, import-error]
