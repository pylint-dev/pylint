# Regression test for https://github.com/pylint-dev/pylint/issues/7647
# `unnecessary-lambda` was wrongly emitted when the lambda called a function
# with `**kwargs` built from an if-else expression.
"""No `unnecessary-lambda` when kwargs come from an if-else expression."""
from contextlib import ExitStack


def eat(**kwargs):
    """Print the meal."""
    print(kwargs)


def run_in_context(callback):
    """Run the callback inside a context."""
    with ExitStack():
        callback()


def main(hungry: bool):
    """Build kwargs conditionally and run."""
    kwargs = {} if hungry else {"fruit": "apple"}
    run_in_context(lambda: eat(**kwargs))
