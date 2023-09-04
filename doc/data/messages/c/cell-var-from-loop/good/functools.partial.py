import functools


def teacher_greeting(names):
    for name in names:

        greet = functools.partial(print, f"Hello, {name}!")

        greet()


teacher_greeting(["Graham", "John", "Terry", "Eric", "Terry", "Michael"])
