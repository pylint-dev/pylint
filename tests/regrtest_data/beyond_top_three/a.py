# pylint: disable=missing-docstring

from .level1.beyond_top_three import func


def do_something(var, some_other_var):  # error
    func(var, some_other_var)
