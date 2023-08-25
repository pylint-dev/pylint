import functools


def teacher(names):
    for name in names:

        def greet():
            functools.partial(print, f"Hello, {name}!")()

        bar()
