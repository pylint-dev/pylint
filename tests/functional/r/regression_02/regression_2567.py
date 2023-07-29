"""
Regression test for `no-member`.
See: https://github.com/pylint-dev/pylint/issues/2567
"""

# pylint: disable=missing-docstring,too-few-public-methods

import contextlib


@contextlib.contextmanager
def context_manager():
    try:
        yield
    finally:
        pass


cm = context_manager()
cm.__enter__()
cm.__exit__(None, None, None)


@contextlib.contextmanager
def other_context_manager():
    try:
        yield
    finally:
        pass


with other_context_manager():  # notice the function call
    pass
