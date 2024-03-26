import contextlib


@contextlib.contextmanager
def cm():
    contextvar = "acquired context"
    print("cm enter")
    yield contextvar
    print("cm exit")


def genfunc_with_cm():  # [contextmanager-generator-missing-cleanup]
    with cm() as context:
        yield context * 2
