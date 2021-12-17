"""Tests for unexpected-keyword-arg"""


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


@param_decorator
def do_something_decorated(junk=None):
    """A decorated function. This should be passed a keyword argument"""
    print(junk)


@kwargs_decorator
def do_something_decorated_too(junk=None):
    """A decorated function. This should be passed a keyword argument"""
    print(junk)


@non_param_decorator
@kwargs_decorator
def do_something_double_decorated(junk=None):
    """A decorated function. This should not be passed a keyword argument.
    non_param_decorator will raise an exception if a keyword argument is passed.
    """
    print(junk)


@param_decorator
@kwargs_decorator
def do_something_double_decorated_correct(junk=None):
    """A decorated function. This should be passed a keyword argument"""
    print(junk)


def function_caller():
    """Call the decorated functions and check if they accept keywords"""
    do_something(internal_arg=2)  # [unexpected-keyword-arg]
    do_something_decorated(internal_arg=2)
    do_something_decorated_too(internal_arg=2)
    do_something_double_decorated(internal_arg=2)  # [unexpected-keyword-arg]
    do_something_double_decorated_correct(internal_arg=2)
