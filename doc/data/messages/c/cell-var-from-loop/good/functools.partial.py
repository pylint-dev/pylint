import functools


def greet_teachers(names):
    greetings = []
    for name in names:
        if name.isalpha():
            # "name" is evaluated when the partial is created here, so this
            # does not do lazy evaluation
            greetings.append(functools.partial(print, f"Hello, {name}!"))

    for greet in greetings:
        # `partial`s are called like functions, but you've already passed the
        # arguments to them
        greet()


greet_teachers(["Alice", "Bob", "Charlie", "Not-A-Name"])
# "Hello, Alice!", ...