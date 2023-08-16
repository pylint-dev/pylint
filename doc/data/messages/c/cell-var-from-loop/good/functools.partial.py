import functools


def teacher_greeting(names):
    for name in names:

        def greet():
            print(functools.partial("Hello, {name}!".format, name=name)())

        greet()


teacher_greeting(["Graham", "John", "Terry", "Eric", "Terry", "Michael"])
