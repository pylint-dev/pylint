# pylint: disable=missing-docstring,unused-argument,too-few-public-methods
import contextlib
import typing


def target(pos, *, keyword):
    return pos + keyword


def forwarding_kwds(pos, **kwds):
    target(pos, **kwds)


def forwarding_args(*args, keyword):
    target(*args, keyword=keyword)


def forwarding_conversion(*args, **kwargs):
    target(*args, **dict(kwargs))


def not_forwarding_kwargs(*args, **kwargs):
    target(*args)  # [missing-kwoa]


target(1, keyword=2)

PARAM = 1
target(2, PARAM)  # [too-many-function-args, missing-kwoa]


def some_function(*, param):
    return param + 2


def other_function(**kwargs):
    return some_function(**kwargs)  # Does not trigger missing-kwoa


other_function(param=2)


class Parent:
    @typing.overload
    def __init__(self, *, first, second, third):
        pass

    @typing.overload
    def __init__(self, *, first, second):
        pass

    @typing.overload
    def __init__(self, *, first):
        pass

    def __init__(
        self,
        *,
        first,
        second: typing.Optional[str] = None,
        third: typing.Optional[str] = None,
    ):
        self._first = first
        self._second = second
        self._third = third


class Child(Parent):
    def __init__(self, *, first, second):
        super().__init__(first=first, second=second)
        self._first = first + second


@contextlib.contextmanager
def run(*, a):
    yield


def test_context_managers(**kw):
    run(**kw)

    with run(**kw):
        pass

    with run(**kw), run(**kw):
        pass

    with run(**kw), run():  # [missing-kwoa]
        pass


test_context_managers(a=1)

# Regression test for https://github.com/pylint-dev/pylint/issues/10029
# Keyword-only arguments provided through a **kwargs dict whose keys are
# inferable should not be reported as missing.
def fun_with_kwargs(a, b, *, c, d, **kwargs):
    """function with kwargs"""
    return a + b + c + d


someargs = {}
someargs["c"] = 3
someargs["d"] = 4
someargs["e"] = 5
someargs["f"] = 6

rval = fun_with_kwargs(1, 2, **someargs)

# Control: the dict does not contain the required keyword-only arguments.
otherargs = {"e": 5}
rval2 = fun_with_kwargs(1, 2, **otherargs)  # [missing-kwoa, missing-kwoa]
