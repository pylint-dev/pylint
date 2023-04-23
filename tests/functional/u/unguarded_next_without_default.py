"""Warnings for using next() without specifying a default value."""
# pylint: disable=missing-class-docstring, too-few-public-methods, missing-function-docstring
# pylint: disable=inconsistent-return-statements

next((i for i in (1, 2)), None)
next(i for i in (1, 2))  # [unguarded-next-without-default]
var = next(i for i in (1, 2))  # [unguarded-next-without-default]

try:
    next(i for i in (1, 2))
except StopIteration:
    pass

try:
    next(i for i in (1, 2))  # [unguarded-next-without-default]
except ValueError:
    pass

try:
    next(i for i in (1, 2))
except (ValueError, StopIteration):
    pass

try:
    next(i for i in (1, 2))
except ValueError:
    pass
except StopIteration:
    pass

redefined_next = next
redefined_next(i for i in (1, 2))  # [unguarded-next-without-default]


class MyClass:
    def __next__(self):
        return next(i for i in (1, 2))


# Example based on astroid code
def func(keywords, context):
    for value in keywords:
        try:
            return next(value.infer(context=context))
        except StopIteration:
            continue
