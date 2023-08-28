import functools


def teacher(names):
    for name in names:

        def greet():
            print(functools.partial("Hello, {name}!".format, name=name)())

        greet()
