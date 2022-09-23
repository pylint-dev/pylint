# pylint: disable=missing-docstring,no-self-argument


class Cls:
    def __init__(self, obj, /):
        self.obj = obj

    # regression tests for no-method-argument getting reported
    # instead of no-self-argument
    def varargs(*args):
        """A method without a self argument but with *args."""

    def kwargs(**kwargs):
        """A method without a self argument but with **kwargs."""

    def varargs_and_kwargs(*args, **kwargs):
        """A method without a self argument but with *args and **kwargs."""
