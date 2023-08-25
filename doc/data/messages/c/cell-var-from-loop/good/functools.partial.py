import functools


def foo(numbers):
    for i in numbers:

        def bar():
            functools.partial(print, i)()

        bar()
