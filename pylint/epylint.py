# mode: python; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4
# -*- vim:fenc=utf-8:ft=python:et:sw=4:ts=4:sts=4

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Emacs and Flymake compatible Pylint.

This script is for integration with emacs and is compatible with flymake mode.

epylint walks out of python packages before invoking pylint. This avoids
reporting import errors that occur when a module within a package uses the
absolute import path to get another module within this package.

For example:
    - Suppose a package is structured as

        a/__init__.py
        a/b/x.py
        a/c/y.py

   - Then if y.py imports x as "from a.b import x" the following produces pylint
     errors

       cd a/c; pylint y.py

   - The following obviously doesn't

       pylint a/c/y.py

   - As this script will be invoked by emacs within the directory of the file
     we are checking we need to go out of it to avoid these false positives.


You may also use py_run to run pylint with desired options and get back (or not)
its output.
"""

from __future__ import annotations

import os
import shlex
import sys
from collections.abc import Sequence
from io import StringIO
from subprocess import PIPE, Popen
from typing import NoReturn, TextIO, overload

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


def _get_env() -> dict[str, str]:
    """Extracts the environment PYTHONPATH and appends the current 'sys.path'
    to it.
    """
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(sys.path)
    return env


def lint(filename: str, options: Sequence[str] = ()) -> int:
    """Pylint the given file.

    When run from emacs we will be in the directory of a file, and passed its
    filename.  If this file is part of a package and is trying to import other
    modules from within its own package or another package rooted in a directory
    below it, pylint will classify it as a failed import.

    To get around this, we traverse down the directory tree to find the root of
    the package this module is in.  We then invoke pylint from this directory.

    Finally, we must correct the filenames in the output generated by pylint so
    Emacs doesn't become confused (it will expect just the original filename,
    while pylint may extend it with extra directories if we've traversed down
    the tree)
    """
    # traverse downwards until we are out of a python package
    full_path = os.path.abspath(filename)
    parent_path = os.path.dirname(full_path)
    child_path = os.path.basename(full_path)

    while parent_path != "/" and os.path.exists(
        os.path.join(parent_path, "__init__.py")
    ):
        child_path = os.path.join(os.path.basename(parent_path), child_path)
        parent_path = os.path.dirname(parent_path)

    # Start pylint
    # Ensure we use the python and pylint associated with the running epylint
    run_cmd = "import sys; from pylint.lint import Run; Run(sys.argv[1:])"
    cmd = (
        [sys.executable, "-c", run_cmd]
        + [
            "--msg-template",
            "{path}:{line}: {category} ({msg_id}, {symbol}, {obj}) {msg}",
            "-r",
            "n",
            child_path,
        ]
        + list(options)
    )

    with Popen(
        cmd, stdout=PIPE, cwd=parent_path, env=_get_env(), universal_newlines=True
    ) as process:

        for line in process.stdout:  # type: ignore[union-attr]
            # remove pylintrc warning
            if line.startswith("No config file found"):
                continue

            # modify the file name that's put out to reverse the path traversal we made
            parts = line.split(":")
            if parts and parts[0] == child_path:
                line = ":".join([filename] + parts[1:])
            print(line, end=" ")

        process.wait()
        return process.returncode


@overload
def py_run(
    command_options: str = ...,
    return_std: Literal[False] = ...,
    stdout: TextIO | int | None = ...,
    stderr: TextIO | int | None = ...,
) -> None:
    ...


@overload
def py_run(
    command_options: str,
    return_std: Literal[True],
    stdout: TextIO | int | None = ...,
    stderr: TextIO | int | None = ...,
) -> tuple[StringIO, StringIO]:
    ...


def py_run(
    command_options: str = "",
    return_std: bool = False,
    stdout: TextIO | int | None = None,
    stderr: TextIO | int | None = None,
) -> tuple[StringIO, StringIO] | None:
    """Run pylint from python.

    ``command_options`` is a string containing ``pylint`` command line options;
    ``return_std`` (boolean) indicates return of created standard output
    and error (see below);
    ``stdout`` and ``stderr`` are 'file-like' objects in which standard output
    could be written.

    Calling agent is responsible for stdout/err management (creation, close).
    Default standard output and error are those from sys,
    or standalone ones (``subprocess.PIPE``) are used
    if they are not set and ``return_std``.

    If ``return_std`` is set to ``True``, this function returns a 2-uple
    containing standard output and error related to created process,
    as follows: ``(stdout, stderr)``.

    To silently run Pylint on a module, and get its standard output and error:
        >>> (pylint_stdout, pylint_stderr) = py_run( 'module_name.py', True)
    """
    # Detect if we use Python as executable or not, else default to `python`
    executable = sys.executable if "python" in sys.executable else "python"

    # Create command line to call pylint
    epylint_part = [executable, "-c", "from pylint import epylint;epylint.Run()"]
    options = shlex.split(command_options, posix=not sys.platform.startswith("win"))
    cli = epylint_part + options

    # Providing standard output and/or error if not set
    if stdout is None:
        stdout = PIPE if return_std else sys.stdout
    if stderr is None:
        stderr = PIPE if return_std else sys.stderr
    # Call pylint in a subprocess
    with Popen(
        cli,
        shell=False,
        stdout=stdout,
        stderr=stderr,
        env=_get_env(),
        universal_newlines=True,
    ) as process:
        proc_stdout, proc_stderr = process.communicate()
        # Return standard output and error
        if return_std:
            return StringIO(proc_stdout), StringIO(proc_stderr)
        return None


def Run(argv: Sequence[str] | None = None) -> NoReturn:
    if not argv and len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} <filename> [options]")
        sys.exit(1)

    argv = argv or sys.argv[1:]
    if not os.path.exists(argv[0]):
        print(f"{argv[0]} does not exist")
        sys.exit(1)
    else:
        sys.exit(lint(argv[0], argv[1:]))


if __name__ == "__main__":
    Run()
