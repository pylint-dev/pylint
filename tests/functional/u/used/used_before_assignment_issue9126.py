"""Lambda parameters must not be looked up in the enclosing scope.
See https://github.com/pylint-dev/pylint/issues/9126"""
# pylint: disable=missing-function-docstring, missing-class-docstring
# pylint: disable=redefined-outer-name, too-few-public-methods, unnecessary-lambda-assignment


def direct_args():
    return lambda *args: args


def direct_kwargs():
    return lambda **kwargs: kwargs


def mixed():
    return lambda x, *args, **kw: (x, args, kw)


def nested_args():
    return lambda *args: (lambda: args)


def nested_positional():
    return lambda x: (lambda: x)


def nested_in_comprehension_vararg():
    return lambda *values: [lambda: values for _ in range(2)]


def nested_in_comprehension_positional():
    return lambda value: [(lambda: value) for _ in range(2)]


def nested_def():
    def inner(*args):
        return args

    return inner


def unbound():
    return lambda: missing  # [possibly-used-before-assignment]


def default_refers_to_enclosing_scope_vararg():
    return lambda a=args, *args: a  # [possibly-used-before-assignment]


def default_refers_to_enclosing_scope_positional():
    return lambda a=x, x=0: a  # [possibly-used-before-assignment]


class LambdaInClass:
    method = lambda *args, **kw: (args, kw)


if __name__ == "__main__":
    args = None
    kwargs = None
    kw = None
    x = None
    values = None
    value = None
    missing = None
