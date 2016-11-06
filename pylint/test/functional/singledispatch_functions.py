# pylint: disable=missing-docstring,import-error,unused-import,assignment-from-no-return
from __future__ import print_function
from UNINFERABLE import uninferable_decorator, uninferable_func

try:
    from functools import singledispatch
except ImportError:
    from singledispatch import singledispatch

my_single_dispatch = singledispatch  # pylint: disable=invalid-name


@singledispatch
def func(arg):
    return arg


@func.register(str)
def _(arg):
    return 42


@func.register(float)
@func.register(int)
def _(arg):
    return 42


@my_single_dispatch
def func2(arg):
    return arg


@func2.register(int)
def _(arg):
    return 42


@singledispatch
def with_extra_arg(arg, verbose=False):
    if verbose:
        print(arg)
    return arg


@with_extra_arg.register(str)
def _(arg, verbose=False):
    return arg[::-1]


@uninferable_decorator
def uninferable(arg):
    return 2*arg


@uninferable.register(str)
def bad_single_dispatch(arg):
    return arg


@uninferable_func.register(str)
def test(arg):
    return arg
