# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/7647

lambda referencing conditional kwargs dict should not trigger unnecessary-lambda.

Fix landed in pylint 3.1.0.
"""

# pylint: disable=missing-docstring
from contextlib import ExitStack


def fun(**kwargs):
    print(kwargs)


def run_in_context(callable_):
    with ExitStack():
        callable_()


def main(omit_arg: bool):
    kwargs = {} if omit_arg else {"arg": 2}
    run_in_context(lambda: fun(**kwargs))
