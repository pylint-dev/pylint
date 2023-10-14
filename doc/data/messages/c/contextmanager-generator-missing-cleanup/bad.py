import contextlib


@contextlib.contextmanager
def cm():  # [contextmanager-generator-missing-cleanup]
    print("cm enter")
    a = yield
    print("cm exit")
