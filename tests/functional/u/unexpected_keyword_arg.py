"""Tests for unexpected-keyword-arg"""
# pylint: disable=undefined-variable, too-few-public-methods, missing-function-docstring, missing-class-docstring, magic-number


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
