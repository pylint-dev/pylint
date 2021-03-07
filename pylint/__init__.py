# Copyright (c) 2008, 2012 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014, 2016-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2018 Nick Drozd <nicholasdrozd@gmail.com>
# Copyright (c) 2020 Pierre Sassoulas <pierre.sassoulas@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import os
import sys

from pylint.__pkginfo__ import version as __version__

# pylint: disable=import-outside-toplevel


def run_pylint():
    from pylint.lint import Run as PylintRun

    try:
        PylintRun(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit(1)


def run_epylint():
    from pylint.epylint import Run as EpylintRun

    EpylintRun()


def run_pyreverse():
    """run pyreverse"""
    from pylint.pyreverse.main import Run as PyreverseRun

    PyreverseRun(sys.argv[1:])


def run_symilar():
    """run symilar"""
    from pylint.checkers.similar import Run as SimilarRun

    SimilarRun(sys.argv[1:])


def modify_sys_path() -> None:
    """Modify sys path for execution as Python module.

    Strip out the current working directory from sys.path.
    Having the working directory in `sys.path` means that `pylint` might
    inadvertently import user code from modules having the same name as
    stdlib or pylint's own modules.
    CPython issue: https://bugs.python.org/issue33053

    - Remove the first entry. This will always be either "" or the working directory
    - Remove the working directory from the second and third entries. This can
      occur if PYTHONPATH includes a ":" at the beginning or the end.
      https://github.com/PyCQA/pylint/issues/3636
    - Don't remove the working directory from the rest. It will be included
      if pylint is installed in an editable configuration (as the last item).
      https://github.com/PyCQA/pylint/issues/4161
    """
    sys.path = [
        p for i, p in enumerate(sys.path) if i > 0 and not (i < 3 and p == os.getcwd())
    ]


__all__ = ["__version__"]
