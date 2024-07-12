"""Tests for unexpected-keyword-arg"""
# pylint: disable=undefined-variable, too-few-public-methods, missing-function-docstring, missing-class-docstring


def non_param_decorator(func):
    """Decorator without a parameter"""

    def new_func():
        func()

    return new_func


def param_decorator(func):
    """Decorator with a parameter"""

    def new_func(internal_arg=3):
        func(junk=internal_arg)

    return new_func


def kwargs_decorator(func):
    """Decorator with kwargs.
    The if ... else makes the double decoration with param_decorator valid.
    """

    def new_func(**kwargs):
        if "internal_arg" in kwargs:
            func(junk=kwargs["internal_arg"])
        else:
            func(junk=kwargs["junk"])

    return new_func


@non_param_decorator
def do_something(junk=None):
    """A decorated function. This should not be passed a keyword argument"""
    print(junk)


do_something(internal_arg=2)  # [unexpected-keyword-arg]


@param_decorator
def do_something_decorated(junk=None):
    """A decorated function. This should be passed a keyword argument"""
    print(junk)


do_something_decorated(internal_arg=2)


@kwargs_decorator
def do_something_decorated_too(junk=None):
    """A decorated function. This should be passed a keyword argument"""
    print(junk)


do_something_decorated_too(internal_arg=2)


@non_param_decorator
@kwargs_decorator
def do_something_double_decorated(junk=None):
    """A decorated function. This should not be passed a keyword argument.
    non_param_decorator will raise an exception if a keyword argument is passed.
    """
    print(junk)


do_something_double_decorated(internal_arg=2)  # [unexpected-keyword-arg]


@param_decorator
@kwargs_decorator
def do_something_double_decorated_correct(junk=None):
    """A decorated function. This should be passed a keyword argument"""
    print(junk)


do_something_double_decorated_correct(internal_arg=2)


# Test that we don't crash on Class decoration
class DecoratorClass:
    pass


@DecoratorClass
def crash_test():
    pass


crash_test(internal_arg=2)  # [unexpected-keyword-arg]


# Test that we don't emit a false positive for uninferable decorators
@unknown_decorator
def crash_test_two():
    pass


crash_test_two(internal_arg=2)


# Test that we don't crash on decorators that don't return anything
def no_return_decorator(func):
    print(func)


@no_return_decorator
def test_no_return():
    pass


test_no_return(internal_arg=2)  # [unexpected-keyword-arg]


def ambiguous_func1(arg1):
    print(arg1)


def ambiguous_func2(other_arg1):
    print(other_arg1)


func1 = ambiguous_func1 if unknown else ambiguous_func2
func1(other_arg1=1)


def ambiguous_func3(arg1=None):
    print(arg1)


func2 = ambiguous_func1 if unknown else ambiguous_func3
func2()


def ambiguous_func4(arg1=print):
    print(arg1)


def ambiguous_func5(arg1=input):
    print(arg1)


def ambiguous_func6(arg1=42):
    print(arg1)


# Two functions with same keyword argument but different defaults (names)
func3 = ambiguous_func4 if unknown else ambiguous_func5
func3()


# Two functions with same keyword argument but different defaults (constants)
func4 = ambiguous_func3 if unknown else ambiguous_func6
func4()


# Two functions with same keyword argument but mixed defaults (names, constant)
func5 = ambiguous_func3 if unknown else ambiguous_func5
func5()


# pylint: disable=unused-argument
if do_something():
    class AmbiguousClass:
        def __init__(self, feeling="fine"):
            ...
else:
    class AmbiguousClass:
        def __init__(self, feeling="fine", thinking="hard"):
            ...


AmbiguousClass(feeling="so-so")
AmbiguousClass(thinking="carefully")
AmbiguousClass(worrying="little")  # we could raise here if we infer_all()


if do_something():
    class NotAmbiguousClass:
        def __init__(self, feeling="fine"):
            ...
else:
    class NotAmbiguousClass:
        def __init__(self, feeling="fine"):
            ...


NotAmbiguousClass(feeling="so-so")
NotAmbiguousClass(worrying="little")  # [unexpected-keyword-arg]

# pylint: enable=unused-argument
