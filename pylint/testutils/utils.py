# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import contextlib
import os
import sys
from collections.abc import Iterator
from typing import TextIO


@contextlib.contextmanager
def _patch_streams(out: TextIO) -> Iterator[None]:
    """Patch and subsequently reset a text stream."""
    sys.stderr = sys.stdout = out
    try:
        yield
    finally:
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__


def create_files(paths: list[str], chroot: str = ".") -> None:
    """Creates directories and files found in <path>.

    :param list paths: list of relative paths to files or directories
    :param str chroot: the root directory in which paths will be created

    >>> from os.path import isdir, isfile
    >>> isdir('/tmp/a')
    False
    >>> create_files(['a/b/foo.py', 'a/b/c/', 'a/b/c/d/e.py'], '/tmp')
    >>> isdir('/tmp/a')
    True
    >>> isdir('/tmp/a/b/c')
    True
    >>> isfile('/tmp/a/b/c/d/e.py')
    True
    >>> isfile('/tmp/a/b/foo.py')
    True
    """
    dirs, files = set(), set()
    for path in paths:
        path = os.path.join(chroot, path)
        filename = os.path.basename(path)
        # path is a directory path
        if filename == "":
            dirs.add(path)
        # path is a filename path
        else:
            dirs.add(os.path.dirname(path))
            files.add(path)
    for dirpath in dirs:
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
    for filepath in files:
        with open(filepath, "w", encoding="utf-8"):
            pass
