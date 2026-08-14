"""Qualified ``typing.NoReturn`` / ``typing.Never`` should terminate a branch.

https://github.com/pylint-dev/pylint/issues/11271
"""
# pylint: disable=missing-docstring, missing-function-docstring, unused-argument, broad-exception-raised

import sys
import typing


def terminate(msg) -> typing.NoReturn:
    raise Exception(msg)


def print_platform_specific_command():
    if sys.platform == "linux":
        cmd = "ls"
    else:
        terminate("only runs on Linux")
    print(cmd)
